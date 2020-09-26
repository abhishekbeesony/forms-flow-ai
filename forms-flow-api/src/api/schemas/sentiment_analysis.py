from flask_pymongo import PyMongo

from ..models import mongo


class SentimentAnalysisSchema(object):
    """Schema for creating pymongo database instance
    with fields
    methods like update, find, delete can be added later
    """

    def __init__(self):
        self.fields = {"input_text": "string", "output_response": "collection"}

    def insert_sentiment(self, sentiment_object):
        # TODO: validate if all the object of database are currently there in required fields
        mongo_db = mongo.db.application_ai
        inserted = mongo_db.insert(sentiment_object)
        id = str(inserted.inserted_id)
        return f"Mongodb sentiment response created for {id}"

    def insert_entity(self, entity_object):
        mongo_db = mongo.db.entity_ai
        inserted = mongo_db.insert(entity_object)
        id = str(inserted.inserted_id)
        return f"Mongodb entity response created for {id}"