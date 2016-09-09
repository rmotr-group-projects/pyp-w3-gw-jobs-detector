import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings

DEFAULT_KEYWORDS = [
    # set some default keywords here
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


def hacker_news(post_id, keywords, **combinations):
    """
    This subcommand aims to get jobs statistics by parsing "who is hiring?"
    HackerNews posts based on given set of keywords.
    """
    print('works')

    job_posts = []
    page = requests.get(
        "https://news.ycombinator.com/item?id=11814828")
    soup = BeautifulSoup(page.text, 'html.parser')
    posts = soup.find_all("tr", class_="athing")
    for post in posts:
        if post.find("img", width="0"):
            job_posts.append(post)

    post_matches = {}

    for _post in job_posts:
        post = _post.lower()
        for keyword in keywords:
            if keyword.lower() in post:
                post_matches.setdefault(keyword, [])
                post_matches[keyword].append(_post)

    stats = []
    total_jobs = len(job_posts)
    stats.append('Total job posts: %s' % total_jobs)
    stats.append('keywords:')
    for keyword in post_matches:
        key_stats = len( post_matches[keyword] )/total_jobs
        str = '{}: {} ({0:.0f}%)'.format(keyword, len(post_matches[keyword]), key_stats * 100)
        stats.append(str)
    for message in stats:
        print message



if __name__ == '__main__':
    jobs_detector()
