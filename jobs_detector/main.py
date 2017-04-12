'''
import sys
import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')
    
DEFAULT_KEYWORDS = [
                    'Remote', 
                    'Postgres', 
                    'Python',
                    'Javascript', 
                    'React', 
                    'Pandas'
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
    output = []
    keyword_list = [word if keywords else DEFAULT_KEYWORDS 
                    for word in keywords.title().split(',')]
    kwd_dict = {key: 0 for key in keyword_list}
    r = requests.get(settings.BASE_URL.format(post_id))
    
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.content, 'html.parser')
        data = soup.find_all('span', 'c00')
        total_jobs = len(data)
        output.append('Total job posts: {}\nKeywords:\n'.format(total_jobs))
        for kwd in keyword_list:
            for item in data:
                if kwd.lower() in item.__str__().lower():
                    kwd_dict[kwd] += 1
        for kwd in keyword_list:
            output.append('{}: {} ({}%)'.format(
                kwd, kwd_dict[kwd], int((kwd_dict[kwd]*100)/total_jobs)))
            
    if combinations:
        combo_dict = {}
        combo_list = [combo.split('-') for combo in combinations]
        output.append("Combinations:\n")
        for pair in combo_list:
            combo_name = '-'.join(pair).title()
            for item in data:
                if (pair[0].lower() in item.__str__().lower() 
                    and pair[1].lower() in item.__str__().lower()):
                    if combo_name not in combo_dict:
                        combo_dict[combo_name] = 0
                    combo_dict[combo_name] += 1
        for pair, value in combo_dict.items():
            output.append('{}: {} ({}%)'.format(
                pair, value, int((value*100)/total_jobs)))
        
    for item in output:
        print(item)

if __name__ == '__main__':
    jobs_detector()
'''    

import click
import requests
import sys
from bs4 import BeautifulSoup
from jobs_detector import settings

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')
    
DEFAULT_KEYWORDS = [
                    'Remote', 
                    'Postgres', 
                    'Python',
                    'Javascript', 
                    'React', 
                    'Pandas'
                    ]


@click.group()
def jobs_detector():
    pass

@jobs_detector.command()
@click.option('-i', '--post-id', type=str, required=True)
@click.option('-k', '--keywords', type=str, default=','.join(DEFAULT_KEYWORDS))
@click.option('-c', '--combinations', type=str,
              callback=lambda _, __, x: x.split(',') if x else x)
def hacker_news(post_id, keywords, combinations):
    output = []
    keyword_list = [word if keywords else DEFAULT_KEYWORDS 
                    for word in keywords.title().split(',')]
    kwd_dict = {key: 0 for key in keyword_list}
    r = requests.get(settings.BASE_URL.format(post_id))
    
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.content.decode('utf-8'), 'html.parser')
        data = soup.find_all('span', 'c00')
        total_jobs = len(data)
        output.append('Total job posts: {}\nKeywords:\n'.format(total_jobs))
        for kwd in keyword_list:
            for item in data:
                if kwd.lower() in item.__str__().lower():
                    kwd_dict[kwd] += 1
        for kwd in keyword_list:
            output.append('{}: {} ({}%)'.format(
                kwd, kwd_dict[kwd], int((kwd_dict[kwd]*100)/total_jobs)))
            
    if combinations:
        combo_dict = {}
        combo_list = [combo.split('-') for combo in combinations]
        output.append("Combinations:\n")
        for pair in combo_list:
            combo_name = '-'.join(pair).title()
            for item in data:
                if (pair[0].lower() in item.__str__().lower() 
                    and pair[1].lower() in item.__str__().lower()):
                    if combo_name not in combo_dict:
                        combo_dict[combo_name] = 0
                    combo_dict[combo_name] += 1
        for pair, value in combo_dict.items():
            output.append('{}: {} ({}%)'.format(
                pair, value, int((value*100)/total_jobs)))

    for item in output:
        print(item)

if __name__ == '__main__':
    jobs_detector()