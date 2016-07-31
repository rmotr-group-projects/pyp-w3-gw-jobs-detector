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
    ''' returns a dict with key = keyword, value = count of keywords in job_posts  '''
    # JUST PRINTING job_posts TO TEST IT
    #print("JUST PRINTING job_posts")
    # #print(job_posts)
    # comment_flag = 0
    # token_flag = 0
    # for comment_para in job_posts :
    #     tokens = comment_para.strip().split(' ')
    #     comment_flag+=1
    #     if comment_flag < 3 :
    #         print(comment_para)
    #         for token in tokens : 
    #             if token_flag < 10 :
    #                 #print(token)
    #                 token_flag+=1
            
    # initialize 
    keyword_dict = defaultdict(int)
    print("keywords: {}".format(keywords))
    # clean up keywords, you only need lower case
    formatted_keywords = [str(keyword).lower() for keyword in keywords.split(",")]
    print("formatted_keywords: {}".format(formatted_keywords))
    
    # make set for faster search
    keywords_set = set(formatted_keywords)
    
    # # clean up job_posts, you only need lower case
    # # job_posts is a list of lists 
    # formatted_comment_words = []
    # for comment_paragraph in job_posts :
    #     for comment_word in comment_paragraph :
    #         formatted_comment_words.append(str(comment_word).lower()) 
            
    # # increment counter of keywords if found in job_posts
    # #print("Is this getting printed")
    # for word in formatted_comment_words :
    #     #print("Word", word)
    #     if word in keywords_set :
    #         keyword_dict[word]+=1
    #     # for keyword in keywords_set:
    #     #     if keyword in comment:
    #     #         keyword_dict[comment]+=1
    for keyword in formatted_keywords:
        for job_post in job_posts:
            if keyword in job_post.lower():
                keyword_dict[keyword] +=1

    return keyword_dict
    

def get_combination_stats (combinations, job_posts) :
    ''' returns a dict with key = list of keywords in combination, 
                            value = count of this combination in job_posts  '''
    
    # initialize
    combination_dict = defaultdict(int)
    
    # clean up combinations, need to split each combination 
    split_combinations = [[x.lower().strip() for x in combination.split('-')] for combination in combinations ] 
    print("split_combinations: {}".format(split_combinations))
    # make a list of set of job_posts for faster search
    # will look like this : list_of_job_posts = [ set('python', 'for', 'this', 'job'), 
                                # set('php', 'and', 'flask' 'for', 'other', job), ... ]
    # list_of_job_posts = []
    # for comment_paragraph in job_posts :
    #     words_in_paragraph = [str(word).lower() for word in comment_paragraph ]
    #     list_of_job_posts.append(set(words_in_paragraph))
        
    # search and check if ALL split_combinations occur in each comment
    formatted_jobs = [job.lower() for job in job_posts] 
    for comment in formatted_jobs:
        for combination in split_combinations:
            if all([keyword in comment for keyword in combination]):
                combination_dict[tuple(combination)] +=1

    # for combination in split_combinations:



    # for split_combination in split_combinations :
    #     for comments in job_posts :
    #         if all (split_combination in comments.lower()):
    #             combination_dict[split_combination] += 1
    
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
    
    # for comment in parent_comments:
    #     print(comment)
    # Could we extract just the part of the post which has <p> tags ?
    
    job_posts = parent_comments 
    
    response = []
    
    response.append(get_total_jobs(job_posts))
    
    keyword_stats = get_keyword_stats(keywords, job_posts)
    response += keyword_stats_repr(keyword_stats, job_posts)
    
    if combinations is not None:
        combined_stats = get_combination_stats(combinations, job_posts)
        response += combinations_stats_repr(combined_stats, job_posts)#todo: rename it
    # response += custom_representation("combined", combined_stats)
    print(response)
    #print("job:0", job_posts[0])
    #print("job:1", job_posts[1])
    # total = len(job_posts)
    
    # msg_so_far = []
    # # 'Total job posts: 883'
    # msg_so_far.append("Total job posts: {}".format(total))
    # #print(total)
    
    # # format keywords
    # keywords = keywords.split(',')
    
    # # run keyword_stats (always)
    # keyword_dict = keyword_stats(keywords, job_posts)
    #print("there")
    #print(keywords)
    
    #print(keyword_dict)
    #print("Printing keyword dict")
    #for k, v in keyword_dict.items() :
    #    print(k, v) 
    
    # # format and print keyword_dict
    # msg_so_far.append("Keywords:")
    # for k, v in keyword_dict.items() :
    #     percent = v*100.0/total
    #     msg_so_far.append('{}: {} ({}%)\n'.format(str(k).capitalize(), v, percent))
    
    
    # # if combinations is True, run combination_stats 
    # if combinations :
    #     combination_dict = combination_stats(combinations, job_posts)
        
    #     #format and print combination_dict
    #     msg_so_far.append("Combinations:")
    #     for k, v in combination_dict.items() :
    #         capitalized_combination = [ str(key_wo).capitalize() for key_wo in k ]
    #         formatted_combi = '-'.join(capitalized_combination)
    #         percent = v*100.0/total
    #         msg_so_far.append('{}: {} ({}%)\n'.format(formatted_combi, v, percent))
    
    #print(msg_so_far)
    return response
    
    '''
    'Total job posts: 883',

    'Keywords:',
    'Python: 143 (16%)',
    'Django: 36 (4%)',

    'Combinations:',
    'Python-Remote: 25 (2%)',
    'Django-Remote: 6 (0%)',
    'Python-Django: 35 (3%)',
    '''
    
    # Comment 1 : Khanacademy job in python and php
    # Comment 2 : YouTube job in python
    # comments = [["Khanacademy job in python and php"],["YouTube job in python"]]
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



