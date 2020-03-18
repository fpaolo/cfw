import re
def match_tweets_hashtags(tweets, hashtags):
    """ Match tweets by hashtags 

        Matches are not case-sensitive and occur if
        at least one tweet hashtag is in hashtags

        Parameters
        ----------
        tweets : a list of objs of class Tweet
        hashtags : a list of hashtags [#htag1, #htag2, ...]

        Returns
        -------
        tweets_ok : a list of objs of class Tweet with matched hashtag
    """
    tweets_ok = []
    hashtags = [h.lower() for h in hashtags]
    for t in tweets:
        t_hashtags = t.hashtags.split(" ")
        t_hashtags = set([h.lower() for h in t_hashtags])
        if len(t_hashtags.intersection(hashtags)) > 0:
            tweets_ok.append(t)
    return tweets_ok


def is_match(string, patterns):
    """ Find if any pattern in patterns is in string.
        Matches are not case-sensitive.

        Parameters
        ----------
        string : str
        patterns : list, patterns to be matched

        Returns
        -------
        bool
    """
    # warning! re.match matches only at BEGINNING of string -> use re.search
    matches = [re.search(p, string, re.IGNORECASE) for p in patterns]
    is_match = [m is not None for m in matches]
    return any(is_match)

def match_tweet_text(tweets, patterns):
    """ Match tweets by text 

        Matches are not case-sensitive and occur if
        any patter in patterns is found in tweet text

        Parameters
        ----------
        tweets : a list of objs of class Tweet
        patterns : a list of re patterns

        Returns
        -------
        a list of matched objs of class Tweet 
    """
    matches = [is_match(t.text, patterns) for t in tweets]
    return [t for t, m in zip(tweets, matches) if m]
