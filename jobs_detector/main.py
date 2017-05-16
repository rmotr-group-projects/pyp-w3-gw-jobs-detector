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
                        ascii_trtag = str(trtag).decode('ascii','ignore')
                        job_posts.append(ascii_trtag)
            except AttributeError:
                pass
    return job_posts
    
def count_keyword(job_posts, keyword):
    # gives count of keyword occurrences total
    count = 0
    for post in job_posts:
        string_post = str(post).upper()
        # count the total number of occurrences of a keyword in all the posts:
        # result = str.count(string_post, keyword.upper())
        # count += result
        # count the number of posts that mention the keyword at least onece:
        if keyword.upper() in string_post:
            count += 1 
    return count

def count_keywords_combination(job_posts, keywords_string):
    # gives count of keyword combined occurrences total
    count = 0
    combos = keywords_string.upper().split("-")
    for post in job_posts:
        occurred = True
        for combo in combos: #django, remote, python
            if combo.upper() not in str(post).upper():
                occurred = False
        if occurred:
            count += 1
    return count


def analyse_posts(job_posts, search_terms, search_function, total_posts):
    results = []
    for item in search_terms:
        item_count = search_function(job_posts, item)
        item_percentage = int((float(item_count)/float(total_posts))  * 100)
        item_string = "{item}: {item_count} ({item_percentage}%)"
        item_string = item_string.format(
            item=str.title(str(item)), 
            item_count=item_count, 
            item_percentage=item_percentage
        )
        results.append(item_string)
    return results
    
@click.group()
def jobs_detector():
    pass


@jobs_detector.command()
@click.option('-i', '--post-id', type=str, required=True)
@click.option('-k', '--keywords', type=str, default=','.join(DEFAULT_KEYWORDS))
@click.option('-c', '--combinations', type=str,
              callback=lambda _, __, x: x.split(',') if x else x)
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
    message.append("Keywords:")  
    keyword_string = keywords.upper()
    keywords = keyword_string.split(',')
    
    results_list = analyse_posts(myjobposts, keywords, count_keyword, total_posts)
    for result in results_list:
        message.append(result)
        
    #lets see if there are any combinations.
    if combinations != None:
        message.append("Combinations:")
        upper_list = [x.upper() for x in combinations]
        combinations = upper_list
        results_list = analyse_posts(myjobposts, combinations, count_keywords_combination, total_posts)
        for result in results_list:
            message.append(result)
    print(message)
    return message 

def cli():
    jobs_detector()
    

if __name__ == '__main__':
    jobs_detector()