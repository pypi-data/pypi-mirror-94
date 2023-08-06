# pytest-docker-registry-fixtures

## Overview

Pytest fixtures to instantiate and populated local docker registries, using [lovely-pytest-docker](https://pypi.org/project/lovely-pytest-docker) and [docker-py](https://pypi.org/project/docker-py), for testing.

## Getting Started

Update <tt>setup.py</tt> to include:

```python
from distutils.core import setup

setup(
	tests_require=["pytest-docker-registry-fixtures"]
)
```

All fixtures should be automatically included via the <tt>pytest11</tt> entry point.
```python
import requests
import pytest
from pytest_docker_registry_fixtures import DockerRegistryInsecure, DockerRegistrySecure  # Optional, for typing

@pytest.mark.push_image("busybox:1.30.1", "alpine")
def test_docker_registry_secure(docker_registry_secure: DockerRegistrySecure):
    response = requests.head(f"https://{docker_registry_secure.endpoint}/v2/",
        headers=docker_registry_secure.auth_header,
        verify=str(docker_registry_secure.cacerts),
    )
    assert response.status_code == 200

def test_docker_registry_insecure(docker_registry_insecure: DockerRegistryInsecure):
    response = requests.head(f"http://{docker_registry_insecure.endpoint}/v2/")
    assert response.status_code == 200
```

The `push_image` mark can optionally be added to stage images in the registry prior to testing. See [Markers](#markers) for details.
## Compatibility

* Tested with python 3.8

## Installation
### From [pypi.org](https://pypi.org/project/pytest-docker-registry-fixtures/)

```
$ pip install pytest_docker_registry_fixtures
```

### From source code

```bash
$ git clone https://github.com/crashvb/pytest-docker-registry-fixtures
$ cd pytest-docker-registry-fixtures
$ virtualenv env
$ source env/bin/activate
$ python -m pip install --editable .[dev]
```

## Fixtures

### docker_client

Creates a Docker client using configuration values from environment variables. This fixture is used to replicate images into a registry.

```python
from docker import DockerClient

def test_docker_pull(docker_client: DockerClient):
    image = docker_client.image.pull("busybox:1.30.1")
```

### <a name="docker_compose_insecure"></a> docker_compose_insecure

This fixture uses the `docker_compose_files` fixture to locate a user-defined docker-compose configuration file (typically <tt>tests/docker-compose.yml</tt>) that contains the <tt>pytest-docker-registry-insecure</tt> service. If one cannot be located, an embedded configuration is copied to a temporary location and returned. This fixture is used to instantiate the insecure docker registry service.

### <a name="docker_compose_secure"></a> docker_compose_secure

This fixture uses the `docker_compose_files` fixture to locate a user-defined docker-compose configuration file (typically <tt>tests/docker-compose.yml</tt>) that contains the <tt>pytest-docker-registry-secure</tt> service. If one cannot be located, an embedded configuration is copied to a temporary location and returned. This fixture is used to instantiate the secure docker registry service; however, unlike the configuration returned by the [docker_compose_insecure](#docker_compose_insecure) fixture, this configuration will be treated as a template; the <tt>$PATH_CERTIFICATE</tt>, <tt>$PATH_HTPASSWD</tt>, and <tt>$PATH_KEY</tt> tokens will be populated with the absolute paths provided by the [docker_registry_certs](#docker_registry_certs) and [docker_registry_htpasswd](#docker_registry_htpasswd) fixtures, as appropriate.

### <a name="docker_registry_auth_header"></a> docker_registry_auth_header

Retrieves an HTTP basic authentication header that is populated with credentials that can access the secure docker registry service. The credentials are retrieved from the [docker_registry_password](#docker_registry_password) and [docker_registry_username](#docker_registry_username) fixtures. This fixture is used to replicate docker images into the secure docker registry service.

### <a name="docker_registry_cacerts"></a> docker_registry_cacerts

Locates a user-defined CA trust store (<tt>tests/cacerts</tt>) to use to verify connections to the secure docker registry service. If one cannot be located, a temporary trust store is created containing certificates from <tt>certifi</tt> and the [docker_registry_certs](#docker_registry_certs) fixture. This fixture is used to instantiate the secure docker registry service.

### <a name="docker_registry_certs"></a> docker_registry_certs

Returns the paths of the self-signed certificate authority certificate, certificate, and private key that are used by the secure docker registry service. This fixture is used to instantiate the secure docker registry service.

#### NamedTuple Fields

The following fields are defined in the tuple provided by this fixture:

* **ca_certificate** - Path to the self-signed certificate authority certificate.
* **ca_private_key** - Path to the self-signed certificate authority private key.
* **certificate** - Path to the certificate.
* **private_key** - Path to the private key.

Typing is provided by `pytest_docker_registry_fixtures.DockerRegistryCerts`.

### <a name="docker_registry_hwpasswd"></a> docker_registry_htpasswd

Provides the path to a htpasswd file that is used by the secure docker registry service. If a user-defined htpasswd file (<tt>tests/htpasswd</tt>) can be located, it is used. Otherwise, a temporary htpasswd file is created using credentials from the [docker_registry_password](#docker_registry_password) and [docker_registry_username](#docker_registry_username) fixtures. This fixture is used to instantiate the secure docker registry service.

### <a name="docker_registry_insecure"></a> docker_registry_insecure

Configures and instantiates a docker registry without TLS or authentication.

```python
import requests
from pytest_docker_registry_fixtures import DockerRegistryInsecure  # Optional, for typing

def test_docker_registry_insecure(docker_registry_insecure: DockerRegistryInsecure):

    for image_name in docker_registry_insecure.images:
        response = requests.head(
            f"http://{docker_registry_insecure.endpoint}/v2/{image_name.image}/manifests/{image_name.tag}",
        )
        assert response.status_code == 200
        assert "Docker-Content-Digest" in response.headers
```

#### NamedTuple Fields

The following fields are defined in the tuple provided by this fixture:

* **docker_client** - from [docker_client](#docker_client)
* **docker_compose** - Path to the fully instantiated docker-compose configuration.
* **endpoint** - Endpoint of the insecure docker registry service.
* **images** - List of images that were replicated into the insecure docker registry service.
* **service_name** - Name of the service within the docker-compose configuration.

Typing is provided by `pytest_docker_registry_fixtures.DockerRegistryInsecure`.

### <a name="docker_registry_password"></a> docker_registry_password

Provides a generated password to use for authentication to the secure docker registry service. This fixture is used to replicate docker images into the secure docker registry service.

### <a name="docker_registry_secure"></a> docker_registry_secure

Configures and instantiates a TLS enabled docker registry with HTTP basic authorization.

```python
import requests
from pytest_docker_registry_fixtures import DockerRegistrySecure  # Optional, for typing

def test_docker_registry_secure(docker_registry_secure: DockerRegistrySecure):

    for image_name in docker_registry_secure.images:
        response = requests.head(
            f"https://{docker_registry_secure.endpoint}/v2/{image_name.image}/manifests/{image_name.tag}",
            headers=docker_registry_secure.auth_header,
            verify=str(docker_registry_secure.cacerts),
        )
        assert response.status_code == 200
        assert "Docker-Content-Digest" in response.headers
```

#### NamedTuple Fields

The following fields are defined in the tuple provided by this fixture:

* **auth_header** - from [docker_registry_auth_header](#docker_registry_auth_header).
* **cacerts** - from [docker_registry_cacerts](#docker_registry_cacerts).
* **certs** - from [docker_registry_certs](#docker_registry_certs).
* **docker_client** - Docker client, from [docker_client](#docker_client), with injected authentication credentials for the secure docker registry service.
* **docker_compose** - Path to the fully instantiated docker-compose configuration.
* **endpoint** - Endpoint of the secure docker registry service.
* **htpasswd** - from [docker_registry_htpasswd](#docker_registry_htpasswd)
* **images** - List of images that were replicated into the secure docker registry service.
* **password** - from [docker_registry_password](#docker_registry_password).
* **service_name** - Name of the service within the docker-compose configuration.
* **ssl_context** - from [docker_registry_ssl_context](#docker_registry_ssl_context).
* **username** - from [docker_registry_username](#docker_registry_username).

Typing is provided by `pytest_docker_registry_fixtures.DockerRegistrySecure`.

### <a name="docker_registry_ssl_context"></a> docker_registry_ssl_context

Provides an SSL context containing the CA trust store from the  [docker_registry_cacerts](#docker_registry_cacerts) fixture. This fixture is used to instantiate the secure docker registry service.

### <a name="docker_registry_username"></a> docker_registry_username

Provides a generated username to use for authentication to the secure docker registry service. This fixture is used to replicate docker images into the secure docker registry service.

## <a name="markers"></a>Markers

### pytest.mark.push_image

This marker specifies the docker image name(s) that should be replicated to the docker registry service(s) prior to testing. It can ...

... decorate individual tests:

```python
import pytest
from pytest_docker_registry_fixtures import DockerRegistrySecure  # Optional, for typing

@pytest.mark.push_image("busybox:1.30.1", "alpine", "python,mysql:latest")
def test_docker_registry_secure(docker_registry_secure: DockerRegistrySecure):
	...
```

... be specified in the `pytestmark` list at the module level:

```python
#!/usr/bin/env python

import pytest

pytestmark = [pytest.mark.push_image("busybox:1.30.1", "alpine", "python,mysql:latest")]

...
```

... or be provided via the corresponding `--push-image` command-line argument:

```bash
python -m pytest --push-image busybox:1.30.1 --push-image alpine --push-image python,mysql:latest ...
```

This marker supports being specified multiple times, and removes duplicate image names (see [Limitations](#limitations) below).

A helper function, `get_pushed_images`, is included for test scenarios that  wish to inspect the maker directly:

```python
import pytest
from pytest_docker_registry_fixtures import DockerRegistrySecure, get_pushed_images, ImageName

@pytest.mark.push_image("busybox:1.30.1")
def test_docker_registry_secure(docker_registry_secure: DockerRegistrySecure, request):
    image_name = ImageName.parse(get_pushed_images(request)[0])
```

## <a name="limitations"></a>Limitations

1. All the fixtures provided by this package are <tt>session</tt> scoped; and will only be executed once per test execution. This allows for a maximum of two docker registry services: one insecure instance and one secure instance.
2. The `push_image` marker is processed as part of the `docker_registry_insecure` and `docker_registry_secure` fixtures. As such:
  * _all_ markers will be aggregated during initialization of the session, and processed prior test execution.
  * Pushed images will be replicated to both the insecure and secure docker registries, if both are instantiated.
3. A working docker client is required to push images.

## Development

[Source Control](https://github.com/crashvb/pytest-docker-registry-fixtures)
