import click, re, requests
from bs4 import BeautifulSoup
# from jobs_detector import settings
import settings, exceptions
from helpers import _keyword_search, _check_combinations, _get_percent
from collections import defaultdict

@jobs_detector.command()
@click.option('-i', '--post-id', type=str, required=True, help= 'HN Post ID.')
@click.option('-k', '--keywords', type=str, default=','.join(DEFAULT_KEYWORDS),
help= "Specify keywords")
@click.option('-c', '--combinations', type=str, help= "Specify keyword combinations to match",
              callback=lambda _, x: x.split(',') if x else x)
@click.argument('hacker_news')


@click.group()

def jobs_detector():
    """
    Find frequency of job-related keywords in a specified site.
    Currently only supports hacker_news.
    """
    pass


#Dict storage for keyword:num and keyword_list:[id1, id2] values
keywords_dict = {}.setdefault
comments_dict = {}
DEFAULT_KEYWORDS = [
    # set some default keywords here
    'Remote',
    'Postgres',
    'Python',
    'Javascript',
    'React',
    'Pandas',
]

def hacker_news(post_id, keywords, combinations):
    """
    Gets jobs statistics by searching HackerNews 
    "who is hiring?" posts for given set of keywords.
    """
    
    combinations_list = combinations.split()
    comments = []
    combinations_dict = {}

    # Fetch the post and make soup.
    # BASE_URL = 'https://news.ycombinator.com/item?id={}'
    url = BASE_URL.format(post_id)
    r = requests.get(url)
    page_content = r.content
    soup = BeautifulSoup(page_content, 'html.parser')
    
    
    for comment in soup.find_all('span', class_='c00'):
        for keyword in keywords:
            _keyword_search(comment, keyword)

    # if combinations have been specified,
    # check for them.
    if combinations:
        for combination in combinations_list:
            _check_combinations(combinations)
        

    total_num_posts = len(comments_dict)
    
    # Print results.
    click.echo("Total job posts: {}\n\nKeywords:".format(total_num_posts))
    for keyword in keywords:
        keyword_count = len(keywords_dict)
        keyword_percentage = _get_percent(keyword_count, comments_dict)
        click.echo("{k}: {kc} ({kp}%)".format(k=keyword, kc=keyword_count, kp=keyword_percentage))

    if combinations:
        click.echo("Combinations:\n")

        for combination in combinations:
            combination_count = len(combinations_dict)
            combination_percentage = _get_percent(combination_count, comments_dict)
            click.echo("{c}: {cc} ({cp}%)",format(c=combination, cc=combination_count, cp=combination_percentage))
        
    # if combinations:
    #     click.echo("Combinations:\n")

    #     for combination in combinations:
    #         combination_count = len(combinations_dict)
    #         combination_percentage = combination_count / len(comments_dict)
            
    #         click.echo("{c}: {cc} ({cp}%)",format(c=combination, cc=combination_count, cp=combination_percentage))

if __name__ == '__main__':
    print "run"
    jobs_detector()
