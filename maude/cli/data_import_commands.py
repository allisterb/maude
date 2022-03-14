import click

from cli.commands import data_import
from cli.util import *

@data_import.command('reddit')
@click.argument('subreddit', required = True)
@click.argument('sort', required = False, type=click.Choice(['hot', 'top', 'new'], case_sensitive=False), default = 'hot')
@click.argument('submission_limit', required = False, type=int, default = 100)
@click.argument('comment_limit', required = False, type=int, default = 1000)
@click.argument('time_filter', required = False, type=click.Choice(['hour', 'year', 'all', 'week', 'month', 'day'], case_sensitive=False), default = 'all')
@click.argument('client_id', envvar='MAUDE_REDDIT_CLIENT_ID')
@click.argument('client_secret', envvar='MAUDE_REDDIT_CLIENT_SECRET')
@click.argument('client_user', envvar='MAUDE_REDDIT_CLIENT_USER')
@click.argument('client_pass', envvar='MAUDE_REDDIT_CLIENT_PASS')
def data_import_reddit(subreddit, sort, submission_limit, comment_limit, time_filter, client_id, client_secret, client_user, client_pass):
   from data.reddit_data_importer import DataImporter
   importer = DataImporter(client_id, client_secret, client_user, client_pass)
   importer.import_data(subreddit, sort, submission_limit, comment_limit, time_filter)
