# Licence

<! --- SPDX-License-Identifier: CC-BY-4.0  -- >

## Deployment

### Prerequisites

1. `docker`
2. `.env` file in the project root (check `configuration.md` for more info)

### Databases

1. Read access to **RS Mongo** (from Cyfronet)
2. Read access to our **RS Content-based mongo** (from Athena, deployed on Cyfronet premises)

### Build and run

1. Make sure that you have added the `.env` file in the project root
2. Run `docker build -t provider-insights-image . -f Dockerfile`
3. Run `docker run -p <port>:4558 provider-insights-image`

Extra network configuration is needed for the service to be able to access both Mongo databases that uses to get the statistics.
