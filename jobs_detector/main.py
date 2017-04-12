import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings

DEFAULT_KEYWORDS = [
    'Remote','Postgres','Python','Javascript','React','Pandas'
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
    
    keyword =  {word.capitalize(): 0 for word  in keywords.split(',')}
    combination = {word1.title(): 0 for word1 in combinations } if combinations else {}
    url = settings.BASE_URL.format(post_id)
    req = requests.get(url)
    soup = BeautifulSoup(req.text,'html.parser')
    posts = soup.find_all("tr",class_='athing')
    posts_jobs = [comments.find('span',class_='c00').get_text() for comments in posts if comments.find('img',width='0') if comments.find('span',class_='c00')]
    
    for job in posts_jobs:
        for key in keyword:
            if key.lower() in job:
                keyword[key] +=1
    
    
    print('Total job posts: {}\nKeywords:'.format(len(posts_jobs)))
    
    for k,v in keyword.items():
        print('{}: {} ({}%)'.format(k,v,int(v*100/len(posts_jobs))))
    
    
    if combination:
        for job in posts_jobs:
            for combi in combination:
                combi_keywords =  [i.lower() for i in combi.split('-')]
                
                if len([key for key in combi_keywords if key in job]) == len(combi_keywords):
                    combination[combi] += 1
                
        print('\nCombinations:')
        for k,v in combination.items():
            print('{}: {} ({}%)'.format(k, v,int(v*100/len(posts_jobs))))
                
        

if __name__ == '__main__':
    jobs_detector()
