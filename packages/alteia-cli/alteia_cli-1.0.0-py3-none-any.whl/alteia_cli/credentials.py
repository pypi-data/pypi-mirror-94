import json
from pathlib import Path

import typer
from alteia.core.errors import ResponseError
from tabulate import tabulate

from alteia_cli import utils
from alteia_cli.sdk import alteia_sdk

app = typer.Typer()


@app.command(name='create')
def create(
        filepath: Path = typer.Option(
        ...,   # '...' in typer.Option() makes the option required
        exists=True,
        readable=True,
        help='Path of the Credential JSON file')):
    """ Create a new credential entry """

    sdk = alteia_sdk()
    credentials_list = json.load(open(filepath))
    if not isinstance(credentials_list, list):
        credentials_list = [credentials_list]
    for cred in credentials_list:
        found_cred = sdk.credentials.search(
            name=cred.get('name'),
            return_total=True
        )
        if found_cred.total >= 1:
            typer.secho(
                '✖ Cannot create a credential entry with the name {!r}. '
                'One already exists on {}'.format(
                    cred.get('name'), sdk._connection._base_url
                ),
                fg=typer.colors.RED
            )
            raise typer.Exit(2)

        try:
            created_cred = sdk.credentials.create(
                name=cred['name'],
                credentials=cred['credentials']
            )
            typer.secho('✓ Credentials created successfully', fg=typer.colors.GREEN)
            return created_cred
        except Exception as ex:
            print('Impossible to save {} with error {}'.format(cred['name'], ex))
            raise typer.Exit(code=1)


@app.command(name='list')
def list_credentials():
    """ List the existing credentials """
    sdk = alteia_sdk()
    with utils.spinner():
        results = sdk.credentials.search(filter={})
    if len(results) > 0:
        table = {
            'Credentials name': [
                typer.style(r.name, fg=typer.colors.GREEN, bold=True)
                for r in results
            ],
        }
    print(tabulate(
        table,
        headers='keys',
        tablefmt='pretty',
        colalign=['left'])
    )

    print()


@app.command(name='delete')
def delete_credentials(
        name: str = typer.Argument(...)):
    """ Delete a credential entry by its name"""
    sdk = alteia_sdk()
    found_cred = sdk.credentials.search(
        name=name,
        return_total=True
    )
    if found_cred.total < 1:
        typer.secho(
            '✖ Credential {!r} not found on {!r}'.format(
                name, sdk._connection._base_url
            ),
            fg=typer.colors.RED
        )
        raise typer.Exit(2)

    try:
        sdk.credentials.delete(found_cred.results[0].id)
    except ResponseError as e:
        typer.secho(
            '✖ Cannot delete the credentials {!r}'.format(name),
            fg=typer.colors.RED
        )
        typer.secho('details: {}'.format(str(e)), fg=typer.colors.RED)
        raise typer.Exit(2)

    typer.secho(
        '✓ Credentials {!r} deleted successfully'.format(name),
        fg=typer.colors.GREEN
    )


if __name__ == "__main__":
    app()
