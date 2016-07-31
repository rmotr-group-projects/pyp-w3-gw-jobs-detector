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
    post_id: post id of the hacker_news thread
        eq: 123124
    keywords: list of keyword to find the info of
        eq: ['Python', 'Django']
    combinations: when not None, it's a list of keywords combined together
        eq: ['Python-Remote', 'Python-Django']
    """
    # HINT: You will probably want to use the `BeautifulSoup` tool to
    # parse the HTML content of the website

    parent_comments = get_parent_comments(post_id) # get all top comments
   
    job_posts = parent_comments 
    
    response = []
    
    response.append(get_total_jobs(job_posts))
    
    keyword_stats = get_keyword_stats(keywords, job_posts)
    response += keyword_stats_repr(keyword_stats, job_posts)
    
    if combinations is not None:
        combined_stats = get_combination_stats(combinations, job_posts)
        response += combinations_stats_repr(combined_stats, job_posts)
    
    print(response)
    return response
    
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

def get_parent_comments(post_id):
    url = settings.BASE_URL.format(post_id) 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    comments = soup.findAll('tr', {'class': 'athing'})
    return [comment.text for comment in comments if is_top_comment(comment)]
    
    
def is_top_comment(comment):
    if not hasattr(comment, 'findAll'):
        return False
    img_nodes = comment.findAll('img')
    if len(img_nodes) != 1:
        return False
    node = img_nodes[0]
    if not hasattr(node, 'attrs'):
        return False
    width_attribute = node.attrs['width']
    if width_attribute == None or width_attribute != '0':
        return False
    return True
    

if __name__ == '__main__':
    jobs_detector()



