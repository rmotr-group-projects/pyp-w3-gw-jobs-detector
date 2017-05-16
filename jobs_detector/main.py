import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings

DEFAULT_KEYWORDS = [
    # set some default keywords here
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
              callback=lambda _, __, x: x.split(',') if x else x)
def hacker_news(post_id, keywords, combinations):
    """
    This subcommand aims to get jobs statistics by parsing "who is hiring?"
    HackerNews posts based on given set of keywords.
    """
    # HINT: You will probably want to use the `BeautifulSoup` tool to
    # parse the HTML content of the website
    url = "https://news.ycombinator.com/item?id=" + str(post_id)
    r = requests.get(url)
    data = r.text
    
    soup = BeautifulSoup(data,"html.parser")
    for link in soup.find_all('a'):
        click.echo(link)
    
    
    
    download_page = requests.get('https://news.ycombinator.com/item?id={}'.format(post_id))
    soup_object = BeautifulSoup(download_page, 'html.parser')

    #for combination
    words = combinations.split('-')
    combo_dictionary = {combinations:0}
   
    total_job_count = 0
    parags = soup_object.find_all('div', class_='athing comtr ')
    job_dict = {keyword : 0 for keyword in DEFAULT_KEYWORDS}
    for each_list in parags:
        if each_list.find('img', width='0') and each_list.find('span', class_='c00'):
            total_job_count += 1
            for k in job_dict.keys():
                if k in each_list.text:
                    job_dict[k]+=1

        #for combination, if all the words are in text increase the related dictionary
        if all(each_word in each_list.text for each_word in words):
            combo_dictionary[combinations] +=1

if __name__ == '__main__':
    jobs_detector()
