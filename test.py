# from jobs_detector import main
import os
from bs4 import BeautifulSoup
import string
# import urllib

# r = urllib.urlopen('https://news.ycombinator.com/item?id=11814828').read()
# soup = BeautifulSoup(r)
# print type(soup)


class JobPosts(object):
    def __init__(self, page):
        self.count = 0
        self.page = page
        self.job_posts = []
        
        # Retrieves all the parent job posts, then appends to list
        soup = BeautifulSoup(open(page), "html.parser")
        trtags = soup.find_all("tr", class_="athing")
        for trtag in trtags:
            for child in trtag.descendants:
                try:
                    if child.get('src') == "s.gif":
                        # print("found an image tag")
                        # we know this is the right image
                        if child.get('width') == "0":
                            # print("found width == 0")
                            self.job_posts.append(trtag)
                except AttributeError:
                    pass
        
    def __len__(self):
        return len(self.job_posts)
        
    def keyword_count_in_post(self, keyword, post):
        return string.count(str(post).upper(), keyword.upper())
        
    def count_keyword(self, keyword):
        # gives count of keyword occurrences total
        count = 0
        for post in self.job_posts:
            count += self.keyword_count_in_post(keyword, post)
        return count
    
    def count_keywords_combination(self, keywords_string):
        # gives count of keyword combined occurrences total
        count = 0
        keywords = keywords_string.upper().split("-")
        for post in self.job_posts:
            occurred = True
            for keyword in keywords: #django, remote, python
                if keyword not in str(post).upper():
                    occurred = False
            if occurred:
                count += 1
        return count



# DATA TO GET
# Total job posts: 888
# Keywords:
# Remote: 174 (19%)
# Postgres: 81 (9%)
# Python: 144 (16%)
# Javascript: 118 (13%)
# React: 133 (14%)
# Pandas: 5 (0%)            

if __name__ == '__main__':
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'tests/fixtures/11814828.html')
    posts = JobPosts(filename)
    # print(posts.job_posts[0])
    fn = os.path.join(os.path.dirname(__file__), 'my_file')

    print(len(posts))
    print(posts.count_keyword("python"))
    print(posts.count_keywords_combination("python-remote-flask"))