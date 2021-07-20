import glob
import ntpath
import os
import sys
from pathlib import Path

import typer

app = typer.Typer()


def read_and_wite(in_file: str, out_file: str) -> None:
    with open(in_file, "r") as f:
        data = f.read()
        with open(out_file, "w") as of:
            of.write(data)


@app.command()
def create(filename: str, tag: str) -> None:
    """Create a new tag from the file provided"""

    # create the tag folder if not exists
    Path("./.tag").mkdir(exist_ok=True)
    if Path(filename).is_file():
        files = [ntpath.basename(i) for i in glob.glob("./.tag/*")]
        file_w_tag = f"{ntpath.basename(filename)}.v{tag.replace('.', '_')}"

        if file_w_tag in files:
            typer.echo("The file with the tag exist", file=sys.stderr)
            raise typer.Exit(1)

        else:
            read_and_wite(filename, os.path.join("./.tag", file_w_tag))
            typer.echo(f"Version tag for the file {filename!r} with the tag {tag!r} created successfully.",
                       file=sys.stdout)
            typer.Exit(0)

    else:
        typer.echo(f"The file {filename} does not exists.", file=sys.stderr)
        raise typer.Exit(1)


@app.command()
def pull(filename: str, tag: str, outfile: str = typer.Option(
        "",
        help="The file to put the contents of the file with the specified version.",
        show_default=False)) -> None:
    """Pull a file with the specified tag to the root directory"""

    file_w_tag = f"{ntpath.basename(filename)}.v{tag.replace('.', '_')}"
    outfile = outfile or filename
    files = [ntpath.basename(i) for i in glob.glob("./.tag/*")]

    if file_w_tag not in files:
        typer.echo("The file with the specified tag does not exists",
                   file=sys.stderr)
        raise typer.Exit(1)

    else:
        read_and_wite(os.path.join("./.tag", file_w_tag), outfile)


@app.command()
def delete(filename: str, tag: str = typer.Option("", help="The specific tag to delete.", show_default=False)) -> None:
    """Delete a specific tagged file"""

    files = [i for i in glob.glob("./.tag/*")]
    files = [i for i in files if filename in i]

    if not files:
        typer.echo("No such file exists", file=sys.stderr)
        typer.Exit(1)

    if tag:
        file_w_tag = f"{filename}.v{tag.replace('.', '_')}"

        if file_w_tag in [ntpath.basename(i) for i in files]:
            os.remove(os.path.join("./.tag", file_w_tag))
            typer.Exit(0)

        else:
            typer.echo(
                "The specific tag for the file does not exist.", file=sys.stderr)
            typer.Exit(1)

    else:
        for _file in files:
            os.remove(_file)
        typer.Exit(0)


@app.command()
def ls(filename: str = typer.Option("", help="The name of the file to view the tags.", show_default=False)) -> None:
    """List all the tagged file. --filename is provided, then lists only the tags of that file"""

    files = [ntpath.basename(i) for i in glob.glob("./.tag/*")]

    if filename:
        files = [i for i in files if filename in i]

    typer.echo("\n".join(files), file=sys.stdout)
    typer.Exit(0)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
