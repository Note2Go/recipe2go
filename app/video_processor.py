import pytube
import log_processor
import os
# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from datetime import datetime


logger = log_processor.get_logger("video_processor")
media_folder = "../media/"
source_video_file_name = "source_video.mp4"

def get_youtube_video_name(url):
    logger.info("Start processing video from url({})".format(url))

    youtube = pytube.YouTube(url)
    video = youtube.streams.get_highest_resolution()

    logger.info('Video "{}" retrieved'.format(video.title))

    return video.title


def download_from_youtube(url):
    """
    download a video file from YouTube with the given url
    url: the url of the youtube video
    video_addr: where the video file will be stored
    """
    # retrieve video
    logger.info("Start processing video from url({})".format(url))
    youtube = pytube.YouTube(url)
    video = youtube.streams.get_highest_resolution()
    logger.info('Video "{}" retrieved'.format(video.title))

    # download video
    download_start_time = datetime.now()
    video.download(media_folder)
    download_finish_time = datetime.now()
    video_addr = media_folder + video.title + ".mp4"
    time_elapsed =  download_finish_time - download_start_time
    seconds_elapsed = time_elapsed.total_seconds()
    logger.info('Video "{}" downloaded with {} seconds:'.format(video_addr, seconds_elapsed))

    # change video file name
    new_video_addr = media_folder+source_video_file_name
    os.rename(video_addr,new_video_addr)

    return new_video_addr


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

def clear_media():
    media_files = []

    for filename in os.listdir(media_folder):
        file_path = os.path.join(media_folder, filename)
        try:
            if os.path.isfile(file_path):
                if file_path.endswith(".mp4") or file_path.endswith(".mp3"):
                    os.remove(file_path)
                    media_files.append(file_path)
        except Exception as e:
            logger.warn('Failed to delete %s. Reason: %s' % (file_path, e))

    msg = "The following media have been cleared:\n"
    for each in media_files:
        msg += "  " + each+"\n"

    logger.info(msg)


if __name__ == "__main__":
    # test_url = "https://www.youtube.com/watch?v=eY90ltI8Sh8"
    short_video_url = "https://www.youtube.com/watch?v=ww95zvvhX0c&list=PLfetWr5y3KmmAPUcfMnepril3nHDNTJ0a"
    # clear_media()
    video_addr = download_from_youtube(short_video_url)
    print("Video addr = {}".format(video_addr))

