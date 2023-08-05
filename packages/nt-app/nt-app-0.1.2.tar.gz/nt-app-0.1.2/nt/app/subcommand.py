import typer

app = typer.Typer(short_help="This is a subcommand")

@app.command("about")
def about():
    print("IN ABOUT")
