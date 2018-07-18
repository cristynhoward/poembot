""" First attempt to work with random poem API.
"""
from langdetect import detect
from secrets import *
import requests
import tweepy


def get_twitter_api():
    """ Use secrets to authenticate twitter API access. """
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    return tweepy.API(auth)


def main():
    """

    :return:
    :rtype:
    """
    count = 1
    while count > 0:

        url = 'https://www.poemist.com/api/v1/randompoems'
        r = requests.get(url)
        json = r.json()

        for i in range(0, len(json)):
            poem = json[i]

            if detect(poem['content']) == 'en' and count > 0:

                poem_thread = tweet_threadify(poem['content'])
                if poem_thread is not None:

                    api = get_twitter_api()

                    head_text = poem['title'] + '\n' + \
                                'Written by ' + poem['poet']['name'] + '.'

                    last_tweet = api.update_status(head_text)
                    print('Tweeted:\n'+head_text)

                    for j in range(0, len(poem_thread)):
                        tweet = api.update_status(poem_thread[j], last_tweet.id)
                        last_tweet = tweet

                    count -= 1


def tweet_threadify(poem_text):
    """ Attempts to cleanly break up poem into sequence of tweet-sized chunks.

    :param poem_text:
    :type poem_text:
    :return: Poem as sequence of tweet-sized chunks, or False iff:
    poem thread contains stansas that are too large with no clear split point,
    [poem thread would be longer than 10 tweets?].
    :rtype: list, Boolean
    """
    stansas = poem_text.split('\n\n')
    to_trim = 0
    for i in range(0, len(stansas)):

        if len(stansas[i]) > 280:
            # TODO : How do we detect where natural breaks occur in the linguistic patterns of poems?
            # TODO : Possible split chars include ; .
            return None

        if i+1 < len(stansas) and len(stansas[i]) <= 135 and len(stansas[i+1]) <= 135:
            # Put two stansas into one tweet.
            combined_stansa = stansas[i] + '\n\n' + stansas[i+1]
            # Replace first tweet.
            stansas[i] = combined_stansa
            # Shift forward all other stansas.
            for j in range(i+1, len(stansas)-1):
                stansas[j] = stansas[j+1]
            to_trim += 1

    for i in range(0, to_trim):
        stansas.pop()

    return stansas


if __name__ == '__main__':
    main()
