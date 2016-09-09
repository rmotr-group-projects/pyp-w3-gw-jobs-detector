import click
import requests
import urllib
from bs4 import BeautifulSoup

from jobs_detector import settings

DEFAULT_KEYWORDS = [
    # set some default keywords here
]


@click.group()
def jobs_detector():
    hacker_news(post_id, keywords, combinations)


@jobs_detector.command()
@click.option('-i', '--post-id', type=str, required=True, help='Post id from Hackernews.')
@click.option('-k', '--keywords', type=str, default=','.join(DEFAULT_KEYWORDS), help='Keywords for counting')
@click.option('-c', '--combinations', type=str,
              callback=lambda _, x: x.split(',') if x else x, help='Keywords with combo')



def hacker_news(post_id, keywords, combinations):
    """
    This subcommand aims to get jobs statistics by parsing "who is hiring?"
    HackerNews posts based on given set of keywords.
    """
    # HINT: You will probably want to use the `BeautifulSoup` tool to
    # parse the HTML content of the website
    pass


def get_posts(html_data):
    post_list = []
    with open('html_data') as f:
        parser = BeautifulSoup(f, 'html.parser')
        cmnt_rows = parser.find_all("tr", class_="athing comtr ")
        for item in cmnt_rows:
            if item.select('img[width=0]') and item.select_one(".c00"):
                post_list.append(item.select_one(".c00").text)
    return post_list
    

def get_html(hn_id):
    url_to_fetch = BASE_URL.replace('{}',hn_id)
    path_to_save = os.join.path(BASE_DIR,hn_id+".html")
    
    webpage_in_file = urllib.URLopener()
    webpage_in_file.retrieve(url_to_fetch, path_to_save)
    
    return path_to_save
    
    
    
    
if __name__ == '__main__':
    jobs_detector()
