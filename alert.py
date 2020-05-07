from config import ( 
    account_sid,
    auth_token,
    NUMBERS, 
    THREAD,
    TWILIO_NUMBER,
)
import datetime as dt
from datetime import datetime, timedelta
from db_connector import RedditDB
import humanize
from reddit import Reddit
from twilio.rest import Client

client = Client(account_sid, auth_token)

def get_natural_delta(created):
    """
    Format timestamp post created
    """
    float_dt = float(created)
    created_datetime = dt.datetime.fromtimestamp(int(float_dt))
    delta = dt.datetime.now() - created_datetime
    return 'Posted ' + humanize.naturaldelta(delta) + ' ago'

def send_text(new_comments, rdb):
    message_body = '-----------------------------------\n\nALERT: New Reddit thread(s) regarding <YOUR_SEARCH_QUERY>\n\n'

    i = 1
    for nc in new_comments:
        comment = rdb.select_comment(nc)
        message_body += f'{i}. "{comment[2]}"\n{comment[1]}\n{get_natural_delta(comment[3])}\n\n'
        i += 1

    for number in NUMBERS:
        client.messages.create(
            from_=TWILIO_NUMBER,
            to=number,
            body=message_body
        )

def get_new_comments(r, rdb):
    new_submissions = r.reddit.subreddit(THREAD).new()

    new_comments = []
    for ns in new_submissions:
        comment = (ns.id, ns.shortlink, ns.title, ns.created_utc)
        if '<THREAD_WHOSE_COMMENTS_MIGHT_CONTAIN_KEYWORD>' in ns.title.lower():
            if not rdb.comment_exists(ns.id):
                ns.comments.replace_more(limit=0)
                for c in ns.comments.list():
                    if '<KEYWORD_TO_MONITOR>' in c.body.lower():
                        new_comm = rdb.create_comment(comment)
                        new_comments.append(ns.id)
        elif '<KEYWORD_TO_MONITOR>' in ns.title.lower(): 
            if not rdb.comment_exists(ns.id):
                new_comm = rdb.create_comment(comment)
                new_comments.append(ns.id)
                
    return new_comments

def main():
    r = Reddit()
    rdb = RedditDB()
    
    new_comments = get_new_comments(r, rdb)
    if len(new_comments):
        send_text(new_comments, rdb)

if __name__ == '__main__':
    main()