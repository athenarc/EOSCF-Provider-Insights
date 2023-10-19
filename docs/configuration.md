# Licence

<! --- SPDX-License-Identifier: CC-BY-4.0  -- >

## Introduction

The provider insights application uses both configuration files and environment variables to control its behaviour. We provide a detailed description of the configuration process below.

## Configuration Overview

The bare minimum configuration needed is creating the `.env` file in the root directory of the project. This file contains the environment variables needed to run the application.

One can then change the configuration file found in `config/backend-prod.yaml` that has variables controlling fastapi settings and application version.

- `.env`: Must be created, should never be committed to the repository.
- `config/backend-prod.yaml`: Optional, only controls fastapi settings and application version.

## Configuration Files

The configuration file (`config/backend-prod.yaml`) controls:

- `fastapi` configuration (workers, host, port, etc.)
- version of the application

We provide a detailed example of the configuration file below:

```yaml
VERSION_NAME: "v1" # Should be changed to differentiate between different versions of the model. It is used in logging and monitoring

FASTAPI:  # Fastapi configuration
  WORKERS: 4
  DEBUG: False
  RELOAD: False
  HOST: '0.0.0.0'
  PORT: 4558

```

## Environmental Variables

The environmental variables control integration with other services and databases. The `.env` file should be created in the root directory of the project and should contain the following variables:

```bash
# Mongo from the Athena recommender
CONTENT_BASED_RS_MONGO_HOST=localhost
CONTENT_BASED_RS_MONGO_PORT=27017
CONTENT_BASED_RS_MONGO_DATABASE=database_name
CONTENT_BASED_RS_MONGO_USERNAME=admin
CONTENT_BASED_RS_MONGO_PASSWORD=admin

# Mongo from the Cyfronet team
COLLABORATIVE_RS_HOST=localhost
COLLABORATIVE_RS_PORT=27017
COLLABORATIVE_RS_DATABASE=database_name
COLLABORATIVE_RS_USERNAME=admin
COLLABORATIVE_RS_PASSWORD=admin

# API Authentication token (needed by anyone attempting to access the API)
ACCESS_TOKEN=29yv1E2gD2j83W2x

# Monitoring services
SENTRY_SDN=https://asd1asd2.ingest.sentry.io/asd1asd2
CRONITOR_API_KEY=asd1asd2
```

## Security Considerations

Each variable that affects the behavior of the app and is not considered secret should be added to the configuration file (`config/backend-prod.yaml`).

The variables that are considered secret should be added to the `.env` file. The `.env` file should never be committed to the repository. It should be created manually on the server.
