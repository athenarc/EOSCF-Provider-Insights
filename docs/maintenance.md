# Licence

<! --- SPDX-License-Identifier: CC-BY-4.0  -- >

## Introduction

The purpose of the document is to provide a set of guidelines and best practices for maintaining the software.

It covers:

* Regular maintenance tasks
* Upgrades and updates
* Data management
* Troubleshooting
* Health checks

## Regular Maintenance Tasks

Regular maintenance tasks include:

* Checking that the software is healthy (covered in [Health Checks](#health-checks))
* Checking that the service is up and running in the front-end (when a provider views their statistics in the providers' dashboard)
* Checking if any package vulnerabilities have been reported and doing the necessary updates (covered in [Upgrades and Updates](#upgrades-and-updates))
* Checking Sentry and resolving any issues
* Update the models if the schema of the Catalog API responses changes (covered in [Data Management](#data-management))

The frequency of these tasks depends on the criticality of the issue.

## Upgrades and Updates

Upgrading and updating the software is done through **GitHub releases**.

Releases can be separated into 3 categories:

* Major releases (i.e. 1.4.2 -> 2.0.0)
* Minor releases (i.e. 1.4.2 -> 1.5.0)
* Patch releases (i.e. 1.4.2 -> 1.4.3)

### Major Releases

Major releases describe a significant change in the software (i.e. a completely new feature). A breaking change (i.e. a change in the API) is also considered a major release.

In the case of a breaking change it must be explicitly written in the:

* release notes
* the README.md file

and also communicated to the users of the software (the providers' team).

### Minor Releases

Minor releases describe a change in the software that does not break the API. These releases can include:

* New features
* Bug fixes
* Performance improvements
* Security patches
* Documentation updates

### Patches

Patches are small changes that fix bugs or security issues that is important to be quickly resolved. They do not include any new features or breaking changes.

Patches should be modular meaning that they cover a specific issue and do not include any other changes.

## Data Management

Concerning persistence the software uses:

* The RS Mongo (external), which is used as a read-only database for getting past recommendations. In case the schema of the recommendations collection changes we must update the statistics queries.
* The Content-Based RS Mongo (external), which is used to store recommendation history. In case the schema of the recommendations collection changes we must update the statistics queries.

## Troubleshooting

Most issues concerning the service will be a consequence of:

* not having access to the RS Mongo
* not having access to the Content-Based RS Mongo
* the providers' backend not having access to the API deployed by Cyfronet

## Health Checks

The health checks are performed by the `health` API call. The call checks the following:

* the app is up and running
* we have access to the RS Mongo
* we have access to the Content-Based RS Mongo

Concerning monitoring (cronitor) and error tracking (sentry) check `monitoring-logging.md`.
