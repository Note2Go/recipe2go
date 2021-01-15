import pytube
import log_processor
import os
from moviepy import editor
from datetime import datetime



logger = log_processor.get_logger("video_processor")
media_folder = "../media/"
source_video_file_name = "source_video.mp4"
default_num_of_video_clip = 10

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


def slice_video(video_addr, clip_time_list=None):
    """
    slice a video into a clips, given the time on which to cut
    video_addr: where the video file is stored
    video_time_list: the list of times to cut videos,
        for example, [15,30] will cut a video into [0:15], [15:30], and [30:]
    """
    source_clip = editor.VideoFileClip(video_addr)
    clips_addr = []

    if clip_time_list != None:
        logger.info("Start slicing the video at ({}), "
                    "slicing interval is {}".format(video_addr, clip_time_list))
    else:
        duration= source_clip.duration
        clip_length =duration/default_num_of_video_clip
        clip_time_list = []
        for i in range(0,default_num_of_video_clip+1):
            clip_time_list.append(clip_length*i)
        logger.info("Start slicing the video at ({})".format(video_addr))
        print("clip_time_list is {}".format(clip_time_list))
        logger.info("Start slicing the video at ({}), "
                    "no slicing intervals provided, "
                    "choose {} intervals on default, "
                    "slicing interval is {}".format(video_addr,
                                                    default_num_of_video_clip,
                                                    clip_time_list))

    for i in range(0,len(clip_time_list)-1):
        current_clip_start_time = clip_time_list[i]
        current_clip_end_time = clip_time_list[i+1]
        print("Clip{} - ({},{})".format(i+1, current_clip_start_time,current_clip_end_time))
        subclip = source_clip.subclip(current_clip_start_time,current_clip_end_time)
        current_clip_addr = media_folder + "clip{}.mp4".format(i+1)
        clips_addr.append(current_clip_addr)
        subclip.write_videofile(current_clip_addr)

    # source_clip.write_videofile(media_folder+"clip20.mp4")
    return clips_addr


def extract_audio(video_addr):
    video = editor.VideoFileClip(video_addr)
    audio = video.audio
    audio_addr = video_addr.replace("mp4","mp3")
    audio.write_audiofile(audio_addr)
    return audio_addr

def batch_extract_audio(video_addr_list):
    audio_addr_list = []
    for each in video_addr_list:
        audio_addr = extract_audio(each)
        audio_addr_list.append(audio_addr)

    return audio_addr_list

def extract_frame(video_addr, frame_time=0.1):
    clip = editor.VideoFileClip(video_addr)
    img_addr = video_addr.replace("mp4","png")
    clip.save_frame(img_addr,frame_time)
    return img_addr

def batch_extract_cover_img(video_addr_list):
    img_addr_list = []
    for each in video_addr_list:
        img_addr = extract_frame(each)
        img_addr_list.append(img_addr)
    return  img_addr_list



def clear_media():
    media_files = []

    for filename in os.listdir(media_folder):
        file_path = os.path.join(media_folder, filename)
        try:
            if os.path.isfile(file_path):
                if (file_path.endswith(".mp4")
                        or file_path.endswith(".mp3")
                        or file_path.endswith(".png")):

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
    clear_media()
    video_addr = download_from_youtube(short_video_url)
    print("Video addr = {}".format(video_addr))
    clip_addr = slice_video(video_addr)
    print("clip addr = {}".format(clip_addr))


    img_addr_list = batch_extract_cover_img(clip_addr)
    print("img_addr = {}".format(img_addr_list))

    audio_addr_list = batch_extract_audio(clip_addr)
    print("audio_addr_list = {}".format(audio_addr_list))

