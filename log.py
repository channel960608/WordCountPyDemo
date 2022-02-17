'''
Author: Caspar
Date: 2022-02-15 22:00:50
Description: file content
'''
import logging
import os

from logging.handlers import TimedRotatingFileHandler
from os.path import abspath, normpath, join

work_dir = '{}/logs'.format('./')
log_path = normpath(join(abspath(work_dir), 'word_count.log'))
if not os.path.isdir(work_dir):
    os.mkdir(work_dir)

logger = logging.getLogger(__name__)
logger.handlers.clear()
logger.setLevel(level = logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S %z')

file_handler = TimedRotatingFileHandler(log_path, \
    when="H", interval=1, backupCount=24)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
