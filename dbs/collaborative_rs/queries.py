import logging
from typing import Optional

from dbs.connector import MongoDbConnector, form_mongo_url
from dbs.exceptions import IdNotFound, PidNotFound
from pymongo.errors import ServerSelectionTimeoutError
from settings import APP_SETTINGS

logger = logging.getLogger(__name__)


class CollaborativeRSMongo:
    def __init__(self):
        self.mongo_connector = MongoDbConnector(
            uri=form_mongo_url(
                APP_SETTINGS["CREDENTIALS"]['COLLABORATIVE_RS_USERNAME'],
                APP_SETTINGS["CREDENTIALS"]['COLLABORATIVE_RS_PASSWORD'],
                APP_SETTINGS["CREDENTIALS"]['COLLABORATIVE_RS_HOST'],
                APP_SETTINGS["CREDENTIALS"]['COLLABORATIVE_RS_PORT']
            ),
            db_name=APP_SETTINGS["CREDENTIALS"]['COLLABORATIVE_RS_DATABASE']
        )
        self.mongo_connector.connect()

    def check_health(self) -> Optional[str]:
        # Check that all the required collections exist in the RS Mongo
        collections = ['recommendation']

        try:
            collection_list = self.mongo_connector.get_db().list_collection_names()
        except ServerSelectionTimeoutError:
            error = "Could not establish connection with RS mongo"
            logger.error(error)
            return error

        missing_collections = []
        for collection in collections:
            if collection not in collection_list:
                logger.error(f"Could not find collection {collection}")
                missing_collections.append(collection)

        return f"Collections {' '.join(missing_collections)} are missing" if len(missing_collections) != 0 else None

    def get_services_of_provider(self, provider_id):
        check = {
            'providers': provider_id
        }
        project = {
            '_id': 1
        }

        results = self.mongo_connector.get_db()["service"].find(
            filter=check,
            projection=project)

        return [result['_id'] for result in results]

    def get_provider_id_from_pid(self, pid: str) -> int:
        query = {
            'pid': pid
        }

        ret_val = self.mongo_connector.get_db()['provider'].find_one(
            filter=query
        )
        if ret_val is None:
            raise PidNotFound(f"Could not find the provider pid {pid}.")

        return ret_val['_id']

    def get_service_id_from_pid(self, pid: str) -> int:
        query = {
            'pid': pid
        }

        ret_val = self.mongo_connector.get_db()['service'].find_one(
            filter=query
        )
        if ret_val is None:
            raise PidNotFound(f"Could not find the service pid {pid}.")

        return ret_val['_id']

    def get_service_pid_from_id(self, service_id: int) -> str:
        query = {
            '_id': service_id
        }

        ret_val = self.mongo_connector.get_db()['service'].find_one(
            filter=query
        )
        if ret_val is None:
            raise IdNotFound(f"Could not find the service id {service_id}.")

        return ret_val['_id']

    def get_number_of_recommendations_daily(self, service_ids):
        result = self.mongo_connector.get_db()["recommendation"].aggregate([
            {
                '$match': {
                    'services': {
                        '$not': {
                            '$size': 0
                        }
                    }
                }
            }, {
                '$project': {
                    '_id': 0,
                    'services': 1,
                    'timestamp': 1
                }
            }, {
                '$unwind': {
                    'path': '$services'
                }
            }, {
                '$match': {
                    'services': {
                        '$in': service_ids
                    }
                }
            }, {
                '$group': {
                    '_id': {
                        'day': {
                            '$dayOfMonth': '$timestamp'
                        },
                        'month': {
                            '$month': '$timestamp'
                        },
                        'year': {
                            '$year': '$timestamp'
                        }
                    },
                    'count': {
                        '$sum': 1
                    }
                }
            }, {
                '$project': {
                    'count': 1,
                    '_id': 1
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
                    'services': {
                        '$not': {
                            '$size': 0
                        }
                    }
                }
            }, {
                '$project': {
                    '_id': 0,
                    'services': 1,
                    'timestamp': 1
                }
            }, {
                '$unwind': {
                    'path': '$services'
                }
            }, {
                '$match': {
                    'services': {
                        '$in': service_ids
                    }
                }
            }, {
                '$group': {
                    '_id': {
                        'service_id': '$services'
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
