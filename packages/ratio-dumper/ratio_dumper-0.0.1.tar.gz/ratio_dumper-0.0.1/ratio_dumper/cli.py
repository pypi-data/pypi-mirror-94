'''
ratio_dumper - Ratio iX5M Log Dumper

MIT License

Copyright (c) 2021 Damian Zaremba

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import logging
import sys
from pathlib import Path

import click

from .driver import SerialDriver
from .utilities import convert_to_xml

logger: logging.Logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
@click.option('--debug', is_flag=True)
@click.option('--serial', default='/dev/tty.usbserial-D309VENO')
def cli(ctx: click.Context, debug: bool, serial: str) -> None:
    '''ratio-dumper - Ratio ix5M dumper.'''
    logging.basicConfig(stream=sys.stderr,
                        level=(logging.DEBUG if debug else logging.INFO),
                        format='%(asctime)-15s %(levelname)s:%(name)s:%(message)s')
    ctx.obj = {'serial_path': serial}


@cli.command()
@click.pass_context
def list(ctx: click.Context) -> None:
    '''List all stored dive ids.'''
    with SerialDriver(ctx.obj['serial_path']) as dc:
        dive_ids = dc.get_dive_ids()

    if not dive_ids:
        click.echo('No dive logs found')
        return

    click.echo('Available dive logs:')
    for dive_id in dive_ids:
        click.echo(f' - {dive_id}')


@cli.command()
@click.pass_context
@click.argument('dive_id', type=int)
def export(ctx: click.Context, dive_id: int) -> None:
    with SerialDriver(ctx.obj['serial_path']) as dc:
        dive = dc.get_dive(dive_id)
        if dive is None:
            click.echo("Failed to read dive")
            sys.exit(1)

    click.echo(convert_to_xml(dive))


@cli.command()
@click.pass_context
@click.argument('target_directory', type=click.Path(exists=True))
def download(ctx: click.Context, target_directory: str) -> None:
    with SerialDriver(ctx.obj['serial_path']) as dc:
        dive_ids = dc.get_dive_ids()
        if dive_ids is None:
            click.echo("Failed to read dive logs")
            sys.exit(1)

        if len(dive_ids) == 0:
            click.echo('No dive logs to download')
            sys.exit(0)

        click.echo('Exporting....')
        for dive_id in dive_ids:
            target_file = Path(target_directory) / f'{dive_id}.xml'
            if target_file.is_file():
                click.echo(f' - {dive_id} [skipping]')
                continue

            click.echo(f' - {dive_id}')
            dive = dc.get_dive(dive_id)
            if dive is None:
                click.echo("Failed to read dive")
                sys.exit(1)

            with open(target_file.as_posix(), 'w') as fh:
                fh.write(convert_to_xml(dive))


if __name__ == '__main__':
    cli()
