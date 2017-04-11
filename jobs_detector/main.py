import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings

DEFAULT_KEYWORDS = [
    'Remote', 'Python', 'Postgres', 'Javascript', 'React', 'Pandas'
]


#@click.group()
def jobs_detector():
    pass
"""

@jobs_detector.command()
@click.option('-i', '--post-id', type=str, required=True)
@click.option('-k', '--keywords', type=str, default=','.join(DEFAULT_KEYWORDS))
@click.option('-c', '--combinations', type=str,
              callback=lambda _, x: x.split(',') if x else x)
"""              
def hacker_news(post_id, keywords, combinations):
    """
    This subcommand aims to get jobs statistics by parsing "who is hiring?"
    HackerNews posts based on given set of keywords.
    """
    stats = []
    
    #Retrieve the data and filter out what we want to detect
    page_data = _get_data_from_page(post_id)
    job_posts = _get_all_parent_comments(page_data)
    
    #Stats representation 
    keyword_stats = _get_keyword_stats(keywords, job_posts)
    total = len(keyword_stats)
    
    stats.append('Total job posts: {}'.format(len(total)))
    stats.append("Keywords:")
    for key, count in keyword_stats.items():
        stats.append("{0}: {1} ({2}%)").format(key, count, int(count * 100 / total))
    
    import ipdb; ipdb.set_trace()
        
    click.echo(stats);
    return stats


def _get_data_from_page(post_id):    
    return requests.get(settings.BASE_URL.format(post_id))


def _get_all_parent_comments(data):
    parent_comments = []
    soup = BeautifulSoup(data.text, 'html.parser')
    posts = soup.find_all("tr", class_="athing")
    
    for post in posts:
        if post.find("img", width = 0):
            parent_comments.append(post.text)
            
    return parent_comments


def _get_keyword_stats(keywords, posts):
    post_matches = {}
    keyword_list = []
    post_list = []
    
    for k in keywords.split(","):
        keyword_list.append(str(k).lower().strip())
    
    for p in post_list:
        post_list.append(p.lower)
        
    for keyword in keyword_list:
        for post in post_list:
            if keyword in post:
                post_matches.setdefault(keyword, [])
                post_matches[keyword].append(post)
                
    return post_matches

if __name__ == '__main__':
    jobs_detector()
