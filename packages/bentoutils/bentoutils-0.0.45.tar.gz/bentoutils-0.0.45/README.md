# bentoutils

## Contents

A) BentoML Framework (Custom Artifact) for [simpletransformers](https://github.com/ThilinaRajapakse/simpletransformers).

B) Console scripts for:

1. bentopack - package an existing pretrained model and save to the Model Registry

```
Usage: bentopack [OPTIONS]

Options:
  --module TEXT  fully qualified module name containing service to package
  --clz TEXT     class name of service to package
  --name TEXT    model name
  --path TEXT    directory path of pretrained model
  --help         Show this message and exit.
```

Example:
```
bentopack \
    --module TopicBentoService \        # python module containing service class
    --clz TopicBentoService \           # service class
    --name tm_train3_roberta_l_weigh \  # pretrained model name
    --path /srv/models/multilabel-topic # local path to pretrained model (excluding name)
```

2. deploy_to_knative - WIP
