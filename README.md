# GraphGrid SDK
The GraphGrid Python SDK is a python-based software development kit that can be used to programmatically interact with GraphGrid services.

Currently, its primary purpose is to provide a flexible way to train NLP models on a variety of tasks.

This README covers setting up the SDK object and method overview.
For further documentation and tutorials please visit https://docs.graphgrid.com/2.0/#/ 
to learn about the GraphGrid SDK and the GraphGrid CDP platform.  

## Set Up the SDK object

The first step in using the SDK is setting up the `GraphGridSdk` python object.

```python
# Setup bootstrap config
bootstrap_conf = SdkBootstrapConfig(
    access_key='a3847750f486bd931de26c6e683b1dc4',
    secret_key='81a62cea53883f4a163a96355d47656e',
    url_base='localhost',
    is_docker_context=False)

# Initialize the SDK
sdk = GraphGridSdk(bootstrap_conf)
```

You create a `SdkBootstrapConfig` object that provides the basic configuration the SDK needs.
This example uses the default `access_key` and `secret_key` associated with [GraphGrid CDP](https://docs.graphgrid.com/2.0/#/).

You can initialize your `GraphGridSdk` object with that configuration and begin using the SDK.

For details on usage please see the docs on [GraphGrid SDK Usage](https://docs.graphgrid.com/2.0/#/graphgrid-docs/sdk/python-sdk-usage).

## GraphGrid SDK Methods

There are currently seven SDK methods available for use:

|  Method | Description |
|---| --- |
| nmt_train |  Kick off training job |
| nmt_status |  Status and results of a training job |
| job_run |  Kick off a custom job |
| job_status |  Status of a custom job |
| save_dataset |  Save a dataset for training |
| promote_model |  Promote an NLP model, swapping it in for use |
| nmt_train_pipeline | Kick off NLP model training pipeline |

The `nmt_train` and `nmt_status` methods are provided to trigger, monitor, and retrieve results from a `nlp-model-training` job run.
In contrast, the methods `job_run` and `job_status` are provided to trigger and monitor custom jobs.

The `nmt_train_pipeline` method is specifically for kicking off NLP model training pipeline, it 
runs training jobs, monitors them, and can promote the newly trained models.  

For details on specific methods please see the docs on [GraphGrid SDK Method Reference](https://docs.graphgrid.com/2.0/#/graphgrid-docs/sdk/python-sdk-method-reference).