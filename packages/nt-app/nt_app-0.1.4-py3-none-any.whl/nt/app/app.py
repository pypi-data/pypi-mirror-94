import typer

app = typer.Typer(help="This is nt-app.app's app!")
name = "app"


@app.command("about")
def about():
    print("IN ABOUT")



if __name__ == "__main__":
    app()
