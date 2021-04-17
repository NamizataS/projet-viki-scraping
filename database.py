from pymongo import MongoClient
import pandas as pd


class Database:
    def __init__(self, df):
        self.shows = df.fillna("").to_dict(orient='records')
        self.client = MongoClient()
        self.db_viki = self.client.viki
        self.collection_viki = self.db_viki['shows']

    def insert(self):
        self.collection_viki.insert_many(self.shows)

    def update(self):
        for document in self.shows:
            result = self.collection_viki.update_one({'Nom': document['Nom']}, {'$set': document}, upsert=True)

    def get_types(self):
        cur = self.collection_viki.aggregate([{"$group": {"_id": "$Type", "TypeShows": {"$sum": 1}}}])
        return cur

    def get_countries(self):
        cur = self.collection_viki.aggregate(
            [{"$group": {"_id": "$Pays", "showsNumber": {"$sum": 1}}}, {'$sort': {'showsNumber': -1}}])
        return cur

    def get_best_shows(self):
        cur_best_series = self.collection_viki.find({'Type': 'Série'}).sort('Note', -1).limit(5)
        cur_best_movies = self.collection_viki.find({'Type': 'Film'}).sort('Note', -1).limit(5)
        return cur_best_movies, cur_best_series