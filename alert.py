from reddit import Reddit
from db_connector import RedditDB
from twilio.rest import Client
import datetime as dt
from datetime import datetime, timedelta
import humanize
from constants import bcolor
import args as arguments
from config import (
    account_sid,
    auth_token,
    KEYWORD_PRIMARY,
    KEYWORD_SECONDARY,
    NUMBERS,
    TWILIO_NUMBER,
    THREAD,
    WEBHOOK_URL
)
import test

client = Client(account_sid, auth_token)

def get_natural_delta(created):
    float_dt = float(created)
    created_datetime = dt.datetime.fromtimestamp(int(float_dt))
    delta = dt.datetime.now() - created_datetime
    return 'Posted ' + humanize.naturaldelta(delta) + ' ago'

# Posting to a Slack channel
def send_message_to_slack(new_comments, rdb):
    from urllib import request, parse
    import json

    text = f'{len(new_comments)} new Reddit thread(s) mentioning {KEYWORD_PRIMARY} have recently been posted\n\n'
    i = 1
    for nc in new_comments:
        comment = rdb.select_comment(nc)
        text += f'{i}. "{comment[2]}"\n{get_natural_delta(comment[3])} ({comment[1]})\n\n'
        i += 1

    print(text)  

    post = {"text": "{0}".format(text)}

    try:
        json_data = json.dumps(post)
        req = request.Request(WEBHOOK_URL,
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'}) 
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))

def send_text(new_comments, rdb):

    message_body = f'-----------------------------------\n\nALERT: {len(new_comments)} new Reddit thread(s) regarding {KEYWORD_PRIMARY}\n\n'

    i = 1
    for nc in new_comments:
        comment = rdb.select_comment(nc)
        message_body += f'{i}. "{comment[2]}"\n{comment[1]}\n{get_natural_delta(comment[3])}\n\n'
        i += 1

    print(message_body)   

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
        if KEYWORD_SECONDARY in ns.title.lower():
            if not rdb.comment_exists(ns.id):
                ns.comments.replace_more(limit=0)
                for c in ns.comments.list():
                    if KEYWORD_PRIMARY in c.body.lower():
                        new_comm = rdb.create_comment(comment)
                        new_comments.append(ns.id)
        elif KEYWORD_PRIMARY in ns.title.lower(): 
            if not rdb.comment_exists(ns.id):
                new_comm = rdb.create_comment(comment)
                new_comments.append(ns.id)

    return new_comments

def main():
    # get command line arguments
    args = arguments.arg_parser()

    # init reddit instance and connect to local sqlite3 db
    r = Reddit()
    rdb = RedditDB()

    # get latest 100 reddit posts from the subreddit
    new_comments = get_new_comments(r, rdb)

    # run tests
    if args.tests == True:
        if args.specify_test:
            test_num = args.specify_test
            if test_num == 1:
                test.t__get_submissions(r)
            elif test_num == 2:
                test.t__send_text(r, client)
            elif test_num == 3:
                test.t__send_message_to_slack(r)
            elif test_num == 4:
                test.t__check_for_new_submissions(new_comments, rdb)
        else:
            test.t__get_submissions(r)
            test.t__send_text(r, client)
            test.t__send_message_to_slack(r)
            test.t__check_for_new_submissions(new_comments, rdb)
        return

    # grab latests posts from the subreddit
    elif len(new_comments):

        # only notify slack
        if args.slack and not args.phone:
            send_message_to_slack(new_comments, rdb) 

        # only notify phones
        elif args.phone and not args.slack:
            send_text(new_comments, rdb)

        # notify slack and text recipients
        else:
            send_text(new_comments, rdb)
            send_message_to_slack(new_comments, rdb) 
            
    # no new comments
    else:
        print(bcolor.get_color('red', '\nNo new posts.\n'))

if __name__ == '__main__':
    main()