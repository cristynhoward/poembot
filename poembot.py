""" First attempt to work with random poem API.
"""
from langdetect import detect
from helpers import *
import requests


def main():
    """ Access API point, find tweetable poem, and tweet it.
    """
    count = 1
    while count > 0:
        log("Attempting to access poem API.")
        url = 'https://www.poemist.com/api/v1/randompoems'
        r = requests.get(url)
        json = r.json()

        for i in range(0, len(json)):
            poem = json[i]
            poem_lang = detect(poem['content'])

            if count > 0 and valid_lang(poem_lang) and no_bad_words(poem['content'], poem_lang):

                poem_thread = tweet_threadify(poem['content'])
                if poem_thread is not None and len(poem_thread) < 6:

                    api = get_twitter_api()

                    head_text = poem['title'] + '\n' + 'Written by ' + poem['poet']['name'] + '.\n'
                    if len(poem_thread) == 1:
                        head_text = head_text + '#micropoetry #poetry #poem #poet #mpy'
                    else:
                        head_text = head_text + '#poetry #poem #poet'

                    last_tweet = api.update_status(head_text)

                    for j in range(0, len(poem_thread)):
                        tweet = api.update_status(poem_thread[j], last_tweet.id)
                        last_tweet = tweet

                    print('Tweeted:\n' + head_text)
                    count -= 1


def tweet_threadify(poem_text):
    """ Attempts to cleanly break up poem into sequence of tweet-sized chunks.

    :param poem_text: Text to be broken up into tweet-sized chunks.
    :type poem_text: str
    :return: Poem as sequence of tweet-sized chunks, or None iff poem thread
        contains stansas that are too large with no clear split point.
    :rtype: list, None
    """
    stansas = poem_text.split('\n\n')
    for i in range(0, len(stansas)):
        if len(stansas[i]) > 280:
            # TODO : How do we detect where natural breaks occur in the linguistic patterns of poems?
            # TODO : Possible split chars include ; .
            return None
    return stansas


if __name__ == '__main__':
    main()
