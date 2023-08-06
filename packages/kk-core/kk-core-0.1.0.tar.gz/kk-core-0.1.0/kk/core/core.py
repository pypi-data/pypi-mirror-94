import typer

app = typer.Typer(short_help="This is the core command")
name = "core"

@app.command()
def core_command1():
    typer.secho("core_command1")

@app.command()
def core_command2():
    typer.secho("core_command2")
