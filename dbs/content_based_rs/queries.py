import logging
from typing import Optional

from dbs.connector import MongoDbConnector, form_mongo_url
from pymongo.errors import ServerSelectionTimeoutError
from settings import APP_SETTINGS

logger = logging.getLogger(__name__)


class ContentBasedRSMongo:
    def __init__(self):
        self.mongo_connector = MongoDbConnector(
            uri=form_mongo_url(
                APP_SETTINGS["CREDENTIALS"]['CONTENT_BASED_RS_MONGO_USERNAME'],
                APP_SETTINGS["CREDENTIALS"]['CONTENT_BASED_RS_MONGO_PASSWORD'],
                APP_SETTINGS["CREDENTIALS"]['CONTENT_BASED_RS_MONGO_HOST'],
                APP_SETTINGS["CREDENTIALS"]['CONTENT_BASED_RS_MONGO_PORT']
            ),
            db_name=APP_SETTINGS["CREDENTIALS"]['CONTENT_BASED_RS_MONGO_DATABASE']
        )
        self.mongo_connector.connect()

    def check_health(self) -> Optional[str]:
        # Check that the database is up
        try:
            db_names = self.mongo_connector.get_conn().list_database_names()
        except ServerSelectionTimeoutError:
            error = "Could not establish connection with content based RS mongo"
            logger.error(error)
            return error

        if APP_SETTINGS["CREDENTIALS"]['CONTENT_BASED_RS_MONGO_DATABASE'] in db_names:
            return None
        else:
            error = f"Content based RS target database " \
                    f"{APP_SETTINGS['CREDENTIALS']['CONTENT_BASED_RS_MONGO_DATABASE']} does not exist"
            logger.error(error)
            return error

    def get_number_of_recommendations_daily(self, service_ids):
        result = self.mongo_connector.get_db()["recommendation"].aggregate([
            {
                '$match': {
                    'recommendation': {
                        '$not': {
                            '$size': 0
                        }
                    }
                }
            }, {
                '$project': {
                    '_id': 0,
                    'date': 1,
                    'recommendation': 1
                }
            }, {
                '$unwind': {
                    'path': '$recommendation'
                }
            }, {
                '$match': {
                    'recommendation.service_id': {
                        '$in': service_ids
                    }
                }
            }, {
                '$group': {
                    '_id': {
                        'day': {
                            '$dayOfMonth': '$date'
                        },
                        'month': {
                            '$month': '$date'
                        },
                        'year': {
                            '$year': '$date'
                        }
                    },
                    'count': {
                        '$sum': 1
                    }
                }
            }, {
                '$sort': {
                    '_id.year': 1,
                    '_id.month': 1,
                    '_id.day': 1
                }
            }
        ])

        return [(recommendations_per_service['_id'], recommendations_per_service['count'])
                for recommendations_per_service in result]

    def get_most_recommended(self, service_ids):
        result = self.mongo_connector.get_db()["recommendation"].aggregate([
            {
                '$match': {
                    'recommendation': {
                        '$not': {
                            '$size': 0
                        }
                    }
                }
            }, {
                '$project': {
                    '_id': 0,
                    'date': 1,
                    'recommendation': 1
                }
            }, {
                '$unwind': {
                    'path': '$recommendation'
                }
            }, {
                '$match': {
                    'recommendation.service_id': {
                        '$in': service_ids
                    }
                }
            }, {
                '$group': {
                    '_id': {
                        'service_id': '$recommendation.service_id'
                    },
                    'count': {
                        '$sum': 1
                    }
                }
            }, {
                '$sort': {
                    'count': -1
                }
            }
        ])

        return [(recommendations_per_service['_id'], recommendations_per_service['count'])
                for recommendations_per_service in result]

    def get_services_recommended_along_your_services(self, service_ids):
        result = self.mongo_connector.get_db()["recommendation"].aggregate([
            {
                '$match': {
                    'recommendation': {
                        '$not': {
                            '$size': 0
                        }
                    }
                }
            }, {
                '$project': {
                    '_id': 0,
                    'recommendation': 1
                }
            }, {
                '$match': {
                    'recommendation.service_id': {
                        '$in': service_ids
                    }
                }
            }, {
                '$set': {
                    'recommendation': '$recommendation.service_id'
                }
            }
        ])

        # return [recommendation['service_id']
        #         for recommendation_sets in result
        #         for recommendation in recommendation_sets['recommendation']
        #         if recommendation['service_id'] not in set(service_ids)]  # We do not include services of the provider

        return [recommendation_sets['recommendation'] for recommendation_sets in result]
