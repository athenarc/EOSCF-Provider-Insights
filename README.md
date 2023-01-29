# Provider RS Insights for EOSCF

Component calculating statistics about the performance that services have on the RS of the marketplace.

## Warning

Until provider PIDs are added in the RS Mongo only the `health` API call will be able to run.

## Building and Running

Prerequisites:

1. Read access to RS Mongo (from Cyfronet)
2. Read access to our RS Content-based mongo (from Athena)

Build and run:

1. Make sure that you have added the `.env` file in the project root
2. Run `docker build -t provider-insights-image . -f Dockerfile-rs`
3. Run `docker run -p <port>:4558 provider-insights-image`

## Environment variables

The following variables should be set in the .env file.
Note that names of the env variables attempt to differentiate between the two RSs:

1. `COLLABORATIVE_RS` for the Cyfronet RS
2. `CONTENT_BASED_RS` for the Athena RS

```shell
# Mongo from the Athena recommender
CONTENT_BASED_RS_MONGO_HOST=localhost
CONTENT_BASED_RS_MONGO_PORT=27017
CONTENT_BASED_RS_MONGO_DATABASE=recommender
CONTENT_BASED_RS_MONGO_USERNAME=dev
CONTENT_BASED_RS_MONGO_PASSWORD=dev

# Mongo from the Cyfronet team
COLLABORATIVE_RS_HOST=localhost
COLLABORATIVE_RS_PORT=27017
COLLABORATIVE_RS_DATABASE=recommender
COLLABORATIVE_RS_USERNAME=dev
COLLABORATIVE_RS_PASSWORD=dev

# The private sdn key for sentry which we use for error logging
SENTRY_SDN=https://389434adfhsf...
```
