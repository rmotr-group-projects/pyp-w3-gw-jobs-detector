import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings

DEFAULT_KEYWORDS = [
    # set some default keywords here
    'python',
    'remote',
    'javascript',
    'react',
    'postgres',
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
    url = settings.BASE_URL.format(post_id)
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')

    post_counter = 0
    keywords_stats = {}
    combinations_stats = {}
    for span in soup.find_all('span', class_='c00'):
        post_counter += 1

        # keyword stats
        for kw in keywords.split(','):
            keywords_stats.setdefault(kw, 0)
            if kw in span.get_text().lower():
                keywords_stats[kw] += 1

        # combination stats
        if not combinations:
            continue
        for comb_string in combinations:
            combinations_stats.setdefault(comb_string, 0)
            splitted = comb_string.split('-')
            if all([c in span.get_text().lower() for c in splitted]):
                combinations_stats[comb_string] += 1

    click.echo('Total job posts: {}'.format(post_counter))
    click.echo()

    if keywords_stats:
        click.echo('Keywords:')
        for kw, counter in keywords_stats.items():
            click.echo('{}: {} ({}%)'.format(
                kw.title(), counter, int((counter / float(post_counter)) * 100)))
        click.echo()

    if combinations_stats:
        click.echo('Combinations:')
        for cb, counter in combinations_stats.items():
            click.echo('{}: {} ({}%)'.format(
                cb.title(), counter, int((counter / float(post_counter)) * 100)))


if __name__ == '__main__':
    jobs_detector()
