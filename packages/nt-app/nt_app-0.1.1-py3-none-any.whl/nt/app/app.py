import typer
from nt.app import subcommand


def app():
    print("Hello from nt-app.nt.app")

app = typer.Typer(help="This is nt-app.app's app!")
app.add_typer(subcommand.app, name="subcommand")

if __name__ == "__main__":
    app()
