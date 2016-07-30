import click
import requests
import re
from bs4 import BeautifulSoup
from .settings import *

DEFAULT_KEYWORDS = [
    "Remote",
    "Postgres",
    "Python",
    "Javascript",
    "React",
    "Pandas",
]


def pull_load(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    posts = soup.find_all('tr', class_='athing') # for the fixtures file
    posts = [post.get_text().upper() for post in posts if re.search('<img.*width="0".*/>', str(post))]
    total = len(posts)
    return posts, total 


def output(counters, keywords, total_posts, combinations):
    click.echo('Total job posts: {}'.format(total_posts))
    click.echo('Keywords:')
    for keyword in keywords:
        click.echo('{}: {} ({}%)'.format(keyword.title(), counters[keyword], int((float(counters[keyword])/float(total_posts))*100)))
    if combinations:
        click.echo('Combinations:')
        for combo in combinations:
            click.echo('{}: {} ({}%)'.format(combo.title(), counters[combo], int((float(counters[combo])/float(total_posts))*100)))

@click.group()
def jobs_detector():
    """
    Tool to use to parse through HackerNews jobs postings, returning the number of posts by keywords.
    Please run with the command hacker_news.
    """
    pass

@jobs_detector.command()
@click.option('-i', '--post-id', type=str, required=True,
                        help='Required command:  Post-ID of HackerNews to parse.')
                        
@click.option('-k', '--keywords', type=str, default=','.join(DEFAULT_KEYWORDS),
                        help='Optional command:  Specify Custom Keywords to use when parsing the post')
                        
@click.option('-c', '--combinations', type=str,
              callback=lambda _, x: x.split(',') if x else x,
              help='Optional command:  Specify groups of Custom Keywords to parse together.  Delimit keywords using a hyphen \'-\'.')

def hacker_news(post_id, keywords, combinations):
    """
    This subcommand aims to get jobs statistics by parsing "who is hiring?"
    HackerNews posts based on given set of keywords.
    """
    # fix keywords list
    keywords = list(keywords.split(','))

    # --- get the amount and content of top level comments
    url = BASE_URL.format(post_id)
    posts, total = pull_load(url)
    counters = {keyword: 0 for keyword in keywords}
    if combinations:
        counters.update({combo: 0 for combo in combinations}) 
     
    # --- iterate over each top-level post and search for each keyword, adding to the count dictionary if found.
    for post in posts:
        for keyword in keywords:
            counters[keyword] += keyword.upper() in post
        if combinations:
            for combo in combinations:
                counters[combo] += all(c.upper() in post for c in combo.split('-'))

    output(counters, keywords, total, combinations)


if __name__ == '__main__':
    jobs_detector()
