import typer
from nt.app import subcommand


def app():
    print("Hello from nt-app.nt.app")

app = typer.Typer(help="This is nt-app.app's app!")
name = "app-command"
app.add_typer(subcommand.app, name=name)

if __name__ == "__main__":
    app()
