import praw
from config import REDDIT_API_CREDENTIALS

class Reddit:
    def __init__(self, submission=None):
        self.reddit = praw.Reddit(    
            client_id=REDDIT_API_CREDENTIALS['client_id'],
            client_secret=REDDIT_API_CREDENTIALS['client_secret'],
            user_agent=REDDIT_API_CREDENTIALS['user_agent'],
            username=REDDIT_API_CREDENTIALS['username'],
            password=REDDIT_API_CREDENTIALS['password']
        )