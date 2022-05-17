import collections
import re
import time

import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('Solarize_Light2')

from googleapiclient.discovery import build
from textblob import TextBlob
import nltk
from wordcloud import WordCloud
from pymystem3 import Mystem
from googletrans import Translator

API_KEY = "AIzaSyDuV1ssRswKsW2uUjOWIyXWVh3sDDovBAw"

youtube = build("youtube", "v3", developerKey=API_KEY)
sw = ["br", "https", "это", "href", "youtu", "www", "com", "quot"]
nltk.download('stopwords')
translator = Translator()


def video_comments(video_id):
    video_response = youtube.commentThreads().list(part="snippet", videoId=video_id).execute()
    comments = []

    while video_response:
        for item in video_response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        if not video_response.get("nextPageToken"):
            break

        video_response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            pageToken=video_response["nextPageToken"]
        ).execute()
        time.sleep(2)

    return comments


def clean_comments(comments: list[str]) -> list[str]:
    return [re.sub(r"\W", " ", comment) for comment in comments]


def clean_stop_words(comments: list[str]) -> list[str]:
    comments = clean_comments(comments)
    return [' '.join([word for word in comment.split()
                      if word not in nltk.corpus.stopwords.words('russian')
                      and word not in nltk.corpus.stopwords.words('english')
                      and word not in sw
                      and len(word) > 1])
            for comment in comments]


def word_count(comments: list[str]):
    word_count_dict = collections.defaultdict(lambda: 0)
    for comment in comments:
        for r in comment.split():
            word_count_dict[r] += 1

    return {k: v for k, v in sorted(word_count_dict.items(), key=lambda x: x[1], reverse=True)}


def wordcloud_from_dict(d: dict):
    wc = WordCloud(
        background_color="black",
        colormap='rainbow',
        max_words=200,
        mask=None,
        width=500,
        height=500
    ).generate_from_frequencies(d)

    return wc


def lemmatize(comments: list[str]) -> list[str]:
    lem_blacklist = ["", " ", "\n"]

    result = []
    m = Mystem()
    for comment in comments:
        lemmas = m.lemmatize(comment)
        result.append(' '.join([lem for lem in lemmas if lem.strip() not in lem_blacklist]))

    return result


def get_polarity(comments: list[str]):
    respol = []
    translated_comments = translator.translate('\n'.join(comments), dest="en")
    translated_comments = translated_comments.text.lower().split('\n')
    for comment in translated_comments:
        respol.append(TextBlob(comment).sentiment.polarity)
    return respol


def get_analysis(score: int) -> str:
    if score < 0:
        return 'Ng'
    elif score == 0:
        return 'Neut'
    else:
        return 'Pos'


def get_graph(polarity_data):
    data = pd.Series(polarity_data)
    data = data.apply(get_analysis)
    # plt.tick_params(axis='both', which='major', labelsize=10, direction='in')
    plt.title('Sentiment Analysis')
    # plt.xlabel('Sentiment')
    plt.ylabel('Counts')
    data.value_counts().plot(kind='bar')
    plt.savefig("static/images/img.png")
