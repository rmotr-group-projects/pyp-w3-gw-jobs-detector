# from jobs_detector import main
from bs4 import BeautifulSoup
# import urllib

# r = urllib.urlopen('https://news.ycombinator.com/item?id=11814828').read()
# soup = BeautifulSoup(r)
# print type(soup)

soup = BeautifulSoup(open("11814828.html"), "html.parser")
# print soup
parent_comment_list = []
trtags = soup.find_all("tr", class_="athing comtr ")
for trtag in trtags:
    for child in trtag.descendants:
        try:
            if child.get('src') == "s.gif":
                # print("found an image tag")
                # we know this is the right image
                if child.get('width') == "0":
                    # print("found width == 0")
                    parent_comment_list.append(trtag)
        except AttributeError:
            pass
# tag_container = []
# for tag in trtags:
#     if tag.contains("img src=\"s.gif\" height=\"1\" width=\"0\""):
#         tag_container += tag


# print("parent_comment_list contains ", len(parent_comment_list), " values")
# print parent_comment_list

# f = open( 'output.dat', 'w' )
# f.write(repr(parent_comment_list))
# f.close()

print parent_comment_list[0]
print(type(parent_comment_list[0]))
        
#   continue
# giftag = trtags.find_all("img")
# print(giftag)





# DATA TO GET
# Total job posts: 888
# Keywords:
# Remote: 174 (19%)
# Postgres: 81 (9%)
# Python: 144 (16%)
# Javascript: 118 (13%)
# React: 133 (14%)
# Pandas: 5 (0%)