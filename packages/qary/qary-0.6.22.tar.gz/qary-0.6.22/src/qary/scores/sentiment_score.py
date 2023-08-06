from nltk.sentiment.vader import SentimentIntensityAnalyzer


def score(reply, stmt=None, **kwargs):
    if kwargs is None:
        kwargs = {}
    sentiment_analyzer = kwargs.get('sentiment_analyzer', SentimentIntensityAnalyzer())

    return (sentiment_analyzer.polarity_scores(reply)['compound'] + 1) / 2.0
