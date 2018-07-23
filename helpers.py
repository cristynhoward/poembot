""" Miscellaneous helper functions.
"""
from os import path, getcwd
from time import strftime, gmtime
from secrets import *
import tweepy, requests


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


def log(message):
    """ Log a message in the bot log file.

    :param message: The message to be recorded.
    :type message: str
    :return: None
    :rtype: None
    """
    print(message)
    day = strftime("%d_%b_%Y", gmtime())
    with open(path.join(get_path_to("logs/" + day + ".log")), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


def valid_lang(lang):
    """ Checks if language is one that can be processed.

    :param lang: The code identifying the language.
    :type lang: str
    :return: Whether lang is a vlaid language.
    :rtype: Boolean
    """
    valid_langs = ["ar", "cs", "da", "de",  "en", "eo", "es", "fa", "fi", "fr", "hi", "hu", "it", "ja", "ko", "nl",
                   "no", "pl", "pt", "ru", "sv", "th", "tr", "zh"]
    return lang in valid_langs


def no_bad_words(text, lang):
    """ Verify that text does not contain any slurs.

    :param text: The text to be checked for slurs.
    :type text: str
    :param lang: The language code of the text.
    :type lang: str
    :return: Whether the text is free of slurs.
    :rtype: Boolean
    """
    if valid_lang(lang):
        url = 'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/'\
              + lang
        r = requests.get(url)
        slurs = r.content.decode().split('\n')
        for slur in slurs:
            if slur != "" and text.find(slur) != -1:
                # Text contains slur.
                return False
        return True
