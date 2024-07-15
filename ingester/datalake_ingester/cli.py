import click
from datalake.common.conf import load_config
from .ingester import Ingester
from .log import log_debugger


DEFAULT_CONFIG = '/etc/datalake-ingester.env'


@click.group(invoke_without_command=True)
@click.version_option()
@click.option('-c', '--config',
              help='config file. The format is just a dotenv file')
@click.option('-t', '--dynamodb-table',
              help='dynamodb table in which to store datalake records.')
@click.option('-r', '--aws-region',
              help='region to use for aws services (e.g., s3, dynamodb)')
@click.option('-k', '--report-key',
              help='key under which reports should be published.')
@click.option('-s', '--aws-s3-host',
              help='AWS s3 host (e.g., s3-us-gov-west-1.amazonaws.com)')
@click.option('-q', '--queue',
              help='name of the ingestion queue (e.g., datalake-sqs)')
@click.pass_context
def cli(ctx, **kwargs):
    conf = kwargs.pop('config')
    log_debugger(None, "datalake_ingester:cli.py before load_config", loc='datalake_ingester:cli.py:cli')
    load_config(conf, DEFAULT_CONFIG, **kwargs)
    log_debugger(None, "datalake_ingester:cli.py AFTER load_config", loc='datalake_ingester:cli.py:cli')


def _subcommand_or_fail(ctx):
    if ctx.invoked_subcommand is None:
        ctx.fail('Please specify a command.')


@cli.command()
def listen():
    log_debugger(None, "datalake_ingester:listen.py before instantiating Ingester", loc='datalake_ingester:cli.py:listen')
    i = Ingester.from_config()
    i.listen()
    log_debugger(None, f"datalake_ingester:listen.py AFTER instantiating Ingester: {i}", loc='datalake_ingester:cli.py:listen')

