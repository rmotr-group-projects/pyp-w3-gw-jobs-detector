import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings

DEFAULT_KEYWORDS = [
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
    soup = BeautifulSoup(html_doc, 'html.parser')


if __name__ == '__main__':
    jobs_detector()




#   PLAN OF ATTACK
#   1. Create web crawler
#       a. Get all HTML data
#       b. Parse HTML data into Python format (dict)
#   2. Create func to print Python dict into human readable form
#   3. Turn func into command line tool