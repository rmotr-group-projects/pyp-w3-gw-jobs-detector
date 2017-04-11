#achieved functionality, haven't tried tests

import click
import requests
import re
import collections
from bs4 import BeautifulSoup

from jobs_detector import exceptions, settings

DEFAULT_KEYWORDS = [
    'Remote', 'Postgres', 'Python', 'Javascript', 'React', 'Pandas'
]

@click.group()
def jobs_detector():
    pass


@jobs_detector.command()
@click.option('-i', '--post-id', type=str, required=True)
@click.option('-k', '--keywords', type=str, default=','.join(DEFAULT_KEYWORDS))
@click.option('-c', '--combinations', type=str,
              callback=lambda _, x: x.split(',') if x else x)

def hacker_news(post_id, keywords, combinations):
    """
    This subcommand aims to get jobs statistics by parsing "who is hiring?"
    HackerNews posts based on given set of keywords.
    """
    keywords = keywords.split(',')
    master_text, job_num = get_job_post_text(post_id)
    
    if combinations == None:
        results = if_keywords(master_text, keywords, job_num)
        print(print_template(job_num, results))
        
    else:
        key_results = if_keywords(master_text, keywords, job_num)
        combo_results = if_combination(master_text, combinations, job_num)
        print(print_template(job_num, key_results, combo_results))
        
def if_keywords(master_text, keywords, job_num):
    keywords_words_counter = single_word_counter_dict(master_text)  
    results = capture_results_to_string(keywords, keywords_words_counter, job_num)
    return results
    
def if_combination(master_text, combinations, job_num):
    combo_master = collections.Counter()
    for i in combinations:
        combinations_dict = single_combination(i, master_text)
        combo_master += combinations_dict
    results_combo = capture_results_to_string(combinations, combo_master, job_num)
    return results_combo
        
def get_job_post_text(post_id):
    '''Returns a list of job descriptions and the number of jobs, as a tuple'''
    
    HACKER_NEWS_URL = 'https://news.ycombinator.com/item?id='    
    r = requests.get(HACKER_NEWS_URL + str(post_id))
    c = r.content
    soup = BeautifulSoup(c, 'html.parser')
    
    master_text = []
    first_comment_filter = soup.find_all('img', width=0)
    for comment in first_comment_filter:
        try:
            content = comment.parent.next_sibling.next_sibling.text
            cont_str = ''.join(content)
            master_text.append(cont_str)         
        except AttributeError:
            break
    return master_text, len(master_text)

def single_word_counter_dict(text_list):
    '''Returns a counter object with the key-value pair as word-frequency'''
    
    unique_words_list = []
    for text in text_list:
        words = re.findall('\w+', text.lower())
        unique_words = list(set(words))
        unique_words_list.extend(unique_words)
    word_counter = collections.Counter(unique_words_list)
    return word_counter

def single_combination(keyword_string, text_list):
    '''Takes single keyword_string argument'''
    combo_list = keyword_string.split('-')
    combo_retrieval = []
    for text in text_list:
        words = re.findall('\w+', text.lower())
        unique_words = list(set(words))
        if set(combo_list) < set(unique_words):
            combo_retrieval.append(keyword_string)
    word_counter = collections.Counter(combo_retrieval)
    return word_counter
        
def capture_results_to_string(keywords, word_counter_dict, job_num):
    results = []
    results_string = ''
    for i in keywords:
        results.append(i + ': {} ({:.0f}%)'.format(word_counter_dict[i.lower()], word_counter_dict[i.lower()]/float(job_num)*100))
    for i in results:
        results_string += '{}\n'.format(i.title())
    return results_string
    
def print_template(job_num, counter1, counter2=None):
    template = '''
Total job posts: {}

Keywords:
{}
Combinations:
{}'''
    if not counter2:
        return template.format(job_num, counter1, '')
    else:
        return template.format(job_num, counter1, counter2)

if __name__ == '__main__':
    jobs_detector()

