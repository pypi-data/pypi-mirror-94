#!/usr/bin/env python

# pylint: disable=redefined-outer-name

"""The actual fixtures, you found them ;)."""

import logging

from base64 import b64encode
from distutils.util import strtobool
from functools import partial
from pathlib import Path
from ssl import create_default_context, SSLContext
from string import Template
from time import time
from typing import Any, Dict, Generator, List, NamedTuple

import pytest

from docker import DockerClient, from_env
from lovely.pytest.docker.compose import Services
from _pytest.tmpdir import TempPathFactory

from .imagename import ImageName
from .utils import (
    check_url_secure,
    DOCKER_REGISTRY_SERVICE,
    DOCKER_REGISTRY_SERVICE_PATTERN,
    generate_cacerts,
    generate_htpasswd,
    generate_keypair,
    get_docker_compose_user_defined,
    get_embedded_file,
    get_user_defined_file,
    replicate_image,
    start_service,
)

LOGGER = logging.getLogger(__name__)


class DockerRegistryCerts(NamedTuple):
    # pylint: disable=missing-class-docstring
    ca_certificate: Path
    ca_private_key: Path
    certificate: Path
    private_key: Path


class DockerRegistryInsecure(NamedTuple):
    # pylint: disable=missing-class-docstring
    docker_client: DockerClient
    docker_compose: Path
    endpoint: str
    images: List[Any]
    service_name: str


# Note: NamedTuple does not support inheritance :(
class DockerRegistrySecure(NamedTuple):
    # pylint: disable=missing-class-docstring
    auth_header: Dict[str, str]
    cacerts: Path
    certs: DockerRegistryCerts
    docker_client: DockerClient
    docker_compose: Path
    endpoint: str
    htpasswd: Path
    images: List[Any]
    password: str
    service_name: str
    ssl_context: SSLContext
    username: str


@pytest.fixture(scope="session")
def docker_client() -> DockerClient:
    """Provides an insecure Docker API client."""
    return from_env()


@pytest.fixture(scope="session")
def docker_compose_insecure(
    docker_compose_files: List[str], tmp_path_factory: TempPathFactory
) -> Generator[Path, None, None]:
    """
    Provides the location of the docker-compose configuration file containing the insecure docker registry service.
    """
    service_name = DOCKER_REGISTRY_SERVICE_PATTERN.format("insecure")
    yield from get_docker_compose_user_defined(docker_compose_files, service_name)
    # TODO: lovely-docker-compose uses the file for teardown ...
    yield from get_embedded_file(
        tmp_path_factory, delete_after=False, name="docker-compose.yml"
    )


@pytest.fixture(scope="session")
def docker_compose_secure(
    docker_compose_files: List[str], tmp_path_factory: TempPathFactory
) -> Generator[Path, None, None]:
    """
    Provides the location of the templated docker-compose configuration file containing the secure docker registry
    service.
    """
    service_name = DOCKER_REGISTRY_SERVICE_PATTERN.format("secure")
    yield from get_docker_compose_user_defined(docker_compose_files, service_name)
    # TODO: lovely-docker-compose uses the file for teardown ...
    yield from get_embedded_file(
        tmp_path_factory, delete_after=False, name="docker-compose.yml"
    )


@pytest.fixture(scope="session")
def docker_registry_auth_header(
    docker_registry_password: str, docker_registry_username: str
) -> Dict[str, str]:
    """Provides an HTTP basic authentication header containing credentials for the secure docker registry service."""
    auth = b64encode(
        f"{docker_registry_username}:{docker_registry_password}".encode("utf-8")
    ).decode("utf-8")
    return {"Authorization": f"Basic {auth}"}


