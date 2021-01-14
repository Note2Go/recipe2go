import pytube




def get_youtube_video_name(url):
    """

    """
    youtube = pytube.YouTube(url)
    video = youtube.streams.get_highest_resolution()
    return video.title


def download_from_youtube(url, video_folder):
    """
    download a video file from YouTube with the given url
    url: the url of the youtube video
    video_addr: where the video file will be stored
    """
    youtube = pytube.YouTube(url)
    video = youtube.streams.get_highest_resolution()
    video.download(video_folder)

    return video_folder+video.title

def slice_video(video_addr, video_time_list):
    """
    slice a video into a clips, given the time on which to cut
    video_addr: where the video file is stored
    video_time_list: the list of times to cut videos,
        for example, [15,30] will cut a video into [0:15], [15:30], and [30:]
    """
    pass

def extract_audio(video_addr, audio_addr):
    pass

def extract_frames(video_addr, frame_time):
    pass

if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=eY90ltI8Sh8"

    video_addr = download_from_youtube(test_url,
                          "videos")