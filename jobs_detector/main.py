from __future__ import  (print_function, division)
import click
import requests
from bs4 import BeautifulSoup
#from jobs_detector import settings

DEFAULT_KEYWORDS = [
    # set some default keywords here
'Remote', 'Postgres', 'Python', 'Javascript', 'React', 'Pandas'
]
'''
@click.group()
def jobs_detector():
    pass


@jobs_detector.command()
@click.option('-i', '--post-id', type=str, required=True)
@click.option('-k', '--keywords', type=str, default=','.join(DEFAULT_KEYWORDS))
@click.option('-c', '--combinations', type=str,
              callback=lambda _, x: x.split(',') if x else x)
'''

def hacker_news(post_id="11814828", keywords=DEFAULT_KEYWORDS, **kwargs):
    """
    This subcommand aims to get jobs statistics by parsing "who is hiring?"
    HackerNews posts based on given set of keywords.
    """
    job_posts = []
    page = requests.get(
        "https://news.ycombinator.com/item?id={}".format(post_id))
    soup = BeautifulSoup(page.text, 'html.parser')
    posts = soup.find_all("tr", class_="athing")
    for post in posts:
        if post.find("img", width="0"):
            job_posts.append(post)

    #keywords = ['python', 'django', 'remote']
    post_matches = {key:0 for key in keywords}

    for each_post in job_posts:
        #post = each_post.lower()
        for keyword in keywords:
            if keyword.lower() in str(each_post).lower():
                post_matches[keyword]+=1

    stats = []
    total_jobs = len(job_posts)
    stats.append('Total job posts: %s' % total_jobs)
    stats.append('keywords:')
    for key in post_matches:
        key_stats =  post_matches[key] /total_jobs
        string = '%s: %s (%d%%)'%(key, post_matches[key], key_stats * 100)
        stats.append(string)
    print(stats)


#if __name__ == '__main__':
#    jobs_detector()


man=hacker_news()
