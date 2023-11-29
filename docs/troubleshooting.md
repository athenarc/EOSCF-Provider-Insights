# Licence

<! --- SPDX-License-Identifier: CC-BY-4.0  -- >

## Troubleshooting

- Common operational issues and solutions.
- Guidelines for diagnosing problems.

### Discover connection problems to databases

Any connection issues with databases can be discovered by doing a `GET` request to the `/v1/health` endpoint. The response will contain the status of all databases. If the status is `DOWN`, it means that the connection to the database is not working. The response will also contain the error message.

**Example response**

```json
{
    "status": "UP",  # Up if everything below is working
    "content_based_recs_mongo": {  # Our internal database for logging recommendations
        "status": "UP",
        "database_type": "Mongo"
    },
    "rs_mongo": {  # The marketplace RS mongo
        "status": "UP",
        "database_type": "Mongo"
    }
}
```
