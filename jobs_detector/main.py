import click
import requests
from bs4 import BeautifulSoup


from jobs_detector import settings
from collections import defaultdict



DEFAULT_KEYWORDS = [
    #set some default keywords here
    'Remote',
    'Postgres',
    'Python',
    'Javascript',
    'React',
    'Pandas'

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
    
    data_to_parse = request_jobs_page(post_id)
    job_posts = retrieve_job_postings(data_to_parse) # get all top comments
    

    # renaming this from response, I found it confusing because we already use response as a variable in the get URL and data request.
    job_stats = []
    
    job_stats.append(get_total_jobs(job_posts))
    
    keyword_stats = get_keyword_stats(keywords, job_posts)
    job_stats += keyword_stats_repr(keyword_stats, job_posts)

    if combinations:
        combined_stats = get_combination_stats(combinations, job_posts)
        job_stats += combinations_stats_repr(combined_stats, job_posts)
    
    click.echo(job_stats);
    return job_stats
    

def get_keyword_stats (keywords, job_posts) :
    ''' returns a dict with key = keyword, value = count of keywords in job_posts  
        "keywords": list of keywords to search the comments for.
            eq: ['Django', 'Python']
        "job_posts": List of comments (top comments) in HN thread
    '''
  
    # initialize 
    keyword_dict = defaultdict(int)

    # clean up keywords, you only need lower case
    formatted_keywords = [str(keyword).lower().strip() for keyword in keywords.split(",")]
    formatted_jobs = [job.lower() for job in job_posts] 

    for keyword in formatted_keywords:
        for job_post in formatted_jobs:
            if keyword in job_post.lower():
                keyword_dict[keyword] +=1

    return keyword_dict
    

def get_combination_stats (combinations, job_posts) :
    ''' returns a dict with key = list of keywords in combination, 
                            value = count of this combination in job_posts  '''
    
    # initialize
    combination_dict = defaultdict(int)
    
    # clean up combinations, need to split each combination and making it lower case, and striping spaces
    # ['Django-Python ', 'RSS'] -> [['django', python] , ['rss']]
    split_combinations = [[x.lower().strip() for x in combination.split('-')] for combination in combinations ] 
    
    # format job_post to lower case
    formatted_jobs = [job.lower() for job in job_posts] 
    for comment in formatted_jobs:
        for combination in split_combinations:
            if all([keyword in comment for keyword in combination]):
                combination_dict[tuple(combination)] +=1 # tuple is hashable and can be key of dictionary
    
    return combination_dict
   
    
def combinations_stats_repr(stats_dic, job_posts):
    ans = []
    ans.append("Combinations:") 

    total_items = len(job_posts)
    for tuple_words, frequency in stats_dic.items():
        combination_word = "-".join(word.capitalize() for word in tuple_words)
        ans.append(get_str_rep(combination_word, frequency, total_items))
    return ans
    

def keyword_stats_repr(stats_dic, job_posts):
    ans = []
    ans.append("Keywords:")

    total_items = len(job_posts)
    for word, frequency in stats_dic.items():
        ans.append(get_str_rep(word.capitalize(), frequency, total_items))
    return ans

def get_str_rep(word, frequency, total_items):
    percent = int(frequency * 100.0 / total_items)
    return "{Word}: {frequency} ({percent}%)".format(Word=word, frequency= frequency, percent= percent)

def get_total_jobs(jobs_posts):
    return 'Total job posts: {}'.format(len(jobs_posts))


def retrieve_job_postings(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    comments = soup.findAll('tr', {'class': 'athing'})
    return [comment.text for comment in comments if comment.find("img", width=0)]
    
def request_jobs_page(post_id):
    url = settings.BASE_URL.format(post_id) 
    return requests.get(url)
    
'''Why do we need so much code here? Please see simplified version above '''
# def get_parent_comments(post_id):
#     url = settings.BASE_URL.format(post_id) 
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     comments = soup.findAll('tr', {'class': 'athing'})
#     return [comment.text for comment in comments if is_top_comment(comment)]
    
    
# def is_top_comment(comment):
#     if not hasattr(comment, 'findAll'):
#         return False
#     img_nodes = comment.findAll('img')
#     if len(img_nodes) != 1:
#         return False
#     node = img_nodes[0]
#     if not hasattr(node, 'attrs'):
#         return False
#     width_attribute = node.attrs['width']
#     if width_attribute == None or width_attribute != '0':
#         return False
#     return True
    

if __name__ == '__main__':
    jobs_detector()



