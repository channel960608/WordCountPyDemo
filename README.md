<!--
 * @Author: Caspar
 * @Date: 2022-02-16 21:12:30
 * @Description: file content
-->

# WordCount  
A project to count words in web page content.
Count words in each url and integrate the word counts from all urls in keywords list

## Requirements  
- Python 3.*
- urllib3
```shell
$ pip install -r requirements.txt
```

## Usage 
```Shell
$ python3 word_count.py -i <INPUT_URLS_FILE> -k <KEYWORDS_FILE> -n <NUMBER_OF_PROCESSES>
```  
### Example
```Shell
$ python3 word_count.py -i ./input.txt -k keywords.txt -n 5
```
