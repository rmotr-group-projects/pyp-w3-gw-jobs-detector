import click
import requests
from bs4 import BeautifulSoup

import settings

DEFAULT_KEYWORDS = [
     "Remote",
    "Postgres",
    "Python",
    "Javascript",
    "React",
    "Pandas"
]




def get_parent_posts(url, keywords=DEFAULT_KEYWORDS):
    count = 0
    job_posts = []
    
    # Retrieves all the parent comments, then appends to list
    soup = BeautifulSoup(open(url), "html.parser")
    trtags = soup.find_all("tr", class_="athing")
    for trtag in trtags:
        for child in trtag.descendants:
            try:
                if child.get('src') == "s.gif":
                    # every HN comment/post has a spacer gif with this name
                    if child.get('width') == "0":
                        # HN parent comments have a s.gif with width = 0
                        job_posts.append(trtag)
            except AttributeError:
                pass
    return job_posts
    
def count_keyword(job_posts, keyword):
    # gives count of keyword occurrences total
    count = 0
    for post in job_posts:
        result = string.count(str(post).upper(), keyword.upper())
        count += result
    return count

def count_keywords_combination(job_posts, keywords_string):
    # gives count of keyword combined occurrences total
    count = 0
    keywords = keywords_string.upper().split("-")
    for post in job_posts:
        occurred = True
        for keyword in keywords: #django, remote, python
            if keyword not in str(post).upper():
                occurred = False
        if occurred:
            count += 1
    return count


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
    # setup
    message = [] 
    filename = "tests/fixtures/" + post_id + ".html"
    myjobposts = get_parent_posts(filename)
    
    # Total job posts messge 
    total_posts = len(myjobposts)
    tmp_string = "Total job posts: " + str(total_posts)
    message.append(tmp_string)
    
    # Stats for keywords 
    for keyword in keywords:
        
    print(message)
    
    



if __name__ == '__main__':
    jobs_detector()