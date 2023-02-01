import subprocess
import time
from typing import List

import docker
import pytest

from embedding_store.jina import JinaEmbeddingStore
from embedding_store.torch import TorchEmbeddingStore

JINA_EMBEDDING_STORE_GRPC = "grpc://0.0.0.0:54321"
JINA_DOCKER_COMPOSE_FILE = "embedding_models/jina/docker-compose.yml"


class DockerComposeFlow:

    healthy_status = "healthy"
    unhealthy_status = "unhealthy"

    def __init__(self, dump_path, timeout_second=30):
        self.dump_path = dump_path
        self.timeout_second = timeout_second

    def __enter__(self):
        subprocess.run(f"docker-compose -f {self.dump_path} up --build -d --remove-orphans".split(" "))

        container_ids = (
            subprocess.run(f"docker-compose -f {self.dump_path} ps -q".split(" "), capture_output=True)
            .stdout.decode("utf-8")
            .split("\n")
        )
        container_ids.remove("")  # remove empty  return line

        if not container_ids:
            raise RuntimeError("docker-compose ps did not detect any launch container")

        client = docker.from_env()

        init_time = time.time()
        healthy = False

        while time.time() - init_time < self.timeout_second:
            if self._are_all_container_healthy(container_ids, client):
                healthy = True
                break
            time.sleep(0.1)

        if not healthy:
            raise RuntimeError("Docker containers are not healthy")

    @staticmethod
    def _are_all_container_healthy(container_ids: List[str], client: docker.client.DockerClient) -> bool:

        for id_ in container_ids:
            status = client.containers.get(id_).attrs["State"]["Health"]["Status"]

            if status != DockerComposeFlow.healthy_status:
                return False
        return True

    def __exit__(self, exc_type, exc_val, exc_tb):
        subprocess.run(f"docker-compose -f {self.dump_path} down --remove-orphans".split(" "))


@pytest.fixture(params=["jira_embedding_store"])
def embedding_store(request):
    if request.param == "jira_embedding_store":
        with DockerComposeFlow(JINA_DOCKER_COMPOSE_FILE):
            selected_embedding_store = JinaEmbeddingStore(embedding_grpc=JINA_EMBEDDING_STORE_GRPC)
            yield selected_embedding_store
    elif request.param == "torch_embedding_store":
        selected_embedding_store = TorchEmbeddingStore()
        yield selected_embedding_store

    else:
        raise ValueError("Not defined embedding store.")
