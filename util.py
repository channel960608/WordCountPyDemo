'''
Author: Caspar
Date: 2022-02-15 22:07:21
Description: file content
'''
#%%
import re
import urllib3
from log import logger

http = urllib3.PoolManager()

def read_txt(path):
    """Read local txt file"""
    try:
        f = open(path)
        content = f.read()
        return content.split("\n")
    except FileNotFoundError as e:
        logger.error("{} is not found".format(path), exc_info=True)
        raise e
    except Exception as e:
        logger.error(str(e),  exc_info=True)
        raise e
    finally:
        if f:
            f.close()

def request_url(method, url):
    """Request the specific url and return data"""
    try:
        r = http.request(method, url)
        if r.status == 200:
            return r.data.decode('utf-8')
        else:
            raise Exception("Fail to {} data from {}".format(method, url))
    except Exception as e:
        logger.error(str(e),  exc_info=True)
        raise e

#%% 