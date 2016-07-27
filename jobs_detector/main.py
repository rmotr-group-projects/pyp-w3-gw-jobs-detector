import click
import requests
from bs4 import BeautifulSoup

from settings import BASE_URL


DEFAULT_KEYWORDS = [
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


#expect keywords to be a list, expect combinations to be a list of string combinations
def helper(post_id, keywords=None, combinations=None):
    url = BASE_URL.format(post_id)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    comments = soup.find_all('span', class_='c00')
    total_job_post_count = len(comments)
    total_job_post_count_string =  "Total job posts: {}".format(total_job_post_count)
    only_text = soup.get_text()
    only_text = only_text.lower()
    
    keyword_counts = {}
    
    for keyword in keywords: #initializing keyword_counts dict with 0 for each keyword, and 0 for stats 
                            #therefore, the datastruct looks like keyword_counts[keyword] = [count, stat]
        keyword = keyword.lower()
        keyword_counts[keyword] = [0, 0]
        
    if keywords is not None:
        
        for keyword in keyword_counts: #iterate through keys
            keyword_counts[keyword][0] = only_text.count(keyword)
            
            temp = keyword_counts[keyword][0] / float(total_job_post_count) * 100
            keyword_counts[keyword][1] = int(temp)
        
            #return keyword_counts    
            
    if combinations is not None:
    #combinations looks like remote-python-flask or remote-django
    #combinations is a list of string of above ^ 
    #'-c', 'python-remote,python-django,django-remote']
    #'python-remote', 'python-django', 'django-remote'
        combination_dict = {}
    
        for combination in combinations: #initializing combination_dict with 0 for each keyword, and 0 for stats 
                                        #therefore, the datastruct looks like combination_dict[combination] = [count, stat]
            combination = combination.lower()
            keyword_list = combination.split('-')
            keyword_list_tuple = tuple(keyword_list)
            combination_dict[keyword_list_tuple] = [0,0] 
        #25 for python-remote, 6 for django
        for comment in comments:
            comment = str(comment).lower()
            for keyword_list in combination_dict: #iterate through dictionary
                flag = True
                for keyword in keyword_list:
                    if keyword not in comment:
                        flag = False
                        break
                flag2 = True
                if flag == True:
                    combination_dict[keyword_list][0] += 1
                    flag2 = True
                continue
        for combination in combination_dict:
            temp = combination_dict[combination][0] / float(total_job_post_count) * 100
            combination_dict[combination][1] = int(temp)
        
    import ipdb; ipdb.set_trace()

# PYTHONPATH=. py.test -s tests/test_main.py::HackerNewsTestCase::test_helper_function

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
    
    # 1) request website
    # 2) use BeautifulSoup to parse the html and get a python object only with the main post (not regular users comments)
    # 3) split the object above into a list of strings
    # 4) loop through all the keywords (or DEFAULT_KEYWORDS if keywords were not given) and for each one check how many times it's in the splited list
    # 5) print the statistics
    
    # later fix imports so we can use 
    print(keywords)
    url = BASE_URL.format(post_id)    # https://news.ycombinator.com/item?id=11814828 
    response = requests.get(url)
    helper(response,keywords)
    #soup = BeautifulSoup(response.content, "html.parser")
    
    #soup.body.center.table.tbody.table.tbody
    

    
# python jobs_detector/main.py hacker_news -i 11814828
# PYTHONPATH=. py.test -s tests/test_main.py::HackerNewsTestCase::test_hacker_news_default_keywords

if __name__ == '__main__':
    jobs_detector()
