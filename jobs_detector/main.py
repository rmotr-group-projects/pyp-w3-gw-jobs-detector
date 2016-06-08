
import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings

DEFAULT_KEYWORDS = [ # this is lifted from test_main.py and the readme.
    'remote',
    'postgres',
    'python',
    'javascript',
    'react',
    'pandas'
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
        
    keywords = keywords.split(',')        
    main_page = requests.get(settings.BASE_URL.format(post_id))
    
    # turn it into a BS4 object we can parse with html.
    soupy = BeautifulSoup(main_page.text, 'html.parser')
    
    # Find all the TR (table row) classes.  This will be the main thread, and each
    # followup post/reply.
    posting = soupy.find_all("tr", class_="athing") 
    top_posts = [p.get_text() for p in posting if p.find("img", width="0")]
    postcount = len(top_posts)

    #print('Post Comprehension posting count is: {}'.format(postcount))
    keyword_dict = dict.fromkeys(keywords, 0)
    
    # Parse each line, loading dict as keywords are found.
    for line in top_posts:
        for keyword in keyword_dict.keys():
            if keyword.lower() in line.lower():
                keyword_dict[keyword] += 1

    # TODO: need to import some itertools.combinations magic to ensure 
    # the combinations portion of this also works.

    #print('Total job posts: {}\n\nKeywords:'.format(postcount))
    #for keyword, count in keyword_dict.items():
    #    print('{}: {} ({}%))'.format(keyword.title(), count, int(((float(count)/postcount) * 100))))
    
    print('Total job posts: {}\n\nKeywords:').format(postcount)
    for keyword, count in keyword_dict.items():
        print('{}: {} ({}%)').format(keyword.title(), count, int(((float(count)/postcount) * 100)))


if __name__ == '__main__':
    jobs_detector()