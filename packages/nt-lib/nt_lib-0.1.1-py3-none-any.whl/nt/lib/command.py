import typer

app = typer.Typer(short_help="This is the main command")

@app.command("main")
def main():
    print("IN MAIN")
