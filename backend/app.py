import os
from flask import Flask, jsonify, request, abort
from models import setup_db, Region, Habitat, Bird
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from populate import populate_region, populate_habitats, populate_birds


ITEMS_PER_PAGE = 10


def paginate_items(request, selection_query):
    selected_page = request.args.get('page', 1, type=int)
    items_limit = request.args.get('limit', ITEMS_PER_PAGE, type=int)
    current_index = selected_page - 1
    selection = selection_query.limit(items_limit).offset(
        current_index * items_limit).all()
    # If the page query param is out of range abort
    if len(selection) == 0:
        abort(404)
    items = [item.format() for item in selection]
    return items


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    with app.app_context():
        populate_region()
        populate_habitats()
        populate_birds()

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS'
        )
        return response

    @app.route('/birds', methods=['GET'])
    def get_birds():
        try:
            selection_query = Bird.query.order_by(Bird.id)
            current_birds = paginate_items(request, selection_query)
            return jsonify(
                {
                    'success': True,
                    'birds': current_birds,
                    'total_birds': len(selection_query.all())
                }
            )
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            abort(422)

    @app.route('/birds/<int:bird_id>', methods=['GET'])
    def get_specified_bird(bird_id):
        try:
            get_bird = Bird.query.filter(Bird.id == bird_id).one_or_none()
            # Resource not found
            if get_bird is None:
                abort(404)

            return jsonify(
                {
                    'success': True,
                    'bird': get_bird.edit_format()
                }
            )
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            abort(422)

    @app.route('/birds', methods=['POST'])
    def add_birds():
        try:
            body = request.get_json()
            common_name = body.get('common_name', None)
            species = body.get('species', None)
            habitats = body.get('habitats', None)
            image_link = body.get('image_link', '')

            # if required attributes are not submitted abort
            if None in [common_name or species or habitats] or len(habitats) == 0:
                abort(400)

            new_bird = Bird(common_name=common_name, species=species,
                            image_link=image_link)

            for habitat in habitats:
                get_habitat = Habitat.query.filter(
                    Habitat.id == habitat).one_or_none()
                # one of the habitats provided doesnt match the habitats in the db
                if get_habitat is None:
                    abort(400)
                new_bird.habitats.append(get_habitat)

            # TODO what if habitat contains id not in db
            # if len(get_habitats) == 0:
                # abort(400)
            # new_bird.habitats = get_habitats

            new_bird.insert()

            return jsonify(
                {
                    'success': True,
                    'bird': new_bird.id,
                }
            )
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            abort(422)

    @app.route('/birds/<int:bird_id>', methods=['PUT'])
    def edit_birds(bird_id):
        try:
            edit_bird = Bird.query.filter(Bird.id == bird_id).one_or_none()
            # Resource not found
            if edit_bird is None:
                abort(404)

            body = request.get_json()
            common_name = body.get('common_name', None)
            species = body.get('species', None)
            image_link = body.get('image_link', None)
            habitats = body.get('habitats', None)

            if common_name:
                edit_bird.common_name = common_name
            if species:
                edit_bird.species = species
            if image_link:
                edit_bird.image_link = image_link
            if habitats:
                get_habitats = Habitat.query.filter(
                    Habitat.id.in_(habitats)).all()
                edit_bird.habitats = get_habitats

            try:
                edit_bird.update()
            except Exception as error:
                abort(422)

            return jsonify(
                {
                    'success': True,
                    'bird': edit_bird.id,
                }
            )
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            abort(422)

    @app.route('/habitats', methods=['GET'])
    def get_habitats():
        try:
            habitats = Habitat.query.order_by(Habitat.id).all()
            habitats_formatted = [habitat.format() for habitat in habitats]
            return jsonify(
                {
                    'success': True,
                    'habitats': habitats_formatted,
                    'total_habitats': len(habitats)
                }
            )
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            abort(422)

    @app.route('/habitats/<int:habitat_id>', methods=['GET'])
    def get_specified_habitat(habitat_id):
        try:
            get_habitat = Habitat.query.filter(
                Habitat.id == habitat_id).one_or_none()
            # Resource not found
            if get_habitat is None:
                abort(404)

            return jsonify(
                {
                    'success': True,
                    'habitat': get_habitat.format()
                }
            )
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            abort(422)

    @app.route('/habitats', methods=['POST'])
    def add_habitats():
        try:
            body = request.get_json()
            name = body.get('name', None)
            region_id = body.get('region_id', None)
            habitat_bird = body.get('bird', None)

            # if required attributes are not submitted abort
            if None in [name or region_id]:
                abort(400)

            region = Region.query.filter(Region.id == region_id).one_or_none()
            if region is None:
                abort(400)

            new_habitat = Habitat(name=name, region_id=region.id)

            if len(habitat_bird) > 0:
                update_bird = Bird.query.filter(
                    Bird.id == habitat_bird).one_or_none()

                if update_bird is None:
                    abort(400)

                new_habitat.Birds.append(update_bird)

            new_habitat.insert()

            return jsonify(
                {
                    'success': True,
                    'habitat': new_habitat.format(),
                }
            )
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            abort(422)

    @app.route('/habitats/<int:habitat_id>', methods=['PUT'])
    def edit_habitats(habitat_id):
        try:
            edit_habitat = Habitat.query.filter(
                Habitat.id == habitat_id).one_or_none()

            # Resource not found
            if edit_habitat is None:
                abort(404)

            body = request.get_json()
            name = body.get('name', None)
            region_id = body.get('region_id', None)

            if name:
                edit_habitat.name = name
            if region_id:
                edit_habitat.region_id = region_id

            try:
                edit_habitat.update()
            except Exception as error:
                abort(422)

            return jsonify(
                {
                    'success': True,
                    'habitat': edit_habitat.id,
                }
            )
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            abort(422)

    @app.route('/regions', methods=['GET'])
    def get_regions():
        try:
            regions = Region.query.order_by(Region.id).all()
            regions_formatted = [region.format() for region in regions]
            return jsonify(
                {
                    'success': True,
                    'regions': regions_formatted,
                    'total_regions': len(regions)
                }
            )
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            abort(422)

    return app


app = create_app()

if __name__ == '__main__':
    app.run()

# curl http://127.0.0.1:5000/bird -X POST -H "Content-Type: application/json" -d '{"title":"Movie1", "actors":[1]}'
# curl http://127.0.0.1:5000/habitat -X POST -H "Content-Type: application/json" -d '{"name":"John Doe"}'
