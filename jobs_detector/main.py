from __future__ import  (print_function, division)
import click
import requests
from bs4 import BeautifulSoup
from jobs_detector import settings

DEFAULT_KEYWORDS = [
    # set some default keywords here
'Remote', 'Postgres', 'Python', 'Javascript', 'React', 'Pandas'
]

@click.group()
def jobs_detector():
    pass


@jobs_detector.command()
@click.option('-i', '--post-id', type=str, required=True)
@click.option('-k', '--keywords', type=str, default=','.join(DEFAULT_KEYWORDS))
@click.option('-c', '--combinations', type=str,
              callback=lambda _, x: x.split(',') if x else x)


def hacker_news(post_id="11814828", keywords=DEFAULT_KEYWORDS, combinations=None):
    """
    This subcommand aims to get jobs statistics by parsing "who is hiring?"
    HackerNews posts based on given set of keywords.
    """
    job_posts = []
    page = requests.get(
        "https://news.ycombinator.com/item?id={}".format(post_id))
    soup = BeautifulSoup(page.text, 'html.parser')
    posts = soup.find_all("tr", class_="athing")
    for post in posts:
        if post.find("img", width="0"):
            job_posts.append(post)

    post_matches = {key:0 for key in keywords}

    for each_post in job_posts:
        #post = each_post.lower()
        for keyword in keywords:
            if keyword.lower() in str(each_post).lower():
                post_matches[keyword]+=1

    stats = []
    total_jobs = len(job_posts)
    stats.append('Total job posts: %s' % total_jobs)
    stats.append('keywords:')
    for key in post_matches:
        key_stats =  post_matches[key] /total_jobs
        string = '%s: %s (%d%%)'%(key, post_matches[key], key_stats * 100)
        stats.append(string)

    if combinations:
        stats.append('Combinations:')
        combination_dict = {key: 0 for key in combinations}
        combinations_list = [item.split('-') for item in combinations]
        for post in job_posts:
            for array in combinations_list:
                count=0
                if all(x in str(post).lower() for x in array):
                    new_key = '-'.join(str(p) for p in array)
                    combination_dict[new_key] += 1

        for k in combination_dict:
            n_string = '%s: %s (%d%%)' % (k, combination_dict[k], combination_dict[k]/total_jobs * 100)
            stats.append(n_string)

    print(stats)



if __name__ == '__main__':
    jobs_detector()


#man=hacker_news('11814828', DEFAULT_KEYWORDS, ['python-remote','python-django','django-remote'])
#man2=hacker_news('11814828', ['python', 'django'], ['python-remote','python-django','django-remote'])
