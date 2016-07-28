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


def request_page(post_id):
    url = BASE_URL.format(post_id)
    return requests.get(url)
    
    
def keywords_count_and_stats(keywords, only_text, total_job_post_count):
    keyword_counts = {}
    keywords = keywords.split(',')
    
    for keyword in keywords: #initializing keyword_counts dict with 0 for each keyword, and 0 for stats 
                            #therefore, the datastruct looks like keyword_counts[keyword] = [count, stat]
        keyword = keyword.lower()
        keyword_counts[keyword] = [0, 0]
        
    if keywords is not None:
        #==========================
        for keyword in keyword_counts: #iterate through keys
            keyword_counts[keyword][0] = only_text.count(keyword)
            
            temp = keyword_counts[keyword][0] / float(total_job_post_count) * 100
            keyword_counts[keyword][1] = int(temp)
        
            
    keyword_output =  "Keywords:\n"
    for keyword in keyword_counts:
        keyword_output = keyword_output + \
        "{}: {} ({}%) \n ".format(keyword.capitalize(), keyword_counts[keyword][0], keyword_counts[keyword][1])
    
    return keyword_output

# def combination_count_and_stats(combinations, comments, total_job_post_count):
#     combination_dict = {}
    
#     for combination in combinations: #initializing combination_dict with 0 for each keyword, and 0 for stats 
#                                     #therefore, the datastruct looks like combination_dict[combination] = [count, stat]
#         combination = combination.lower()
#         combination_list = combination.split(',')
#         keyword_list = combination_list.split('-')
#         keyword_list_tuple = tuple(keyword_list)
#         combination_dict[keyword_list_tuple] = [0,0] 

#     for comment in comments:
#         comment = str(comment).lower()
#         for keyword_l in combination_dict: #iterate through dictionary
#             flag = True
#             for keyword in keyword_l:
#                 if keyword not in comment:
#                     flag = False
#                     break
#             flag2 = True
#             if flag == True:
#                 combination_dict[keyword_l][0] += 1
#                 flag2 = True
#             continue
#     for combination in combination_dict:
#         temp = combination_dict[combination][0] / float(total_job_post_count) * 100
#         combination_dict[combination][1] = int(temp)

#     return combination_dict
    # return combination_output

@jobs_detector.command()
@click.option('-i', '--post-id', type=str, required=True)
@click.option('-k', '--keywords', type=str, default=','.join(DEFAULT_KEYWORDS))
@click.option('-c', '--combinations', type=str,
              callback=lambda _, x: x.split(',') if x else x)
def hacker_news(post_id, keywords=DEFAULT_KEYWORDS, combinations=None):
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
    
    page = request_page(post_id)
    soup = BeautifulSoup(page.content, "html.parser")
    # import ipdb; ipdb.set_trace()
    comments = soup.find_all('span', class_='c00')
    total_job_post_count = len(comments)
    total_job_post_count_output =  "Total job posts: {}".format(total_job_post_count)
    click.echo(total_job_post_count_output)
    
    only_text = soup.get_text()
    only_text = only_text.lower()
    
    keyword_output = keywords_count_and_stats(keywords, only_text, total_job_post_count)
    click.echo(keyword_output)
    # combination_dict = combination_count_and_stats(combinations, comments, total_job_post_count)
    # combination_output = "Combinations:"
   
    # if combinations is not None:
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
    click.echo(combination_dict.keys())
    for comment in comments:
        comment = str(comment).lower()
        #(u'django', u'remote') 
        #import ipdb; ipdb.set_trace()
        for combination_keywords in combination_dict.keys(): #iterate through dictionary
            click.echo(combination_keywords[0])#django
            click.echo(combination_keywords[1])#remote
            # flag = True
            for keyword in combination_keywords:
                click.echo(keyword)
                click.echo(type(comment))
                click.echo(comment)
                click.echo(str(combination_keywords[1]) in comment)
                if str(keyword) not in comment:
                    click.echo("I hate my life") #Jason Meeks "its becus its unicorn"
                # if keyword not in format_comment:
                #     # flag = False
                #     click.echo(keyword)
                #     break
            else:
            # if flag == True:
                combination_dict[combination_keywords][0] += 1
                click.echo(combination_dict[combination_keywords][0])


    click.echo(combination_dict)
    for key in combination_dict:
        temp = combination_dict[key][0] / float(total_job_post_count) * 100
        combination_dict[key][1] = int(temp)

    combination_output = "Combinations:"
    click.echo(combination_output)
    
    for combination in combination_list:
        
        combination = combination.lower()
        keyword_list = combination.split('-')
        keyword_list_tuple = tuple(keyword_list)
        
        capitalized_keywords = [key.capitalize() for key in keyword_list]
        temp = ""
        for index, keyword in enumerate(capitalized_keywords):
            if index is len(capitalized_keywords) -1:
                temp = temp + keyword
                break
            temp = temp + keyword + "-"
        combination_output = combination_output + \
        "{}: {} ({})%\n".format(combination, combination_dict[keyword_list_tuple][0], combination_dict[keyword_list_tuple][1])
    click.echo(combination_output)
    
    
    
