# Licence

<! --- SPDX-License-Identifier: CC-BY-4.0  -- >

## Backup and Recovery

This application is stateless and does not store any information in local storage, apart from the temporary files in `Indexes` shared volume. Therefore, there is no need for backup for this application, but only for the contents of dependencies, mainly HDFS.

### HDFS

The application uses data stored in HDFS for its operation, more specifically a Index Storage directory, as well as directory with files representing of the relations graph.

The HDFS data should be periodically backed up, so that if main HDFS storage is lost, the backup data can be used. In such case all three NN Finder submodules will need to be restarted and temporarily connected to the backup HDFS storage with the credential variables `HDFS_URL` and `HDFS_USER` updated accordingly.

### PostgreSQL

The database used for training of indexes and storing of embeddings is PostgreSQL should be backed up periodically. The required tables are described in [System Architecture](system_architecture.md). If the database is lost, the NN Finder app can still function but no new indexes will be trained until the database is restored, or the backup is used in the Training Module.

### Configuration

The configuration files with fields defined as in [Configuration](configuration.md) should be backed up and stored on a secure server, as in [Security](security.md).