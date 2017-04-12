import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings

RESULT_FORMAT = "{}: {} ({}%)"
DEFAULT_KEYWORDS = [
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
              callback=lambda _, __, x: x.split(',') if x else x)
def hacker_news(post_id, keywords, combinations):
    keywords_list = keywords.split(',')

    # get all job offers in the Hacker News post
    job_offers = get_job_offers(post_id, keywords_list)

    # count amount of job offers containing each keyword
    search_results = search_for_keywords(job_offers, keywords_list)

    # print results in the stdout
    print_results(job_offers, search_results)

    if combinations:
        combo_terms = []
        for c in combinations:
            combo_terms.append(tuple(c.split('-')))
        combo_results = search_combinations(job_offers, combo_terms)
        print_combo(job_offers, combo_results)


def get_job_offers(post_id, keywords_list):
    """
    Generates a Soup from Hacker News response HTML content, finds all
    job offers and returns them.
    """
    url = settings.BASE_URL.format(post_id)
    response = requests.get(url)
    if not response.status_code == requests.codes.ok:
        raise ValueError('Got unexpected response from Hacker News '
                         'site: {}'.format(response.status_code))
    job_offers = []
    soup = BeautifulSoup(response.text, 'html.parser')
    for td in soup.find_all('td', class_="ind"):  # find comment spacers
        # if spacer width is zero, comment is a top level comment
        if td.img.get('width') == '0':
            # spans with class c00 contain the actual comment text
            job_offers.append(td.parent.find("span", class_="c00").text)
    return job_offers


def search_for_keywords(job_offers, keywords):
    """
    Returns a dictionary containing all keywords as keys and the counter
    of job offers that include that keyword.
    """
    search_results = {key: sum([1 for post in job_offers
                                if key.lower() in post.lower()])
                      for key in keywords}
    return search_results


def _check_combination(job_offer, combination):
    """
    Returns True if all keywords in the combination are included
    in given job offer text, and False otherwise.
    """
    return all([c.lower() in job_offer.lower() for c in combination])


def search_combinations(job_offers, combos):
    print('search combos')
    search_results = {c: sum([1 for post in job_offers
                              if _check_combination(post, c)])
                      for c in combos}
    print('search complete')
    return search_results


def print_results(job_offers, search_results):
    """
    Prints keyword matching results to the standar output respecting
    the expected format.
    """
    print("Total job posts: {}".format(len(job_offers)))
    print("Keywords:")
    for keyword in search_results.keys():
        results = search_results[keyword]
        percentage = int((float(results) / len(job_offers)) * 100)
        print(RESULT_FORMAT.format(keyword.capitalize(), results, percentage))


def print_combo(job_offers, combo_results):
    """
    Prints keyword combination results to the standar output respecting
    the expected format.
    """
    print("Combinations:")
    for combo in combo_results.keys():
        results = combo_results[combo]
        percentage = int((float(results) / len(job_offers)) * 100)
        combo_name = "-".join([x.capitalize() for x in combo])
        print(RESULT_FORMAT.format(combo_name, results, percentage))


if __name__ == '__main__':
    jobs_detector()
