# GGCORE TODO README
A suite of tools for working with AWS.

## Modules

### aws-utils

Tools for cleaning up resources in AWS Cloud environments.

### aws-params

Tools for managing AWS SSM Param Store.


### Venv/Pip Setup
`pip install -e .`


# Scripts

## update_model_metadata.py
Script to update the model metadata

Basic usage (in the same directory that update_model_metadata.py exists in):

```
python3 -m update_model_metadata {REVISION_NUMBER_TO_COPY_FROM} {REVISION_NUMBER_TO_COPY_TO}
```
e.g.

`python3 -m update_model_metadata 1.4.0 1.4.99`

which should yield the following output
```
download: s3://graphgrid-nlp-models/model_metadata_registry.json to ../../../tmp/tmpyppxj2ez/model_metadata_registry.json
copy: s3://graphgrid-nlp-models/model_metadata_registry.json to s3://graphgrid-nlp-models/model_metadata_registry_backup.json
upload: ../../../tmp/tmpyppxj2ez/model_metadata_registry_edited.json to s3://graphgrid-nlp-models/model_metadata_registry.json
```
It creates a copy of the current registry named model_metadata_registry_backup.json before uploading the new one. It should only be using built-in python packages, so no venvs or packages necessary.

