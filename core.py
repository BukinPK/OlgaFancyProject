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


if __name__ == "__main__":
    comments_list = video_comments(VIDEO_ID)
