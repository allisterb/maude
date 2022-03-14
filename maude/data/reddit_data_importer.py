from logging import info, error, warn, debug

import praw
from praw.models import SubredditHelper
from base.timer import begin
from core.data_importer import DataImporter

class DataImporter(DataImporter):
    """Import topic, comment and image data from Reddit."""

    def __init__(self, client_id, client_secret, client_user, client_pass, args=[]):
        self.client_id=client_id
        self.client_secret=client_secret
        self.client_user = client_user
        self.client_pass=client_pass
        self.args = args
        info(f'Reddit client id is {self.client_id}. Reddit client user is {self.client_user}.')
        self.reddit = praw.Reddit(
            user_agent="maude by u/allisterb",
            client_id=self.client_id,
            client_secret=self.client_secret,
            username=self.client_user,
            password=self.client_pass
        )

    def get_importer_info(self):
        pass
    
    def import_data(self, *args):
        """Import data using the parameters specified in the DataImport constructor"""
        debug(f'Import args are: {args}')
        subreddit_name = args[0]
        sort = args[1]
        time_filter = args[2]
        submission_limit = args[3]
        subreddit:SubredditHelper = self.reddit.subreddit(subreddit_name)
        submissions = []
        with begin("Fetching submissions") as op:
            submissions = subreddit.top(time_filter, limit=submission_limit) if sort == 'top' else subreddit.hot(limit=submission_limit) if sort == 'hot' else subreddit.new(time_filter, limit=submission_limit)
            op.complete()
        for submission in submissions:
            print(submission.title)

        

         



    