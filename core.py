import collections
import re
import time

from googleapiclient.discovery import build

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


def word_count(comments: list[str]):
    # defaultdict -- это такой же словарь как и обычный, только ты можешь задавать ему дефолтное значение типо если
    # такого ключа нет -- то он выставляется нулём. Это чтобы можно было сразу инкрементить значение, а не делать
    # проверку на то есть оно или нет и в случае если нет то присваисать, а в случае если есть -- инкрементить.
    # Не забудь удалить комменты перед сдачей)))
    word_count_dict = collections.defaultdict(lambda: 0)
    for comment in comments:
        clean_comment = re.sub(r"\W", " ", comment)

        # Тут можешь точку ставить и чекать правильно ли отрабатывает твоя регулярка
        for r in clean_comment.split():
            word_count_dict[r] += 1

    # Это тупо сортировка, не пугайся
    return {k: v for k, v in sorted(word_count_dict.items(), key=lambda x: x[1], reverse=True)}


if __name__ == "__main__":
    comments_list = video_comments(VIDEO_ID)
