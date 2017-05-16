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
              callback=lambda _, __, x: x.split(',') if x else x)
def hacker_news(post_id, keywords, combinations):
    """
    This subcommand aims to get jobs statistics by parsing "who is hiring?"
    HackerNews posts based on given set of keywords.
    """
    keywords = [word.capitalize() for word in keywords.split(',')]
    combinations = [comb.title() for comb in combinations] if combinations else []
    
    r = requests.get('https://news.ycombinator.com/item', params = {'id':post_id})
    page = r.text
    soup = BeautifulSoup(page, 'html.parser')
    commentstuff = soup.find_all('tr', class_ = 'athing')
    top_comments = [com.find('span', class_ = 'c00').get_text() for com in commentstuff if com.find('img', width = '0') and com.find('span', class_ = 'c00')]
    
    mentions = {key:0 for key in keywords}
    combo_mentions = {combo:0 for combo in combinations}
    combo_words = set()
    for combo in combinations:
        for word in combo.split('-'):
            combo_words.add(word)
            
    for com in top_comments:
        for key in mentions:
            if key.lower() in com.lower():
                mentions[key] += 1
        combo_words_present = [word for word in combo_words if word.lower() in com.lower()]
        for combo in combo_mentions:
            if all(word in combo_words_present for word in combo.split('-')):
                combo_mentions[combo] += 1
        
    total_postings = len(top_comments)
    print_results(mentions, combo_mentions, total_postings)
    
def print_results(keyword_dict, combination_dict, total):
    print('Total job posts: {}'.format(total))
    print('\nKeywords:')
    for key, value in keyword_dict.items():
        print('{}: {} ({}%)'.format(key, value, 100*value//total))
        
    if combination_dict:
        print('\nCombinations:')
        for combo, value in combination_dict.items():
            print('{}: {} ({}%)'.format(combo, value, 100*value//total))


if __name__ == '__main__':
    jobs_detector()
