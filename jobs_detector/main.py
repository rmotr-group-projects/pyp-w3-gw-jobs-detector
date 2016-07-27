import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings
#import settings

DEFAULT_KEYWORDS = ['remote',
                    'postgres',
                    'python',
                    'javascript',
                    'react',
                    'pandas',
                    ]
key_count = {}
comb_count = {}
    
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
    response = _request_page(post_id)
    jobListings = _extract_job_postings(response)
    num_of_job_listings = len(jobListings)
    
    _calculate_keyword_statistics(jobListings, keywords)
    _echo_keyword_results(num_of_job_listings, keywords)
    
    if combinations:
        _caluculate_combinations_statistics(jobListings, combinations)
        _echo_comb_results(num_of_job_listings, combinations)
    # elif keywords:
    #     _calculate_keyword_statistics(jobListings, keywords)
    #     _echo_keyword_results(num_of_job_listings, keywords)
    # else:
    #     _calculate_keyword_statistics(jobListings, keywords)
    #     _echo_keyword_results(num_of_job_listings, keywords)
        
        
def _request_page(post_id):
    """
    Makes a get request to ycombinator's job listings thread and returns a 
    response
    """
    return requests.get(settings.BASE_URL.format(post_id))
    
def _extract_job_postings(response):
    """
    Gets the top level comments (job listings) so we can use statistics on it later
    """
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all("tr", class_="athing")
    jobListings = [post for post in posts if post.find("img", width=0)]
    return jobListings
    
def _calculate_keyword_statistics(jobListings, keywords):
    """
    Searches for keywords in job listings and performs calculations
    """
    keyword_list = keywords.split(',')  if keywords else DEFAULT_KEYWORDS
    for listing in jobListings:
        for keyword in keyword_list:
            if keyword in listing.text.lower():
                key_count[keyword] = key_count.get(keyword, 0) + 1
    
def _caluculate_combinations_statistics(jobListings, combinations):
    """
    Searches for combinations in job listings and performs calculations
    """
    for comb in combinations:
        comb_keys = comb.split('-')
        for listing in jobListings:
            if all([key in listing.text.lower() for key in comb_keys]): 
                comb_count[comb] = comb_count.get(comb, 0) + 1
                
def _echo_keyword_results(num_jobs, keywords):
    """
    Displays the keyword results of the job search
    """
    keyword_list = keywords.split(',') if keywords else DEFAULT_KEYWORDS
    click.echo ('Total job posts: {}'.format(num_jobs))
    click.echo ()
    click.echo ('Keywords:')
    for kw in keyword_list:
        click.echo('{}: {} ({}%)'.format(kw.title(), key_count[kw], key_count[kw]*100//num_jobs))
            
def _echo_comb_results(num_jobs, combinations):
    """
    Displays the combination results of the job search
    """
    click.echo()
    click.echo("Combinations:")
    for comb in combinations:
        comb_str = '-'.join([key.title() for key in comb.split('-')])
        click.echo("{}: {} ({}%)".format(comb_str, comb_count[comb], comb_count[comb]*100//num_jobs))
    
if __name__ == '__main__':
    jobs_detector()
