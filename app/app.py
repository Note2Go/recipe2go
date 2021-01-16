from flask import Flask
from flask_restful import Resource, Api, reqparse
import log_processor
import re
import requests

logger = log_processor.get_logger("flask")

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

responses = {
    "successful_get": (
        {"message": "please post to this api to use the service"},
        200
    ),
    "successful_post":(
        {"message":"Your request has been received. The extracted note will be sent to you shortly"},
        200
    ),
    "failed_post_url": (
        {"message": "the url provided is not a valid YouTube video address"},
        400
    ),
    "failed_post_email": (
        {"message": "the email provided is not a valid email address"},
        400
    )
}

class GetYouTubeTask(Resource):
    def get(self):
        return responses["successful_get"]

    def post(self):
        args = self.get_argument()
        url = args['url']
        email = args['email']

        valid_url = check_url(url)
        valid_email = check_email(email)

        if not valid_url:
            return responses["failed_post_url"]
        if not valid_email:
            return responses["failed_post_email"]

        print("url is {} and email is {}".format(url, email))

        return responses["successful_post"]

    def get_argument(self):
        parser.add_argument('url', type=str,
                            help="Please send a valid url of a YouTube Video that you wish to download ")

        parser.add_argument('email', type=str,
                            help="Please send your valid email address to receive the extracted note")
        args = parser.parse_args()

        return args

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



api.add_resource(GetYouTubeTask,'/')

if __name__ == '__main__':
    app.run(debug=True)