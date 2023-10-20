# Licence

<! --- SPDX-License-Identifier: CC-BY-4.0  -- >

## Introduction

The Provider Insights service has the goal of generating RS statistics so as the providers have an overview of how well their services perform on the recommender.

Specifically the statistics generated are:

- Most recommended services
- Recommendations over time
- Most recommended services next to your services

The application is built as a microservice with a REST API that is deployed in the marketplace infrastructure (from Cyfronet) and is exposed to be accessed by the providers platform (from Athena).

## API

[Provider Insights API](https://provider-insights.docker-fid.grid.cyf-kr.edu.pl/docs)

**Note**: Authentications is needed to access the API.
