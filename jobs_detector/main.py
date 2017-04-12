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
    if keywords:
        keyword_list = keywords.title().split(',')
    else:
        keyword_list = DEFAULT_KEYWORDS
    output = []
    kwd_dict = {}
    url = settings.BASE_URL.format(post_id)
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.content, 'html.parser')
        data = soup.find_all('span', 'c00')
        total_jobs = len(data)
        output.append('Total job posts: {}\n'.format(total_jobs))
        output.append('Keywords:\n')
        for kwd in keyword_list:
            for item in data:
                if kwd.lower() in item.prettify():
                    if kwd not in kwd_dict:
                        kwd_dict[kwd] = 0
                    kwd_dict[kwd] += 1
        for kwd in keyword_list:
            output.append('{}: {} ({}%)'.format(
                kwd, kwd_dict[kwd], int((kwd_dict[kwd]*100)/total_jobs)))

            
    if combinations:
        combo_dict = {}
        combo_list = [combo.split('-') for combo in combinations]
        output.append("Combinations:\n")
        for pair in combo_list:
            combo_name = '-'.join(pair).title()
            for item in data:
                if (pair[0] in item.prettify() 
                    and pair[1] in item.prettify()):
                    if combo_name not in combo_dict:
                        combo_dict[combo_name] = 0
                    combo_dict[combo_name] += 1
        for pair in combo_dict:
            output.append('{}: {} ({}%)'.format(
                pair, combo_dict[pair], int((combo_dict[pair]*100)/total_jobs)))
        
    for item in output:
        print(item)

if __name__ == '__main__':
    jobs_detector()
