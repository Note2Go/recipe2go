from speech_to_text import *
from video2keyframes import *
from pprint import pprint
import json

def video2recipe(video_id, videopath):
    dir = './extract_result/'
    keyframes, time_frame_list = keyframs_time(videopath, dir)
    transcript_list = get_text_from_video(video_id)
    temp_text = ""
    counter = 1

    divided_steps = divide_steps(transcript_list, time_frame_list)
    steps = []
    for transcript, keyframe in zip(divided_steps,keyframes):
        counter += 1
        if transcript != "":
            keyframe["transcript"] = transcript
            steps.append(keyframe)

    for item in transcript_list:
        text = item['text']
        temp_text += text

        # result = classify_content(temp_text)
    ingredients_result = []
    equipments_result = []
    ingredients = []
    equipments = []
    temp_result = analyze_entity_sentiment(temp_text)
    # Remove duplicates
    [ingredients.append(x) for x in temp_result if x not in ingredients]
    [equipments.append(x) for x in temp_result if x not in equipments]
    # final filtering
    for item in ingredients:
        if item in ingredients_list:
            ingredients_result.append(item)
    for item in equipments:
        if item in equipment_list:
            equipments_result.append(item)
    res = {"ingredients_result": ingredients_result,
           "equipments_result":equipments_result,
           "steps": steps}
    return res



if __name__ == "__main__":
    result = video2recipe("ztl0gGVFoK0&t", 'demo.mp4')
    pprint(result)