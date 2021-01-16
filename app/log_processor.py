import logging
import os
from datetime import datetime

log_folder = '../logs/'
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def get_logger(current_session, current_task):

    # set up the sub-folder for current session logs
    current_session_folder = current_session+"/"
    if not os.path.exists(log_folder+current_session_folder):
        os.mkdir(log_folder+current_session_folder)

    # set up logger
    logger = logging.getLogger(current_task)
    logger.setLevel(logging.DEBUG)

    # set up file handler
    log_file_addr = current_task+".log"
    fh = logging.FileHandler(log_folder+current_session_folder+log_file_addr)
    fh.setLevel(logging.DEBUG)

    # set up console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # set up logging format
    formatter = logging.Formatter(log_format)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add both handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

# needs update
def clear_log():
    log_files = []

    for filename in os.listdir(log_folder):
        file_path = os.path.join(log_folder, filename)
        try:
            if os.path.isfile(file_path):
                if file_path.endswith(".log"):
                    log_files.append(file_path)
                    os.remove(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    print("The following logs have been cleared:")
    for each in log_files:
        print("  "+each)



if __name__ == "__main__":
    print("Testing Log Processor")
    # logger = get_logger("Shawn Test")
    # logger.info("haha")
