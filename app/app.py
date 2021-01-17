from flask import Flask, g
from flask_restful import Resource, Api, reqparse
import log_processor
import re
import requests
import hashlib
from datetime import datetime
from config import time_format, server_responses, \
    server_log_file_name, url_hashing_character_count,\
    celery_backend, celery_broker
from media_processor import MediaProcessor
from pdf_processor import batch_convert_img2pdf
from email_processor  import send_pdf
from celery import Celery


# set up logger
current_time = datetime.now()
current_session_time = current_time.strftime(time_format)
logger = log_processor.get_logger(current_session_time,server_log_file_name)

# initialize the flask app
app = Flask("recipe2go")
api = Api(app)
parser = reqparse.RequestParser()
celery = Celery(
        app.import_name,
        backend=celery_backend,
        broker=celery_broker
    )
logger.info("Flask server started")


class GetYouTubeTask(Resource):
    def get(self):
        return server_responses["successful_get"]

    def post(self):
        # read arguments from request
        args = self.get_argument()
        url = args['url']
        email = args['email']

        # validate parameters
        valid_url = check_url(url)
        valid_email = check_email(email)
        if not valid_url:
            return server_responses["failed_post_url"]
        if not valid_email:
            return server_responses["failed_post_email"]
        logger.info("new request: url is {} and email is {}".format(url, email))

        # make an async call to process the video and proceed to return response
        extract_note.delay(url, email)
        return server_responses["successful_post"]

    def get_argument(self):
        # set up arguments needed in the parser
        parser.add_argument('url', type=str,
                            help="Please send a valid url of a YouTube Video that you wish to download ")
        parser.add_argument('email', type=str,
                            help="Please send your valid email address to receive the extracted note")

        # parse the arguments and return
        args = parser.parse_args()
        return args

api.add_resource(GetYouTubeTask,'/')


# Helper methods
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

# initiate the process of extracting notes
@celery.task()
def extract_note(url, email):

    # start processing
    if url != None and email != None:
        logger.info("new request: url is {} and email is {}".format(url, email))

    # create a hash for the video and use for logging
    url_hash = get_hash(url)
    task_logger = log_processor.get_logger(current_session_time, url_hash)

    # process the video to extract pdf slides from it
    media_processor = MediaProcessor(url = url, hash=url_hash, logger=task_logger)
    title, resources = media_processor.process_video()
    images_path = resources["images_path"]
    pdf_path = batch_convert_img2pdf(images_path)

    # send the final pdf slide to user
    send_pdf(email, pdf_path)


if __name__ == '__main__':
    app.run(debug=True)