import typer

import embestore.cli.serve as serve

app = typer.Typer()
app.add_typer(serve.app, name="serve", help="Serve the model in docker container.")


if __name__ == "__main__":
    app()
