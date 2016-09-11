import os
import sys
import click
from bs4 import BeautifulSoup
from six.moves import urllib
import settings

DEFAULT_KEYWORDS = ['remote','Postgres','python','javascript','react','pandas'
    # set some default keywords here
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
    # HINT: You will probably want to use the `BeautifulSoup` tool to
    # parse the HTML content of the website
    keywords_list = keywords.split(',')
    if combinations:
        combo_list = [x.split('-') for x in combinations]
    else: combo_list =[]
    
    hn_html = settings.BASE_URL.format(post_id)
    file_path = os.path.join(settings.BASE_DIR, post_id + ".html")
    htmldata = urllib.request.urlopen(hn_html)
    
    with open(file_path, 'w') as fp:
        if sys.version_info < (3, 0):
            fp.write(htmldata.read())
        else:
            fp.write(htmldata.read().decode('cp437'))
    
    with open(file_path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    
    posts = soup.find_all("tr", class_="athing comtr ")
    job_posts = []
    for post in posts:
        if post.find("img", width="0"):
            job_posts.append(post.text)
    
    result_formatted = ["Total job posts: {}".format(len(job_posts)),"Keywords:"] + get_result(job_posts,keywords_list,combo_list)
    
    for msg in result_formatted:
        print (msg)

def keyword_count(post_list, word):
    word_count = 0
    for elem in post_list:
        elem1 = elem.lower()
        if word.lower() in elem1:
            word_count += 1
    return word_count
    
def combowords_count(post_list, combo_words):
    combo_count = 0
    for elem in post_list:
        elem1 = elem.lower()
        word_presence = [0]*len(combo_words)
        for ind in range(len(combo_words)):
            if combo_words[ind].lower() in elem1:
                word_presence[ind] = 1
        if all(word_presence):
            combo_count += 1
    return combo_count
    
def get_result(job_posts,keywords_list,combo_list):
        total_posts = len(job_posts)
                
        keyword_result = {}
        for kword in keywords_list:
            keyword_result[kword] = keyword_count(job_posts, kword)
        keyword_result_formatted = ["{key}: {value} ({percent}%)".format(key = x.capitalize(), value = keyword_result[x], percent = 100*keyword_result[x]/(total_posts)) for x in keyword_result.keys()]
        
        combo_result = {}
        for combo in combo_list:
            combo1 = [x.capitalize() for x in combo]
            combo_result['-'.join(combo1)] = combowords_count(job_posts, combo)
        combo_result_formatted = ["{key}: {value} ({percent}%)".format(key = x, value = combo_result[x], percent = 100*combo_result[x]/total_posts) for x in combo_result.keys()]
        if len(combo_result_formatted) != 0:
            combo_result_formatted = ["Combinations:"] + combo_result_formatted
        return keyword_result_formatted + combo_result_formatted
    
if __name__ == '__main__':
    jobs_detector()
