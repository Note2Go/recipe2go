# log file setting
time_format = '%Y_%m_%d_%H_%M_%S'
server_log_file_name = "server"
url_hashing_character_count = 8

# flask server setting
server_responses = {
    "successful_get": (
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

# media setting
media_folder = "../media/"
source_video_file_name = "source_video"
default_num_of_video_clip = 3


# email setting
email_usrname = "thenote2go@gmail.com"
email_password = "TheNote2Go"
email_subject = "Your recipe is ready to go!"
email_body = "Check out the attached pdf file for your recipe"