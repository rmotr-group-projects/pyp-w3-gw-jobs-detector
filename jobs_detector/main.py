import click
import requests
from bs4 import BeautifulSoup
import pdb

from jobs_detector import settings

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
              callback=lambda _, x: x.split(',') if x else x)
def hacker_news(post_id, keywords, combinations):
    keywords_list = keywords.split(',')
    postings = get_postings(post_id, keywords_list)

    search_results = search_for_keywords(postings, keywords_list)
    print_results(postings, search_results)

    if combinations:
        combo_terms = []
        for c in combinations:
            combo_terms.append(tuple(c.split('-')))
        combo_results = search_combinations(postings, combo_terms)
        print_combo(postings, combo_results)


def get_postings(post_id, keywords_list):
    url = settings.BASE_URL.format(post_id)
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        postings = []
        soup = BeautifulSoup(r.text, 'html.parser')
        for td in soup.find_all('td', class_="ind"):  # find comment spacers
            # if spacer width is zero, comment is a top level comment
            if td.img.get('width') == '0':
                # spans with class c00 contain the actual comment text
                postings.append(td.parent.find("span", class_="c00").text)
        return postings


def _check_combination(posting, combination):
    return all([c in posting for c in combination])


def search_for_keywords(postings, keywords):
    search_results = {key: sum([1 for post in postings if key in post])
                      for key in keywords}
    return search_results


def search_combinations(postings, combos):
    print('search combos')
    search_results = {c: sum([1 for post in postings
                              if _check_combination(post, c)])
                      for c in combos}
    print('search complete')
    return search_results


RESULT_FORMAT = "{}: {} ({}%)"


def print_results(postings, search_results):
    post_count = len(postings)
    print("Total job posts: {}".format(post_count))
    print("Keywords:")
    for keyword in search_results.keys():
        results = search_results[keyword]
        percentage = int((float(results)/post_count)*100)
        print(RESULT_FORMAT.format(keyword.capitalize(), results, percentage))


def print_combo(postings, combo_results):
    post_count = len(postings)
    print("Combinations:")
    for combo in combo_results.keys():
        results = combo_results[combo]
        percentage = int((float(results)/post_count)*100)
        combo_name = "-".join([x.capitalize() for x in combo])
        print(RESULT_FORMAT.format(combo_name, results, percentage))

if __name__ == '__main__':
    jobs_detector()
