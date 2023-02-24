import typer
from rich.console import Console
from rich.table import Table
from model import Todo
from database import get_all_todos, delete_todo, insert_todo, match_todo, update_todo

console = Console()

app = typer.Typer()


@app.command(short_help='adds an item')
def add(namespace: str, deploy: str, version: str):
    typer.echo(f"adding {namespace}, {deploy}, {version}")
    todo = Todo(namespace, deploy, version)
    insert_todo(todo)
    show()

@app.command()
def delete(position: int):
    typer.echo(f"deleting {position}")
    # indices in UI begin at 1, but in database at 0
    delete_todo(position-1)
    show()

@app.command()
def update(position: int, namespace: str = None, deploy: str = None, version: str = None):
    typer.echo(f"updating {position}")
    update_todo(position-1, namespace, deploy, version)
    show()

@app.command()
def match(position: int):
    typer.echo(f"match {position}")
    match_todo(position-1)
    show()

@app.command()
def show():
    deploys = get_all_todos()
    console.print("[bold magenta]Todos[/bold magenta]!", "💻")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Namespace", min_width=20)
    table.add_column("Deployment", min_width=20)
    table.add_column("Version", min_width=12, justify="right")
    table.add_column("Match", min_width=12, justify="right")

    def get_version_color(version):
        COLORS = {'Learn': 'cyan', 'YouTube': 'red', 'Sports': 'cyan', 'Study': 'green'}
        if version in COLORS:
            return COLORS[version]
        return 'white'

    for idx, deploy in enumerate(deploys, start=1):
        c = get_version_color(deploy.version)
        is_done_str = '✅' if deploy.status == 2 else '❌'
        table.add_row(str(idx), deploy.namespace, deploy.deploy, f'[{c}]{deploy.version}[/{c}]', is_done_str)
    console.print(table)


if __name__ == "__main__":
    app()