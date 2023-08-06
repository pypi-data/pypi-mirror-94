# Inferrd

Inferrd is a hosting platform for TensorFlow.

### Authentication

In order to use this library you need to get a api token from [inferrd.com](https://inferrd.com)

Authenticate with the `inferrd.auth` method:

```python
import inferrd

inferrd.auth('<token>')
```

### Deploying TensorFlow

First, create a model on [inferrd.com](https://inferrd.com) and select the kind of instance you want. Then simple call `inferrd.deploy_tf`:

```python
import inferrd

# this only needs to be done once
inferrd.auth('<token>')

# deploy TF
inferrd.deploy_tf(tf_model, '<name of the model>')
```

### Fetching predictions

Inferrd allows us to pull predictions back into your notebook by using `inferrd.get_requests`:

```python
import inferrd

# this only needs to be done once
inferrd.auth('<token>')

# get the requests
requests = inferrd.get_requests('<name of the model>', limit=100, page=0, includeFailures=False)
```