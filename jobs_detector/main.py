import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings

DEFAULT_KEYWORDS = [
    # set some default keywords here
    'Remote', 'Postgres','Python','Javascript','React','Pandas','Django',
    # 'REMOTE', 'POSTGRES','PYTHON','JAVASCRIPT','REACT','PANDAS','DJANGO'
    
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
    html = requests.get('https://news.ycombinator.com/item?id=' + post_id)
    # click.echo('html:')
    # click.echo(html.content)
    # click.echo(dir(html))
    
    print('\npost_id: {}'.format(post_id))
    print('keywords: {}'.format(keywords))
    print('combinations: {}'.format(combinations))
    
    kwdict = {}
    for keyword in DEFAULT_KEYWORDS:
        kwdict[keyword] = 0
    jobpostings = 0
    
    #lines to get bs data
    # url = raw_input(html)
    # r  = requests.get("http://" +url)
    data = html.text
    soup = BeautifulSoup(data)
    comments = soup.find_all('td', class_="ind")

    for comment in comments:
        # print(type(comment))
        # print(dir(comment))
        width = comment.findChildren()[0].attrs['width']
        # print('\n\nCOMMENT with width: ' + width)
        if width == '0':
            jobpostings += 1
            content = str(comment.findNextSiblings()[1].find('span', class_='c00'))
            # print("Content: {}. END".format(content))
            for keyword in kwdict:
                # print("Keyword: {}".format(keyword))
                if keyword.lower() in content.lower():
                    kwdict[keyword] += 1
    print('\n Dictionary: {}'.format(str(kwdict)))
    print(jobpostings)
   
   
   
   
    # print([link.get('href') for link in soup.find_all('a')])


if __name__ == '__main__':
    jobs_detector()
