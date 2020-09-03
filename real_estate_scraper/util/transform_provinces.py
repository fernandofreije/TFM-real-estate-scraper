from scrapy.utils.project import get_project_settings
from pymongo import MongoClient


class MongoTransformer:

    TRANSFORMATION_DICT = {
        'ACoruña': 'A Coruña',
        'Castellón-Castelló': 'Castellón-Castelló',
        'LasPalmas': 'Las Palmas',
        'SantaCruzdeTenerife': 'Santa Cruz de Tenerife',
        'Navarra-Nafarroa': 'Navarra',
        'Vizcaya-Bizkaia': 'Vizcaya',
        'Álava-Araba': 'Álava',
        'Guipúzcoa-Gipuzkoa': 'Gipuzkoa',
        'CiudadReal': 'Ciudad Real',
        'Castellón-Castelló': 'Castellón',
        "IslasBaleares-IllesBalears": "Baleares",
        'LaRioja': 'La Rioja',
        'València': 'Valencia',
    }

    def __init__(self):
        settings = get_project_settings()
        self.connection = MongoClient(
            settings['MONGODB_CONNECTION_STRING']
        )
        self.db = self.connection[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]

    def transform(self):
        for bad_name, good_name in MongoTransformer.TRANSFORMATION_DICT.items():
            self.collection.update_many(
                {'province': bad_name},
                {'$set': {'province': good_name}}
            )

    def __del__(self):
        self.connection.close()


if __name__ == "__main__":
    MongoTransformer().transform()
