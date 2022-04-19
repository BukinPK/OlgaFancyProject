import collections
import re
import time

from googleapiclient.discovery import build
from wordcloud import WordCloud
from pymystem3 import Mystem

API_KEY = "AIzaSyDuV1ssRswKsW2uUjOWIyXWVh3sDDovBAw"
VIDEO_ID = "uaX3X3AF6Gw"

youtube = build("youtube", "v3", developerKey=API_KEY)


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


def word_count(comments: list[str]):
    word_count_dict = collections.defaultdict(lambda: 0)
    for comment in comments:
        for r in comment.split():
            word_count_dict[r] += 1

    return {k: v for k, v in sorted(word_count_dict.items(), key=lambda x: x[1], reverse=True)}


def wordcloud_from_dict(d: dict):
    wc = WordCloud(
        background_color="black",
        colormap='Blues',
        max_words=200,
        mask=None,
        width=1600,
        height=1600
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


if __name__ == "__main__":
    comments_list = video_comments(VIDEO_ID)
