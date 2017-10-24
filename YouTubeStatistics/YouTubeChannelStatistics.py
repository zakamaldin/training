from apiclient.discovery import build
from apiclient.errors import HttpError
import xlsxwriter
import dateutil.parser
import datetime
import os.path

DEVELOPER_KEY = "REPLACE_ME"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MAX_RESULTS = 50

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)

today = datetime.date.today().strftime("%d_%m_%Y")
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data')
channel_id = ''


def get_channel_name(page_token=None, max_res=MAX_RESULTS):
    result = youtube.search().list(
        channelId=channel_id,
        type="video",
        part="snippet",
        maxResults=max_res,
        pageToken=page_token,
    ).execute()
    return result["items"][0]['snippet']['channelTitle']


def search_video(video_ids):
    result = youtube.videos().list(
        part='statistics,snippet',
        id=video_ids
    ).execute()
    return result['items']


def get_video_count():
    result = youtube.channels().list(
        part="statistics, contentDetails",
        id=channel_id
    ).execute()
    return int(result['items'][0]['statistics']['videoCount'])


def get_video_id_list(playlistitems_list_response):
    search_videos = []
    for item in playlistitems_list_response.get("items", []):
        search_videos.append(item['snippet']['resourceId']['videoId'])
    video_ids = ",".join(search_videos)
    return video_ids


def get_playlistitems_list_request():
    channel = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()
    uploads_playlist_id = channel['items'][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    playlistitems_list_request = youtube.playlistItems().list(
        playlistId=uploads_playlist_id,
        part="snippet",
        maxResults=50
    )
    return playlistitems_list_request


def get_channel_statistics():

    global channel_id
    channel_id = input('Write the channel\'s ID here: ')
    channel_name = get_channel_name()
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    data_xls = os.path.join(data_dir, "{0}from {1}.xlsx".format(channel_name, today))
    wb = xlsxwriter.Workbook(data_xls)
    ws = wb.add_worksheet('Statistics')
    row = 0
    ws.write_row(0, 0, ['Video title', 'Link to video', 'Published At', 'View count', 'Likes', 'Dislikes'])
    video_count = get_video_count()
    playlistitems_list_request = get_playlistitems_list_request()
    while playlistitems_list_request:
        playlistitems_list_response = playlistitems_list_request.execute()
        video_ids = get_video_id_list(playlistitems_list_response)
        videos_list = search_video(video_ids)
        for video in videos_list:
            row += 1
            print("Process: {0}%".format(int((row / video_count) * 100)))
            video_title = video["snippet"]["title"]
            link_to_video = 'https://www.youtube.com/watch?v=' + video['id']
            view_count = int(video['statistics']['viewCount'])
            try:
                like_count = int(video['statistics']['likeCount'])
            except KeyError:
                like_count = None
            try:
                dislike_count = int(video['statistics']['dislikeCount'])
            except KeyError:
                dislike_count = None

            date = video['snippet']['publishedAt']
            date = datetime.datetime.strftime(dateutil.parser.parse(date), '%d.%m.%Y')
            ws.write_row(row, 0, [video_title, link_to_video, date, view_count, like_count, dislike_count])

        playlistitems_list_request = youtube.playlistItems().list_next(playlistitems_list_request,
                                                                       playlistitems_list_response)
    wb.close()


if __name__ == "__main__":
    try:
        get_channel_statistics()
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
