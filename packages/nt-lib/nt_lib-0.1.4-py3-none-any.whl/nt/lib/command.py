import typer

app = typer.Typer(short_help="This is the main command")
name = "lib"

@app.command()
def main1():
    print("IN MAIN_1")

@app.command()
def main2():
    print("IN MAIN_2")
