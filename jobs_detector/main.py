import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings

DEFAULT_KEYWORDS = [
    'Remote', 'Postgres','Python','Javascript','React','Pandas'
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
    jobpostings = 0
    keywordsDict = generate_keywordsDict(keywords)
    combinationsDict = generate_combinationsDict(combinations)
    
    # print('\npost_id: {}'.format(str(post_id)))
    # print('keywords: {}'.format(str(keywords)))
    # print('keywordsDict: {}'.format(str(keywordsDict)))
    # print('combinations: {}'.format(str(combinations)))
    # print('combinationsDict: {}'.format(str(combinationsDict)))

    html = requests.get('https://news.ycombinator.com/item?id=' + post_id)
    soup = BeautifulSoup(html.text, 'html.parser')
    ind_elements = soup.find_all('td', class_="ind")
    for ind_elem in ind_elements:
        
        width = ind_elem.findChildren()[0].attrs['width']
        if width == '0':
            
            jobpostings += 1
            
            post_elem = ind_elem.findNextSiblings()[1].find('span', class_='comment')
            post_content = post_elem.get_text().lower()
                
            for keyword in keywordsDict:
                if keyword in post_content:
                    keywordsDict[keyword] += 1
                    
            for combination in combinationsDict:
                if all(cKeyword in post_content for cKeyword in combination):
                    combinationsDict[combination] += 1
            
    click.echo(generate_result(jobpostings, keywordsDict, combinationsDict))


def generate_keywordsDict(keywords):
    keywordsDict = {}
    keywords = keywords.split(',')
    for keyword in keywords:
        keywordsDict[keyword.lower()] = 0
    return keywordsDict
    
    
def generate_combinationsDict(combinations): 
    combinationsDict = {}
    if combinations:
        for combination in combinations:
            combinationTuple = tuple(combination.lower().split('-'))
            combinationsDict[combinationTuple] = 0
    return combinationsDict
    
    
def generate_result(jobpostings, keywordsDict, combinationsDict):
    
    results = ['Total job posts: {}'.format(jobpostings)]

    if len(keywordsDict) > 0:
        results.append('Keywords:')
        for keyword in keywordsDict:
            name = keyword.title()
            number = keywordsDict[keyword]
            percentage = 100*number/jobpostings
            results.append('{}: {} ({}%)'.format(name ,number, int(percentage)))
            
    if len(combinationsDict) > 0:
        results.append('Combinations:')
        for combination in combinationsDict:
            name = '-'.join(combination).title()
            number = combinationsDict[combination]
            percentage = 100*number/jobpostings
            results.append('{}: {} ({}%)'.format(name ,number, int(percentage)))
            
    return results
   

if __name__ == '__main__':
    jobs_detector()
