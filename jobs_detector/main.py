import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings

DEFAULT_KEYWORDS = ['Remote', 'Postgres', 'Python', 'Javascript', 
                    'React', 'Pandas']




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
    keywords = keywords.split(',')
    #_parser(post_id, keywords, combinations)
    #_results(keywords, combinations)


    n_job_posts = 0
    k_jobs_dict = {}
    c_jobs_dict = {}



#def _parser(post_id, keywords=DEFAULT_KEYWORDS, combinations=None):
    
   
    res = requests.get(settings.BASE_URL.format(post_id))
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    all_posts = soup.find_all("tr",class_='athing')
    job_posts = [post.find('span',class_='c00').get_text() for post in all_posts if post.find('img',width='0') and post.find('span',class_='c00')]
    n_job_posts = len(job_posts)
    
    for post in job_posts:
        for e in keywords:
            if e.capitalize() not in k_jobs_dict: k_jobs_dict[e.capitalize()] = 0
            if e.lower() in post:
                k_jobs_dict[e.capitalize()] += 1
            
    
    if combinations:
        c_jobs_dict = {combo.title(): 0 for combo in combinations}
        for post in job_posts:
            for combo in c_jobs_dict:
                
                keycombo = combo.split('-')
                if all([x.lower() in post for x in keycombo]):
                    c_jobs_dict[combo] +=1 

    
#def _results(keywords=DEFAULT_KEYWORDS,combinations=None): 
    template = "Total job posts: {}, \n\nKeywords:\n".format(n_job_posts)
    print(template)    
    for k, v in k_jobs_dict.items():
        print("{}: {} ({}%),\n".format(k, v, 100*v//n_job_posts))
        
    if combinations is not None:
        print("\nCombinations:\n")
        for k, v in c_jobs_dict.items():
            print("{}: {} ({}%),\n".format(k, v, 100*v//n_job_posts))


if __name__ == '__main__':
    jobs_detector()
