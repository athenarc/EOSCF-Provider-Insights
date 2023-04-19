from dbs.collaborative_rs.queries import CollaborativeRSMongo
from dbs.content_based_rs.queries import ContentBasedRSMongo


def test_rs_mongo():
    db = CollaborativeRSMongo()

    health_check_error = db.check_health()

    if health_check_error is None:
        return {
            "rs_mongo": {
                "status": "UP",
                "database_type": "Mongo"
            }
        }
    else:
        return {
            "rs_mongo": {
                "status": "DOWN",
                "error": health_check_error,
                "database_type": "Mongo"
            }
        }


def test_content_based_rs_mongo():
    db = ContentBasedRSMongo()
    health_check_error = db.check_health()

    if health_check_error is None:
        return {
            "content_based_recs_mongo": {
                "status": "UP",
                "database_type": "Mongo"
            }
        }
    else:
        return {
            "content_based_recs_mongo": {
                "status": "DOWN",
                "error": health_check_error,
                "database_type": "Mongo"
            }
        }


def service_health_test():
    tests = [
        test_rs_mongo(),
        test_content_based_rs_mongo()
    ]
    response = {
        "status": "UP"
    }

    for test in tests:
        response = response | test
        if list(test.values())[0]['status'] == 'DOWN':
            response['status'] = "DOWN"

    return response
