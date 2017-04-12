import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings

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
    
    data = requests.get('https://news.ycombinator.com/item?id={}'.format(post_id))
    if data.status_code == requests.codes.ok:
        soup = BeautifulSoup(data.text, 'html.parser')

    jobs = []
    
    comments = soup.find_all('tr', class_='athing')
    for comment in comments:
        #for top_comment in comment:
        if comment.find('img', width='0'):
            jobs.append(comment)
    
    
    print(len(jobs))
    
    
    total_jobs = "Total job posts: {}".format(len(jobs))
    print(total_jobs)
       
                

    print('Keywords:')
    kwords = keywords.split(",")
    jobs_keywords = {k: 0 for k in kwords}
    for job in jobs:
        for keyword in kwords:
            if keyword.lower() in job.text:
                jobs_keywords[keyword] += 1

    for kw in kwords:
        for key in jobs_keywords:
            if kw == key:
                percentage = (jobs_keywords[key] * 100) // len(jobs)
                print("{}: {} ({}%)".format(kw.capitalize(), jobs_keywords[key], percentage))
    
    if combinations:
        #_default_keywords(jobs, job_counter)
        
        print('Combinations:')
        
        comb_iter = [item.split('-') for item in combinations]
        jobs_combinations = {combinations[i]: 0 for i in range(len(combinations))}
        for job in jobs:
            for comb in comb_iter:
                if comb[0].lower() in job.text and comb[1].lower() in job.text:
                    comb_key = "{}-{}".format(comb[0], comb[1])
                    jobs_combinations[comb_key] += 1
    
        for comb in combinations:
            for key in jobs_combinations:
                if comb == key:
                    percentage = (jobs_combinations[key] * 100) // len(jobs)
                    print("{}: {} ({}%)".format(comb.title(), jobs_combinations[key], percentage))



if __name__ == '__main__':
    jobs_detector()
    

