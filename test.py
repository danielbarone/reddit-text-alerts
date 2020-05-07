from config import (
    KEYWORD_PRIMARY,
    NUMBERS, 
    PERSONAL_MOBILE_NUM, 
    TEST_WEBHOOK_URL, 
    THREAD, 
    TWILIO_NUMBER
)
from constants import bcolor
import datetime as dt 
from datetime import datetime, timedelta
import humanize

def print_test(num, desc):
        test_header = f'Test {num}: {desc}'
        div1 = '\n============================================'
        div2 = '--------------------------------------------'
        print(bcolor.get_color('green', div1))
        print(bcolor.get_color('green', test_header))
        print(bcolor.get_color('green', div2))

def get_natural_delta(created):
    float_dt = float(created)
    created_datetime = dt.datetime.fromtimestamp(int(float_dt))
    delta = dt.datetime.now() - created_datetime
    return 'Posted ' + humanize.naturaldelta(delta) + ' ago'

# Test 1
def t__get_submissions(r):
    print_test(1, 't__get_submissions()')
    new_submissions = r.reddit.subreddit(THREAD).new()
    i = 1
    for ns in new_submissions:
        print(f'{i}: {ns.title}')
        i += 1

# Test 2
def t__send_text(r, client):
    print_test(2, 't__send_text()')
    new_submissions = r.reddit.subreddit(THREAD).new()
    test_submission = None

    i = 0
    for ns in new_submissions:
        if i == 1:
            break
        test_submission = ns
        i += 1

    message_body = f'-----------------------------------\n\nALERT: 1 new Reddit thread by {test_submission.author.name}\n\n'
    message_body += f'{i}. "{test_submission.title}"\n{test_submission.shortlink}\n{get_natural_delta(test_submission.created_utc)}\n\n'

    print(message_body)   

    client.messages.create(
        from_=TWILIO_NUMBER,
        to=PERSONAL_MOBILE_NUM,
        body=message_body
    )

# Test 3
def t__send_message_to_slack(r):
    from urllib import request, parse
    import json
    print_test(3, 't__send_message_to_slack()')
    new_submissions = r.reddit.subreddit(THREAD).new()
    test_submission = None

    i = 0
    for ns in new_submissions:
        if i == 1:
            break
        test_submission = ns
        i += 1

    text = f'1 new Reddit thread by {test_submission.author.name}\n\n'
    text += f'{i}. "{test_submission.title}"\n{get_natural_delta(test_submission.created_utc)} ({test_submission.shortlink})\n\n'

    print(text)   

    post = {"text": "{0}".format(text)}

    try:
        json_data = json.dumps(post)
        req = request.Request(TEST_WEBHOOK_URL,
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'}) 
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))

# Test 4
def t__check_for_new_submissions(new_comments, rdb):
    print_test(4, 't__check_for_new_submissions()')
    message_body = f'\n\nALERT: {len(new_comments)} new Reddit thread(s) regarding {KEYWORD_PRIMARY}\n\n'

    i = 1
    for nc in new_comments:
        comment = rdb.select_comment(nc)
        message_body += f'{i}. "{comment[2]}"\n{comment[1]}\n{get_natural_delta(comment[3])}\n\n'
        i += 1

    print(message_body)   