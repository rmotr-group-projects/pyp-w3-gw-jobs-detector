import click
import requests
from bs4 import BeautifulSoup
from collections import defaultdict


from jobs_detector import settings

DEFAULT_KEYWORDS = [
    # set some default keywords here
    'Remote',
    'Postgres',
    'Python',
    'Javascript',
    'React',
    'Pandas',
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
    
    comments = []
    kw_dict = {}
    combo_dict = defaultdict(int)
    
    keylist = keywords.lower().split(',')
    news = requests.get(settings.BASE_URL.format(post_id))
    parsedhtml  = BeautifulSoup(news.text, 'html.parser')
    allposts = parsedhtml.find_all('tr', class_='athing')
    for post in allposts:
        if post.find('img', width='0'):
            if post.find('span', class_='c00'):
                comments.append(post.text)
    
    numcomments = len(comments)
    result = 'Total job posts: {}\n Keywords:\n'.format(numcomments)




                
    for comment in comments:
        for word in keylist:
            if word not in kw_dict:
                kw_dict[word] = 0
            if word in comment.lower():
                kw_dict[word] += 1
                
        if combinations:
            for combo in combinations:
                splitcombo = combo.split('-')
                if all([word.lower() in comment.lower() for word in splitcombo]):
                        combo_dict[combo] += 1
    
    for key, value in kw_dict.items():
        tempresult = '{}: {} ({}%)'.format(key.title(),value,int((float(value)/numcomments)*100))
        result += tempresult + '\n'

    if combinations:
        header = 'Combinations:\n'
        result += header
        for key,value in combo_dict.items():
            tempresult = '{}: {} ({}%)'.format(key.title(),value,int((float(value)/numcomments)*100))
            result += tempresult + '\n'
    

    print(result)

    
    

if __name__ == '__main__':
    jobs_detector()