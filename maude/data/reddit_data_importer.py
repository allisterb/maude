from logging import info, error, warn, debug

import praw
from praw.models import SubredditHelper, Submission, Comment

import maude_global

from base.runtime import serialize_to_json
from base.timer import begin
from core.data_importer import DataImporter

class DataImporter(DataImporter):
    """Import submission, comment and image data from Reddit."""

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
        """Import Reddit data using the parameters specified"""
        
        debug(f'Import args are: {args}')
        subreddit_name:str = args[0]
        sort:str = args[1]
        submission_limit:int = args[2]
        comment_limit:int = args[3]
        time_filter:str = args[4]
        subreddit:SubredditHelper = self.reddit.subreddit(subreddit_name)
        submissions:list[Submission] = []
        comments:dict[str, list[Comment]] = {}
        
        with begin(f'Fetching data for {submission_limit} {sort} submission(s)') as op:
            submissions = subreddit.top(time_filter, limit=submission_limit) if sort == 'top' else subreddit.hot(limit=submission_limit) if sort == 'hot' else subreddit.new(limit=submission_limit)
            for submission in submissions:
                if maude_global.KBINPUT:
                    op.abandon()
                    return
                submission.comments.replace_more(limit=None)
                comments[submission.title] = submission.comments.list()
            op.complete()

        print(serialize_to_json(c.body for c in comments))
        