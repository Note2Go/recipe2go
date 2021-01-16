from flask import Flask
from flask_restful import Resource, Api, reqparse
import log_processor
import re
import requests
import hashlib
from datetime import datetime
from config import time_format, server_responses, server_log_file_name, url_hashing_character_count
from media_processor import MediaProcessor

# set up logger
current_time = datetime.now()
current_session_time = current_time.strftime(time_format)
logger = log_processor.get_logger(current_session_time,server_log_file_name)

# initialize the flask app
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

logger.info("Flask server started")


class GetYouTubeTask(Resource):
    def get(self):
        return server_responses["successful_get"]

    def post(self):
        args = self.get_argument()
        url = args['url']
        email = args['email']

        valid_url = check_url(url)
        valid_email = check_email(email)

        if not valid_url:
            return server_responses["failed_post_url"]
        if not valid_email:
            return server_responses["failed_post_email"]

        print("url is {} and email is {}".format(url, email))
        extract_note(url, email)

        return server_responses["successful_post"]

    def get_argument(self):
        parser.add_argument('url', type=str,
                            help="Please send a valid url of a YouTube Video that you wish to download ")

        parser.add_argument('email', type=str,
                            help="Please send your valid email address to receive the extracted note")
        args = parser.parse_args()

        return args

api.add_resource(GetYouTubeTask,'/')


def extract_note(url, email):
    url_hash = get_hash(url)
    task_logger = log_processor.get_logger(current_session_time, url_hash)
    media_processor = MediaProcessor(url = url, hash=url_hash, logger=task_logger)
    resources = media_processor.process_video()
    print(resources)
    pass


def get_hash(s):
    hash_object = hashlib.sha512(s.encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex[0:url_hashing_character_count]


def check_url(url):
    if not (url.startswith("https://www.youtube.com/watch?v=")
        or url.startswith("www.youtube.com/watch?v=")):
        return False

    try:
        request = requests.get(url)
        if request.status_code != 200:
            print("3")
            return False
    except:
        print("Exception!")
        return False

    return True

def check_email(email):
    regex_for_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return re.search(regex_for_email, email)




if __name__ == '__main__':
    app.run(debug=True)