import typer

app = typer.Typer(short_help="This is plugin1")
name = "plugin1"

@app.command()
def plugin1_command1():
    print("plugin1_command1")

@app.command()
def plugin1_command2():
    print("plugin1_command2")

if __name__ == "__main__":
    app()
