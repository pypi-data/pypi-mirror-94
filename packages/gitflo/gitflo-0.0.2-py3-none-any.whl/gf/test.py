import git
import typer
from git.exc import GitCommandError

app = typer.Typer()


def ntb(f):
    """block out python traceback message"""
    def _wapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except GitCommandError as e:
            typer.echo(e)
    return _wapper


@app.command()
def test_git():
    repo = git.Repo()
    heads= repo.heads
    test = heads.test
    ntb(repo.git.checkout)('test')

repo = git.Repo()
idx = repo.index
breakpoint()