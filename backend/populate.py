from models import setup_db, Region, Habitat, Bird


def populate_region():
    region_info = [
        {'name': 'Africa', 'image':
            'https://upload.wikimedia.org/wikipedia/commons/8/86/Africa_%28orthographic_projection%29.svg'},
        {'name': 'Antartica', 'image':
            'https://upload.wikimedia.org/wikipedia/commons/f/f2/Antarctica_%28orthographic_projection%29.svg'},
        {'name': 'Asia', 'image':
            'https://upload.wikimedia.org/wikipedia/commons/8/80/Asia_%28orthographic_projection%29.svg'},
        {'name': 'Europe', 'image':
            'https://upload.wikimedia.org/wikipedia/commons/4/44/Europe_orthographic_Caucasus_Urals_boundary_%28with_borders%29.svg'},
        {'name': 'North America', 'image':
            'https://upload.wikimedia.org/wikipedia/commons/4/43/Location_North_America.svg'},
        {'name': 'Oceania', 'image':
            'https://upload.wikimedia.org/wikipedia/commons/8/88/Oceania_%28centered_orthographic_projection%29.svg'},
        {'name': 'South America', 'image':
            'https://upload.wikimedia.org/wikipedia/commons/0/0f/South_America_%28orthographic_projection%29.svg'}
    ]

    for region in region_info:
        name = region.get("name")
        image = region.get("image")
        new_region = Region(name=name, image_link=image)
        new_region.insert()


def populate_habitats():
    habitat_info = [
        {'name': 'Austalia', 'region': 'Oceania'},
        {'name': 'Galápagos Islands of Ecuador', 'region': 'South America'},
        {'name': 'Coastal Colombia', 'region': 'South America'},
        {'name': 'Venezuela', 'region': 'South America'},
        {'name': 'West Indies', 'region': 'South America'},
        {'name': 'Yucatán Peninsula', 'region': 'North America'},
        {'name': 'Southern Florida', 'region': 'North America'},
    ]

    for habitat in habitat_info:
        name = habitat.get("name")
        region = habitat.get("region")
        get_region = Region.query.filter(Region.name == region).one_or_none()
        new_habitat = Habitat(name=name, region_id=get_region.id)
        new_habitat.insert()


def populate_birds():
    bird_info = [
        {'common_name': 'American flamingo',
         'species': 'Phoenicopterus ruber',
         'habitats': ['Galápagos Islands of Ecuador', 'Coastal Colombia', 'Venezuela', 'West Indies', 'Yucatán Peninsula', 'Southern Florida'],
         'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/American_flamingo_(Phoenicopterus_ruber).JPG/1920px-American_flamingo_(Phoenicopterus_ruber).JPG'},
        {'common_name': 'Budgerigar',
         'species': 'Melopsittacus undulatus',
         'habitats': ['Austalia'],
         'image': 'https://upload.wikimedia.org/wikipedia/commons/2/2b/Budgerigar_diagram-labeled.svg'},


    ]

    for bird in bird_info:
        common_name = bird.get("common_name")
        species = bird.get("species")
        image = bird.get("image")
        habitats = bird.get("habitats")
        get_habitat = Habitat.query.filter(Habitat.name.in_(habitats)).all()
        new_bird = Bird(common_name=common_name,
                        species=species, image_link=image)
        new_bird.habitats = get_habitat
        new_bird.insert()


if __name__ == '__main__':
    populate_region()
    populate_habitats()
    populate_birds()

# curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{"title":"Movie1", "actors":[1]}'
# curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{"name":"John Doe"}'
