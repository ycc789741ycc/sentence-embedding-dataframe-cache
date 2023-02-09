import subprocess

import typer

JINA_DOCKER_COMPOSE_FILE = "embedding_models/jina/docker-compose.yml"


app = typer.Typer(help="Serve the model in docker container.")


@app.command(name="start-jina", help="Start the embedding model in jina flow with docker container")
def start_jina():
    subprocess.run(f"docker-compose -f {JINA_DOCKER_COMPOSE_FILE} up --build -d".split(" "))


@app.command(name="stop-jina", help="Stop the embedding model in jina flow with docker container")
def stop_jina():
    subprocess.run(f"docker-compose -f {JINA_DOCKER_COMPOSE_FILE} down".split(" "))
