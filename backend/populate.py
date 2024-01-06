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
        name = region.get('name')
        image = region.get('image')
        new_region = Region(name=name, image_link=image)
        new_region.insert()


def populate_habitats():
    habitat_info = [
        {'name': 'Africa', 'region': 'Africa'},
        {'name': 'Antartica', 'region': 'Antartica'},
        {'name': 'Asia', 'region': 'Asia'},
        {'name': 'Australia', 'region': 'Oceania'},
        {'name': 'Central Africa', 'region': 'Africa'},
        {'name': 'Coastal Colombia', 'region': 'South America'},
        {'name': 'Eastern Australia', 'region': 'Oceania'},
        {'name': 'Europe', 'region': 'Europe'},
        {'name': 'Galápagos Islands of Ecuador', 'region': 'South America'},
        {'name': 'New Guinea Island', 'region': 'Oceania'},
        {'name': 'North America', 'region': 'Africa'},
        {'name': 'Northern Africa', 'region': 'Africa'},
        {'name': 'South America', 'region': 'South America'},
        {'name': 'Southern Africa', 'region': 'Africa'},
        {'name': 'Southern Florida', 'region': 'North America'},
        {'name': 'Venezuela', 'region': 'South America'},
        {'name': 'West Indies', 'region': 'South America'},
        {'name': 'Yucatán Peninsula', 'region': 'North America'},
        {'name': 'sub-Saharan Africa', 'region': 'Africa'},
    ]

    for habitat in habitat_info:
        name = habitat.get('name')
        region = habitat.get('region')
        get_region = Region.query.filter(Region.name == region).one_or_none()
        new_habitat = Habitat(name=name, region_id=get_region.id)
        new_habitat.insert()


def populate_birds():
    bird_info = [
        {'common_name': 'American flamingo',
         'species': 'Phoenicopterus ruber',
         'habitats': ['Galápagos Islands of Ecuador', 'Coastal Colombia', 'Venezuela', 'West Indies', 'Yucatán Peninsula', 'Southern Florida'],
         'image': 'https://ak.picdn.net/shutterstock/videos/1032061757/thumb/1.jpg'},
        {'common_name': 'Budgerigar',
         'species': 'Melopsittacus undulatus',
         'habitats': ['Australia'],
         'image': 'https://c.pxhere.com/photos/6a/cb/budgie_bird_parakeet_animals_wildlife_photography_ziervogel_feather_creature-1386714.jpg!d'},
        {'common_name': 'African Grey Parrot',
         'species': 'Psittacus erithacus',
         'habitats': ['Central Africa'],
         'image': 'https://images.pexels.com/photos/1599532/pexels-photo-1599532.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260'},
        {'common_name': 'European robin',
         'species': 'Erithacus rubecula',
         'habitats': ['Europe', 'Northern Africa'],
         'image': 'https://www.publicdomainpictures.net/pictures/40000/velka/bird-robin-erithacus-rubecula.jpg'},
        {'common_name': 'Galah',
         'species': 'Eolophus roseicapilla',
         'habitats': ['Australia'],
         'image': 'https://tse2.mm.bing.net/th/id/OIP.6JP6q5MZ1RfLWCjKdA00eAHaE8?rs=1&pid=ImgDetMain'},
        {'common_name': 'Sulphur-crested cockatoo',
         'species': 'Cacatua galerita',
         'habitats': ['Eastern Australia', 'New Guinea Island'],
         'image': 'https://www.publicdomainpictures.net/pictures/40000/velka/sulphur-crested-cockatoo.jpg'},
        {'common_name': 'Bald eagle',
         'species': 'Haliaeetus leucocephalus',
         'habitats': ['North America'],
         'image': 'https://www.publicdomainpictures.net/pictures/20000/velka/amercian-bald-eagle.jpg'},
        {'common_name': 'African fish eagle',
         'species': 'Icthyophaga vocifer',
         'habitats': ['sub-Saharan Africa', 'Southern Africa'],
         'image': 'https://images.pexels.com/photos/1109945/pexels-photo-1109945.jpeg?cs=srgb&dl=africa-bird-fish-eagle-zambia-1109945.jpg&fm=jpg'},
        {'common_name': 'Peregrine falcon',
         'species': 'Falco peregrinus',
         'habitats': ['North America', 'South America', 'Asia', 'Europe', 'Africa', 'Australia'],
         'image': 'https://ak1.picdn.net/shutterstock/videos/1310071/thumb/1.jpg'},
        {'common_name': 'Emperor penguin',
         'species': 'Aptenodytes forsteri',
         'habitats': ['Antartica'],
         'image': 'https://images.pexels.com/photos/4147993/pexels-photo-4147993.jpeg?auto=compress&cs=tinysrgb&dpr=3&h=750&w=1260'},
        {'common_name': 'Common raven',
         'species': 'Corvus corax',
         'habitats': ['Europe', 'North America', 'Asia', 'Northern Africa'],
         'image': 'https://cdn.pixabay.com/photo/2017/06/30/19/46/common-raven-2459448_960_720.jpg'},
        {'common_name': 'African penguin',
         'species': 'Spheniscus demersus',
         'habitats': ['Southern Africa'],
         'image': 'https://tse3.mm.bing.net/th/id/OIP.rzjBtREzFR-iRKNIUVOV9wHaFj?rs=1&pid=ImgDetMain'},
    ]

    for bird in bird_info:
        common_name = bird.get('common_name')
        species = bird.get('species')
        image = bird.get('image')
        habitats = bird.get('habitats')
        get_habitat = Habitat.query.filter(Habitat.name.in_(habitats)).all()
        new_bird = Bird(common_name=common_name,
                        species=species, image_link=image)
        new_bird.habitats = get_habitat
        new_bird.insert()


if __name__ == '__main__':
    populate_region()
    populate_habitats()
    populate_birds()
