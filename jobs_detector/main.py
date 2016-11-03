import click
import requests
from bs4 import BeautifulSoup

#from jobs_detector import settings

DEFAULT_KEYWORDS = [
    'remote',
    'postgres',
    'python',
    'javascript',
    'react',
    'pandas'
]

HACKERNEWS_URL = "https://news.ycombinator.com/item?id={}"

class JobPosting(object):

    def __init__(self, posting, keywords):
        self.keywords = {k:0 for k in keywords}
        self.posting = posting
        self._scan_keywords()

    def _scan_keywords(self):
        for keyword in self.keywords.keys():
            if keyword in self.posting.text:
                self.keywords[keyword] = True

    def check_combo(self, combo):
        for key in combo:
            if key not in self.keywords.keys():
                if key not in self.posting.text:
                    return False
            elif self.keywords[key] == False:
                return False
        return True


def is_top_level_comment(td):
    if td.img.get('width') == '0':
        return True
    else:
        return False

def get_postings(post_id, keywords_list):
    url = HACKERNEWS_URL.format(post_id)
    r = requests.get(url)
    if r.status_code == 200:
        postings = []
        soup = BeautifulSoup(r.text, 'html.parser')
        for td in soup.find_all('td', class_="ind"):
            if is_top_level_comment(td):
                posting = td.parent.find("span", class_="c00")
                postings.append(JobPosting(posting, keywords_list))
                
        return postings
    else:
        return None

def search_for_keywords(postings, keywords):
    search_results = {}
    for key in keywords:
        search_results[key] = sum([1 for post in postings if post.keywords[key] == True])
    return search_results

def search_combinations(postings, combos):
    search_results = {}
    for c in combos:
        search_results[c] = sum([1 for post in postings if post.check_combo(c)])
    return search_results

def print_results(postings, search_results):
    post_count = len(postings)
    print("Total job posts: {}".format(post_count))
    print("Keywords:")
    for keyword in search_results.keys():
        results = search_results[keyword]
        percentage = int((float(results)/post_count)*100)
        print("{}: {} ({}%)".format(keyword.capitalize(), results, percentage))

def print_combo(postings, combo_results):
    post_count = len(postings)
    print("Combinations:")
    for combo in combo_results.keys():
        results = combo_results[combo]
        percentage = int((float(results)/post_count)*100)
        combo_name = "-".join([x.capitalize() for x in combo])
        print("{}: {} ({}%)".format(combo_name, results, percentage))


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


if __name__ == '__main__':
    jobs_detector()
