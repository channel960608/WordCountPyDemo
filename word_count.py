'''
Author: Caspar
Date: 2022-02-15 20:40:26
Description: file content
'''
#%%
from log import logger
from util import read_txt, request_url
import urllib3
import re
import heapq
from multiprocessing import Pool, current_process
import os
import sys, getopt
import argparse
#%%
def run(input_path, keyword_path, process_num=5):
    """Run the job with specific input file path(for urls and keywords) and the num of processes"""
    
    logger.info("Start the job with #process = {} for input files {} and {}".format(process_num, input_path, keyword_path))
    # Retrive urls and keywords from local file
    urls = read_txt(input_path)
    keywords = read_txt(keyword_path)
    
    # Execute the jobs for given input
    # You can choose multiprocessing by define process_num
    list_result = excute(process_one_url, [(x, keywords) for x in urls], process_num=process_num)
    
    # Integrate results of jobs
    dict_total = combine(list_result)
    list_result_sorted = sort_dict_by_value(dict_total)
    
    msg = ", ".join(["'" + x[0] + "'" + " : " + str(x[1]) for x in list_result_sorted])
    logger.info("The total result for the job: {}".format(msg))
    return list_result_sorted

def excute(f, list_input, process_num = 1):
    """Execute the job
    
    Args:
        f (function): the function to process input 
        list_input (list): a list of input data
        process_num (int):  number of processes to execute subtasks, if process_num > 1 then create a process pool to do it    

    Returns:
        list: result of all subtasks
    """
    if process_num == 1:
        return use_loop(f, list_input)
    else:
        return use_multipleprocess(f, list_input, process_num=process_num)

def use_multipleprocess(f, list_input, process_num = 5):
    """Multiple processing"""
    list_result = []
    try:
        p = Pool(process_num)
        res = p.map(f, list_input)
        list_result += res
    except Exception as e:
        logger.error(str(e),  exc_info=True)
    finally:
        p.close()
    return list_result

def use_loop(f, list_input):
    """Single processing"""
    list_result = []
    for input in list_input:
        list_result.append(f(input))
    return list_result

def process_one_url(url_and_keywords):
    """The subtask to process one url, count the words from that url and return the frequency of keywords
    
    Args:
        url_and_keywords (tuple):  a tuple like (url, keywords) containing the current url and the list of keywords

    Returns:
        list: the frequency of keywords in this url
    """
    logger.info("Process {}: Start processing content from {}".format(str(current_process()), url_and_keywords[0]))
    try:
        content = request_url("GET", url_and_keywords[0])
        content_preprocessed = preprocess_content(content)
        dict_words = {} 
        for line in content_preprocessed.split("\n"):
            words = line.split(" ")
            for word in words:
                if word != "":
                    if word in dict_words:
                        dict_words[word] += 1
                    else:
                        dict_words[word] = 1
            
        largest_3 = largest_n_element(dict_words, 3)
        msg = ", ".join(["\'" + x[0] + "\'" + " : " + str(x[1]) for x in largest_3])
        logger.info("{} : The most frequent words in the given list are [{}]".format(str(current_process()), msg))
        list_sorted = [(dict_words[x], x) for x in dict_words if x in url_and_keywords[1]]
        list_sorted.sort()
        list_sorted.reverse()
        logger.info("Process {}: End processing content from {}".format(str(current_process()), url_and_keywords[0]))
        return list_sorted
    except Exception as e:
        logger.error(str(e),  exc_info=True)
        return []        

def preprocess_content(content):
    """Preprocessing the content you retrieve from the url

    Args:
        content (str): the content you get from url

    Returns:
        str: processed content
    """
    # Do some necessary preprocessing for the content retrieved from webside
    # - remove punctuations
    # - to lower case
    # - other operations if necessary
    content = re.sub(r'[^\w\s]','',content)
    return content.lower()

def largest_n_element(m_dict, n):
    """Get the largest n words from the dict

    Args:
        m_dict (dict): the dict with word as key and the count of word as value
        n (int): the number of elements we have to return 

    Returns:
        list_: the n largest pairs in the dict order by value
    """
    # use priorityqueue to find the largest n words in map
    heap = [(x, m_dict[x]) for x in m_dict]
    return heapq.nlargest(n, heap, key = lambda x : x[1])


def combine(list_results):
    dict_total = {}
    for result in list_results:
        for m in result:
            if m[1] in dict_total:
                dict_total[m[1]] += m[0]
            else:
                dict_total[m[1]] = m[0]
    return dict_total

def sort_dict_by_value(m_dict):
    """Sort the dict by value"""
    list_tuple = [(x, m_dict[x]) for x in m_dict]
    list_tuple.sort(key = lambda x : -x[1])
    return list_tuple

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_urls')
    parser.add_argument('-k', '--keywords')
    parser.add_argument('-n', '--process_num')
    
    args = parser.parse_args()
    
    run(input_path=args.input_urls, keyword_path=args.keywords, process_num=int(args.process_num))
# %%
if __name__ == '__main__':
    main()

# %%
