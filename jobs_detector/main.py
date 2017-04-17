import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings

DEFAULT_FORMAT = "{}: {} ({}%)"
DEFAULT_KEYWORDS = [
    'remote', 
    'postgres',
    'python',
    'javascript',
    'react',
    'pandas'
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
    get_keys = keywords.split(',')
    
    jobs = get_jobs(post_id)    # list of jobs
    
    # list of keys found in jobs { "keyword": num_found }
    keyword_list = keywords.lower().split(',')
    keys_in_jobs = search_jobs_by_keyword(jobs, keyword_list) 
    
    # print list of keys found and percentage of posts found in
    print_list(jobs, keys_in_jobs)
    
    # if we have combinations of keywords, then process those too
    if combinations:
        combo_lists = []
        # split into combo lists
        for combo in combinations:
            combo_split = combo.lower().split('-')   # split combo joined by dash
            combo_lists.append(tuple(combo_split))          # append to combo lists
        
        # get list of combos found in jobs
        combos_in_jobs = search_jobs_for_combos(jobs, combo_lists)
        
        # print combo list
        if len(combos_in_jobs):
            print_combo_list(jobs, combos_in_jobs)
    
    
def get_jobs(post_id):
    # get url to scrape
    scrape_url = settings.BASE_URL.format(post_id)
    
    # get response of url
    response = requests.get(scrape_url)
    
    # if response is bad, then raise error
    if not response.status_code == requests.codes.ok:
        raise ValueError("Page request failed with status code: "
                            "{}".format(response.status_code))
    
    # response was good so we can process
    jobs = []
    soup = BeautifulSoup(response.text, 'html.parser')

    # find spacer that can indent posts
    for ind_td in soup.find_all('td', class_="ind"):
        # if post is not indented - it's a top level comment
        if ind_td.img.get('width') == '0' and not ind_td.parent.find("span", class_="c00") is None:
            # add the span class with post in it to our jobs
            jobs.append(ind_td.parent.find("span", class_="c00").text)
    return jobs
    
    
def search_jobs_by_keyword(job_list, key_list):
    ''' Searches jobs to find number of times keys are found '''
    output = {}
    for key in key_list:
        num_found = 0
        for job in job_list:
            if job.find(key) != -1:
                num_found += 1
        if num_found != 0:
            output[key] = num_found
    return output


def _check_has_keys(job_post, combo):
    # verify that keys are found in a post
    return all([keyword in job_post for keyword in combo])
          
         
def search_jobs_for_combos(job_list, combo_list):
    ''' Searches jobs for number of times combo of keywords found in post '''
    
    # weed out jobs that only have those combo of words in them
    output = {}
    for keywords in combo_list:
        num_found = 0
        for post in job_list:
            if _check_has_keys(post, keywords):
                num_found += 1
        if num_found > 0:
            output[keywords] = num_found
    return output

          
def print_list(job_list, key_list):
    
    print('Total job posts: {}'.format(len(job_list)))
    print('Keywords:')
    for key, value in key_list.iteritems():
        percentage = int((float(value) / len(job_list)) * 100)
        print(DEFAULT_FORMAT.format(key.capitalize(), value, percentage))
        

def print_combo_list(job_list, combo_list):
    
    print('Combinations:')
    for combo in combo_list.keys():
        value = combo_list[combo]
        percentage = int((float(value) / len(job_list)) * 100)
        key_output = '-'.join([key.capitalize() for key in combo])
        print(DEFAULT_FORMAT.format(key_output, value, percentage))
        

if __name__ == '__main__':
    jobs_detector()