@pytest.fixture(scope="session")
def docker_registry_cacerts(
    docker_registry_certs: DockerRegistryCerts,
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[Path, None, None]:
    """
    Provides the location of a temporary CA certificate trust store that contains the certificate of the secure docker
    registry service.
    """
    yield from get_user_defined_file(pytestconfig, "cacerts")
    yield from generate_cacerts(
        tmp_path_factory, certificate=docker_registry_certs.ca_certificate
    )


@pytest.fixture(scope="session")
def docker_registry_certs(
    tmp_path_factory: TempPathFactory,
) -> Generator[DockerRegistryCerts, None, None]:
    """Provides the location of temporary certificate and private key files for the secure docker registry service."""
    # TODO: Augment to allow for reading certificates from /test ...
    tmp_path = tmp_path_factory.mktemp(__name__)
    keypair = generate_keypair()
    path_ca_certificate = tmp_path.joinpath(f"{DOCKER_REGISTRY_SERVICE}-ca.crt")
    path_ca_certificate.write_bytes(keypair.ca_certificate)
    path_ca_private_key = tmp_path.joinpath(f"{DOCKER_REGISTRY_SERVICE}-ca.key")
    path_ca_private_key.write_bytes(keypair.ca_private_key)
    path_certificate = tmp_path.joinpath(f"{DOCKER_REGISTRY_SERVICE}.crt")
    path_certificate.write_bytes(keypair.certificate)
    path_key = tmp_path.joinpath(f"{DOCKER_REGISTRY_SERVICE}.key")
    path_key.write_bytes(keypair.private_key)
    yield DockerRegistryCerts(
        ca_certificate=path_ca_certificate,
        ca_private_key=path_ca_private_key,
        certificate=path_certificate,
        private_key=path_key,
    )
    path_ca_certificate.unlink(missing_ok=True)
    path_ca_private_key.unlink(missing_ok=True)
    path_certificate.unlink(missing_ok=True)
    path_key.unlink(missing_ok=True)


@pytest.fixture(scope="session")
def docker_registry_htpasswd(
    docker_registry_password: str,
    docker_registry_username: str,
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[Path, None, None]:
    """Provides the location of the htpasswd file for the secure registry service."""
    yield from get_user_defined_file(pytestconfig, "htpasswd")
    yield from generate_htpasswd(
        tmp_path_factory,
        username=docker_registry_username,
        password=docker_registry_password,
    )


@pytest.fixture(scope="session")
def docker_registry_insecure(
    docker_client: DockerClient,
    docker_compose_insecure: Path,
    docker_services: Services,
    request,
) -> Generator[DockerRegistryInsecure, None, None]:
    """Provides the endpoint of a local, mutable, insecure, docker registry."""
    service_name = DOCKER_REGISTRY_SERVICE_PATTERN.format("insecure")
    LOGGER.debug("Starting insecure docker registry service ...")
    LOGGER.debug("  docker-compose : %s", docker_compose_insecure)
    LOGGER.debug("  service name   : %s", service_name)
    endpoint = start_service(
        docker_services,
        docker_compose=docker_compose_insecure,
        service_name=service_name,
    )
    LOGGER.debug("Insecure docker registry endpoint: %s", endpoint)

    LOGGER.debug("Replicating images into %s ...", service_name)
    images = _replicate_images(docker_client, endpoint, request)

    yield DockerRegistryInsecure(
        docker_client=docker_client,
        docker_compose=docker_compose_insecure,
        endpoint=endpoint,
        images=images,
        service_name=service_name,
    )


@pytest.fixture(scope="session")
def docker_registry_password() -> str:
    """Provides the password to use for authentication to the secure registry service."""
    return f"pytest.password.{time()}"


@pytest.fixture(scope="session")
def docker_registry_secure(
    docker_client: DockerClient,
    docker_compose_secure: Path,
    docker_registry_auth_header: Dict[str, str],
    docker_registry_cacerts: Path,
    docker_registry_certs: DockerRegistryCerts,
    docker_registry_htpasswd: Path,
    docker_registry_password: str,
    docker_registry_ssl_context: SSLContext,
    docker_registry_username: str,
    docker_services: Services,
    request,
    tmp_path_factory: TempPathFactory,
) -> Generator[DockerRegistrySecure, None, None]:
    # pylint: disable=too-many-arguments,too-many-locals
    """Provides the endpoint of a local, mutable, secure, docker registry."""
    service_name = DOCKER_REGISTRY_SERVICE_PATTERN.format("secure")
    tmp_path = tmp_path_factory.mktemp(__name__)

    # Create a secure registry service from the docker compose template ...
    path_docker_compose = tmp_path.joinpath("docker-compose.yml")
    template = Template(docker_compose_secure.read_text("utf-8"))
    path_docker_compose.write_text(
        template.substitute(
            {
                "PATH_CERTIFICATE": docker_registry_certs.certificate,
                "PATH_HTPASSWD": docker_registry_htpasswd,
                "PATH_KEY": docker_registry_certs.private_key,
            }
        ),
        "utf-8",
    )

    LOGGER.debug("Starting secure docker registry service ...")
    LOGGER.debug("  docker-compose : %s", path_docker_compose)
    LOGGER.debug("  ca certificate : %s", docker_registry_certs.ca_certificate)
    LOGGER.debug("  certificate    : %s", docker_registry_certs.certificate)
    LOGGER.debug("  htpasswd       : %s", docker_registry_htpasswd)
    LOGGER.debug("  private key    : %s", docker_registry_certs.private_key)
    LOGGER.debug("  password       : %s", docker_registry_password)
    LOGGER.debug("  service name   : %s", service_name)
    LOGGER.debug("  username       : %s", docker_registry_username)

    check_server = partial(
        check_url_secure,
        auth_header=docker_registry_auth_header,
        ssl_context=docker_registry_ssl_context,
    )
    endpoint = start_service(
        docker_services,
        check_server=check_server,
        docker_compose=path_docker_compose,
        service_name=service_name,
    )
    LOGGER.debug("Secure docker registry endpoint: %s", endpoint)

    # DUCK PUNCH: Inject the secure docker registry credentials into the docker client ...
    docker_client.api._auth_configs.add_auth(  # pylint: disable=protected-access
        endpoint,
        {"password": docker_registry_password, "username": docker_registry_username},
    )

    LOGGER.debug("Replicating images into %s ...", service_name)
    images = _replicate_images(docker_client, endpoint, request)

    yield DockerRegistrySecure(
        auth_header=docker_registry_auth_header,
        cacerts=docker_registry_cacerts,
        certs=docker_registry_certs,
        docker_client=docker_client,
        docker_compose=path_docker_compose,
        endpoint=endpoint,
        htpasswd=docker_registry_htpasswd,
        password=docker_registry_password,
        images=images,
        service_name=service_name,
        ssl_context=docker_registry_ssl_context,
        username=docker_registry_username,
    )


@pytest.fixture(scope="session")
def docker_registry_ssl_context(docker_registry_cacerts: Path) -> SSLContext:
    """
    Provides an SSLContext referencing the temporary CA certificate trust store that contains the certificate of the
    secure docker registry service.
    """
    return create_default_context(cafile=str(docker_registry_cacerts))


@pytest.fixture(scope="session")
def docker_registry_username() -> str:
    """Retrieve the name of the user to use for authentication to the secure registry service."""
    return f"pytest.username.{time()}"


def _replicate_images(
    docker_client: DockerClient, endpoint: str, request
) -> List[ImageName]:
    """
    Replicates all marked images to a docker registry service at a given endpoint.

    Args:
        docker_client: Docker client with which to replicate the marked images.
        endpoint: The endpoint of the docker registry service.
        request: The pytest requests object from which to retrieve the marks.

    Returns: The list of images that were replicated.
    """
    always_pull = strtobool(str(request.config.getoption("--always-pull", True)))
    images = request.config.getoption("--push-image", [])
    # images.extend(request.node.get_closest_marker("push_image", []))

    # * Split ',' separated lists
    # * Remove duplicates - see conftest.py::pytest_collection_modifyitems()
    images = [image for i in images for image in i.split(",")]
    images = [ImageName.parse(image) for image in list(set(images))]
    for image in images:
        LOGGER.debug("- %s", image)
        try:
            replicate_image(docker_client, image, endpoint, always_pull=always_pull)
        except Exception as exception:  # pylint: disable=broad-except
            LOGGER.warning(
                "Unable to replicate image '%s': %s", image, exception, exc_info=True
            )
    return images
