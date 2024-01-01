# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import os
from flask import Flask, jsonify, request, abort
from models import setup_db, Region, Habitat, Bird
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from populate import populate_region, populate_habitats, populate_birds
from auth import AuthError, requires_auth


def werkzeug_exceptions(e):
    '''werkzeug_exceptions(e) catches HTTP errors'''
    if isinstance(e, HTTPException):
        abort(e.code, e.description)
    abort(422)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#
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

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#


def create_app(test_config=None):

    app = Flask(__name__)
    if test_config is not None:
        setup_db(app, test_config)
    else:
        setup_db(app)
    CORS(app, origins="*")

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

    # ----------------------------------------------------------------------------#
    # Birds.
    # ----------------------------------------------------------------------------#

    @app.route('/birds', methods=['GET'])
    # @requires_auth('get:drinks-detail')
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
            werkzeug_exceptions(e)

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
                    'bird': get_bird.format()
                }
            )
        except Exception as e:
            werkzeug_exceptions(e)

    @app.route('/birds', methods=['POST'])
    def add_bird():
        try:
            body = request.get_json()
            common_name = body.get('common_name', None)
            species = body.get('species', None)
            habitats = body.get('habitats', None)
            image_link = body.get('image_link', '')

            # if required attributes are not submitted abort
            if None in [common_name, species, habitats] or len(habitats) == 0:
                abort(400)

            get_habitats = Habitat.query.filter(
                Habitat.id.in_(habitats)).all()

            # one of the habitats provided doesnt match the habitats in the db abort
            if (len(get_habitats) is not len(habitats)):
                abort(404)

            new_bird = Bird(common_name, species, image_link)
            new_bird.habitats = get_habitats

            try:
                new_bird.insert()
            except:
                abort(422, 'duplicate bird resource')

            return jsonify(
                {
                    'success': True,
                    'bird': new_bird.id,
                }
            )
        except Exception as e:
            werkzeug_exceptions(e)

    @app.route('/birds/<int:bird_id>', methods=['PUT'])
    def edit_bird(bird_id):
        try:
            edit_bird = Bird.query.filter(Bird.id == bird_id).one_or_none()
            # Resource not found
            if edit_bird is None:
                abort(404)

            body = request.get_json()
            habitats = body.get('habitats', None)
            print(habitats)

            if habitats and len(habitats) > 0:
                get_habitats = Habitat.query.filter(
                    Habitat.id.in_(habitats)).all()
                # one of the habitats provided doesnt match the habitats in the db abort
                if (len(get_habitats) is not len(habitats)):
                    abort(404)
                edit_bird.habitats = get_habitats
                try:
                    edit_bird.update()
                except:
                    abort(422)

            for att in ['common_name', 'species', 'image_link']:
                attribute = body.get(att, None)
                if attribute:
                    setattr(edit_bird, att, attribute)
                    try:
                        edit_bird.update()
                    except:
                        abort(422, f'Bird {att} already exist')

            return jsonify(
                {
                    'success': True,
                    'bird': edit_bird.id,
                }
            )
        except Exception as e:
            werkzeug_exceptions(e)

    @app.route('/birds/<int:bird_id>', methods=['DELETE'])
    def delete_bird(bird_id):
        try:
            bird = Bird.query.filter(
                Bird.id == bird_id).one_or_none()

            # If bird cannot be found abort
            if bird is None:
                abort(404)

            bird.delete()

            return jsonify(
                {
                    "success": True,
                    "deleted": bird_id
                }
            )

        except Exception as e:
            werkzeug_exceptions(e)

    # ----------------------------------------------------------------------------#
    # Habitats.
    # ----------------------------------------------------------------------------#

    @app.route('/habitats', methods=['GET'])
    def get_habitats():
        try:
            habitats = Habitat.query.order_by(Habitat.id)
            current_habitats = paginate_items(request, habitats)
            return jsonify(
                {
                    'success': True,
                    'habitats': current_habitats,
                    'total_habitats': len(habitats.all())
                }
            )
        except Exception as e:
            werkzeug_exceptions(e)

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
            werkzeug_exceptions(e)

    @app.route('/habitats', methods=['POST'])
    def add_habitats():
        try:
            body = request.get_json()
            name = body.get('name', None)
            region_id = body.get('region_id', None)
            habitat_bird = body.get('bird', None)
            search = body.get('search', None)

            if search:
                habitats = Habitat.query.filter(
                    Habitat.name.ilike('%' + search + '%')).all()
                formatted_habitats = [item.format() for item in habitats]

                return jsonify(
                    {
                        'success': True,
                        'habitats': formatted_habitats,
                        'total_habitats': len(habitats)
                    }
                )

            else:

                # if required attributes are not submitted abort
                if None in [name, region_id]:
                    abort(400)

                region = Region.query.filter(
                    Region.id == region_id).one_or_none()
                # if invalid region is given abort
                if region is None:
                    abort(400)

                new_habitat = Habitat(name=name, region_id=region.id)

                if habitat_bird:
                    update_bird = Bird.query.filter(
                        Bird.id == habitat_bird).one_or_none()

                    if update_bird is None:
                        abort(400)

                    new_habitat.Birds.append(update_bird)

                try:
                    new_habitat.insert()
                except:
                    abort(422, 'Habitat resource already exist')

                return jsonify(
                    {
                        'success': True,
                        'habitat': new_habitat.format(),
                    }
                )
        except Exception as e:
            werkzeug_exceptions(e)

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
                try:
                    edit_habitat.update()
                except:
                    abort(422, 'Habitat name already exist')

            if region_id:
                region = Region.query.filter(
                    Region.id == region_id).one_or_none()
                # if invalid region is given abort
                if region is None:
                    abort(400)
                edit_habitat.region_id = region_id
                try:
                    edit_habitat.update()
                except:
                    abort(422)

            return jsonify(
                {
                    'success': True,
                    'habitat': edit_habitat.id,
                }
            )
        except Exception as e:
            werkzeug_exceptions(e)

    @app.route('/habitats/<int:habitat_id>', methods=['DELETE'])
    def delete_habitat(habitat_id):
        try:
            habitat = Habitat.query.filter(
                Habitat.id == habitat_id).one_or_none()

            # If bird cannot be found abort
            if habitat is None:
                abort(404)

            habitat.delete()

            return jsonify(
                {
                    "success": True,
                    "deleted": habitat_id
                }
            )

        except Exception as e:
            werkzeug_exceptions(e)

    # ----------------------------------------------------------------------------#
    # Regions.
    # ----------------------------------------------------------------------------#
    @app.route('/regions', methods=['GET'])
    def get_regions():
        try:
            regions = Region.query.order_by(Region.id).all()
            regions_formatted = [region.format() for region in regions]
            return jsonify(
                {
                    'success': True,
                    'regions': regions_formatted,
                }
            )
        except Exception as e:
            werkzeug_exceptions(e)

    # ----------------------------------------------------------------------------#
    # Error Handlers.
    # ----------------------------------------------------------------------------#
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': 'forbidden'
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404,

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': error.description
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error.get('description', 'AuthError')
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run()

# curl http://127.0.0.1:5000/bird -X POST -H "Content-Type: application/json" -d '{"title":"Movie1", "actors":[1]}'
# curl http://127.0.0.1:5000/habitat -X POST -H "Content-Type: application/json" -d '{"name":"John Doe"}'
