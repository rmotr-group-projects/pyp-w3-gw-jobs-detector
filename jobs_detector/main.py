
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
    combinations = combinations or [] # set this first so next line can iterate
    combinations = [combinations.title() for combination in combinations]
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

    for combination in combinations:
        for keyword in combinations.split('-'):
            if all(keyword in top_posts):
                keyword_dict[combination] += 1 # not sure if this is right

    print('Total job posts: {}\n\nKeywords:').format(postcount)
    for keyword, count in keyword_dict.items():
        print('{}: {} ({}%)').format(keyword.title(), count, int(((float(count)/postcount) * 100)))

    if combinations:
        print('\n\nCombinations:')
        for combination, count in keyword_dict.items():
            print('{}: {} ({}%)').format(combination.title(), count, int(((float(count)/postcount) * 100)))

    # TODO: need to import some itertools.combinations magic to ensure
    # the combinations portion of this also works.

    # make the combinations.  (itertools.combinations?)
    # all(stuff) is a good way to check if evertything is there.
    # all(keyword in post for keyword in combos)

    # make a new combos dict out of the final combo list.
    # then iter, like line 51-ish, but checking the combos instead of just keywords.

    '''
    'Total job posts: 883',

            'Keywords:',
            'Python: 145 (20%)',
            'Django: 37 (5%)',

            'Combinations:',
            'Python-Remote: 25 (2%)',
            'Django-Remote: 6 (0%)',
            'Python-Django: 35 (3%)',
    '''


if __name__ == '__main__':
    jobs_detector()