if __name__ == '__main__':
    jobs_detector()    
    
    
    
    
    
    
# ===================reorganizing code for prettier, optional?============================    
    
# python jobs_detector/main.py hacker_news -i 11814828
# PYTHONPATH=. py.test -s tests/test_main.py::HackerNewsTestCase::test_hacker_news_default_keywords


    # url = BASE_URL.format(post_id) # https://news.ycombinator.com/item?id=11814828 
    # response = requests.get(url)
    # soup = BeautifulSoup(response.content, "html.parser")
    
    
    # comments = soup.find_all('span', class_='c00')
    
    # total_job_post_count = len(comments)
    
    #add next to the main body of fcn
    # total_job_post_count_string =  "Total job posts: {}".format(total_job_post_count)
    
    # only_text = soup.get_text()
    # only_text = only_text.lower()
    
    # keyword_counts = {}
    # keywords = keywords.split(',')
    
    # for keyword in keywords: #initializing keyword_counts dict with 0 for each keyword, and 0 for stats 
    #                         #therefore, the datastruct looks like keyword_counts[keyword] = [count, stat]
    #     keyword = keyword.lower()
    #     keyword_counts[keyword] = [0, 0]
        
    # if keywords is not None:
        
        
    #     #==========================
    #     for keyword in keyword_counts: #iterate through keys
    #         keyword_counts[keyword][0] = only_text.count(keyword)
            
    #         temp = keyword_counts[keyword][0] / float(total_job_post_count) * 100
    #         keyword_counts[keyword][1] = int(temp)
        
    #         #return keyword_counts    
            
    # keyword_output =  "Keywords:\n"
    # for keyword in keyword_counts:
    #     keyword_output = keyword_output + \
    #     "{}: {} ({}%) \n ".format(keyword.capitalize(), keyword_counts[keyword][0], keyword_counts[keyword][1])
        
    
    # click.echo(total_job_post_count_string)
    # click.echo(keyword_output)
        
    # if combinations is not None:
    # #combinations looks like remote-python-flask or remote-django
    # #combinations is a list of string of above ^ 
    # #'-c', 'python-remote,python-django,django-remote']
    # #'python-remote', 'python-django', 'django-remote'
    #     combination_dict = {}
    
    #     for combination in combinations: #initializing combination_dict with 0 for each keyword, and 0 for stats 
    #                                     #therefore, the datastruct looks like combination_dict[combination] = [count, stat]
    #         combination = combination.lower()
    #         combination_list = combination.split(',')
    #         keyword_list = combination_list.split('-')
    #         keyword_list_tuple = tuple(keyword_list)
    #         combination_dict[keyword_list_tuple] = [0,0] 
    #     #25 for python-remote, 6 for django
    #     for comment in comments:
    #         comment = str(comment).lower()
    #         for keyword_list in combination_dict: #iterate through dictionary
    #             flag = True
    #             for keyword in keyword_list:
    #                 if keyword not in comment:
    #                     flag = False
    #                     break
    #             flag2 = True
    #             if flag == True:
    #                 combination_dict[keyword_list][0] += 1
    #                 flag2 = True
    #             continue
    #     for combination in combination_dict:
    #         temp = combination_dict[combination][0] / float(total_job_post_count) * 100
    #         combination_dict[combination][1] = int(temp)
    
    #     combination_output = "Combinations:"
        
    #     for combination in combination_list:
    #         keyword_list = combination.split()
    #         capitalized_keywords = [key.capitalize() for key in keyword_list]
    #         temp = ""
    #         for index, keyword in enumerate(capitalized_keywords):
    #             if index is len(capitalized_keywords) -1:
    #                 temp = temp + keyword
    #                 break
    #             temp = temp + keyword + "-"
    #         combination_output = combination_output + \
    #         "{}: {} ({})%\n".format(combination, combination_dict[combination][0], combination_dict[combination][1])
            
        # click.echo(combination_output)