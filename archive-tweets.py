#!/usr/local/bin/python

import tweepy
import pytz
import os

# Parameters.
accounts = ['account1', 'account2'] # Add accounts to this list to archive multiple accounts
tweetdir = os.environ['HOME'] + '/Dropbox/Backups/twitter/'
datefmt = '%B %d, %Y at %I:%M %p'
homeTZ = pytz.timezone('US/Central')
utc = pytz.utc

def setup_api():
  """Authorize the use of the Twitter API."""
  a = {}
  with open(os.environ['HOME'] + '/.twitter-credentials') as credentials:
    for line in credentials:
      k, v = line.split(': ')
      a[k] = v.strip()
  auth = tweepy.OAuthHandler(a['consumerKey'], a['consumerSecret'])
  auth.set_access_token(a['token'], a['tokenSecret'])
  return tweepy.API(auth)

# Authorize.
api = setup_api()

for account in accounts:
  urlprefix = 'http://twitter.com/%s/status/' % account
  tweetfile = tweetdir + '%s_twitter.txt' % account
  idfile = tweetdir + '%s_lastID.txt' % account

  # Get the ID of the last downloaded tweet.
  with open(idfile, 'r') as f:
    lastID = f.read().rstrip()

  # Collect all the tweets since the last one.
  tweets = api.user_timeline(account, since_id=lastID, count=200, include_rts=True)

  # Write them out to the twitter.txt file.
  with open(tweetfile, 'a') as f:
      for t in reversed(tweets):
        ts = utc.localize(t.created_at).astimezone(homeTZ)
        lines = ['',
                 t.text,
                 ts.strftime(datefmt),
                 urlprefix + t.id_str,
                 '- - - - -',
                 '']
        f.write('\n'.join(lines).encode('utf8'))
        lastID = t.id_str

  # Update the ID of the last downloaded tweet.
  with open(idfile, 'w') as f:
    lastID = f.write(lastID)
