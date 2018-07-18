""" Miscellaneous helper functions.
"""
from os import path, getcwd
from secrets import *
import tweepy


def get_twitter_api():
    """ Use secrets to authenticate twitter API access. """
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    return tweepy.API(auth)


def get_path_to(filename):
    """ Get the path to a file by filename in the present directory.

    :param filename: The name of the file in the present directory.
    :type filename: str
    :return: The full path to the file.
    :rtype: str
    """
    dir = path.realpath(path.join(getcwd(), path.dirname(__file__)))
    return path.join(dir, filename)


def no_banned_words(poem_text):
    """ Verify poem does not contain slurs.

    :param poem_text: Text of poem to be checked for banned terms.
    :type poem_text: str
    :return: Whether input is free of banned terms.
    :rtype: Boolean
    """
    banned_words_file = open(get_path_to(BANNED_WORDS_FILE), 'r')

    for rawline in banned_words_file:
        line = rawline.rstrip()

        if poem_text.find(line) != -1:
            # Poem contains banned word.
            return False

    return True
