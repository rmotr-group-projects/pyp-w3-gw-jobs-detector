# -*- coding: utf-8 -*-
import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings
from .settings import BASE_URL
import re
f
'''
r = requests.get('https://news.ycombinator.com/item?id=11814828') # r == request of URL
r.text == html
'''

'''
<table border="0" class='comment-tree'>  <tr class='athing'><td><table border="0">

</span><div class='reply'>   

        <tr class='athing'><td><table border="0">  <tr><td class='ind'><img src="s.gif" height="1" width="0"></td><td valign="top" class="votelinks"><center><a id="up_11815632" href="vote?for=11815632&amp;dir=up&amp;goto=item%3Fid%3D11814828"><div class="votearrow" title="upvote"></div></a></center></td><td class="default"><div style="margin-top:2px; margin-bottom:-10px;"><span class="comhead">
          <a href="user?id=greglindahl">greglindahl</a> <span class="age"><a href="item?id=11815632">2 days ago</a></span> <span class="par"></span>          <span class='storyon'></span>
                  </span></div><br><span class="comment">
                  <span class="c00">Internet Archive | San Francisco | Onsite or Remote | Full-time<p>The Internet Archive is a non-profit library with a huge mission: to give everyone access to all knowledge — the books, web pages, audio, television, and softw
are of our shared human culture. Forever. Based in San Francisco, with satellite offices around the world, the Internet Archive&#x27;s staffers are building the dig
ital library of the future -- a place where we can all go to learn and explore.<p>We are looking for smart, collaborative and resourceful engineers to help advance and develop web-delivered services, including the next versions of the Wayback Machine, website, and digital library tools. Ideal candidates will possess a desire to work collaboratively with a small internal team and a large, vocal, and active user community; demonstrate independence, creativity, initiative, thoughtful design, and technological savvy -- all in addition to being great programmers and engineers. We are seeking both back-end and front-end developers, with proven experience delivering projects in Python and JavaScript. We also have many projects working primarily in PHP.<p>To see all current postings: <a href="https:&#x2F;&#x2F;archive.org&#x2F;about&#x2F;jobs.php" rel="nofollow">https:&#x2F;&#x2F;archive.org&#x2F;about&#x2F;jobs.php</a><p>Current technical openings include:<p><pre><code>  * Manager: Operations and Infrastructure (on-site, SF and Richmond CA)
  * Senior Application Developer: archive.org (on-site, SF)
  * Senior Engineer: Wayback Machine (on-site, SF)
  * Web Archiving Software Engineer (on-site SF or remote)
</code></pre>
We are also open to creating positions for exceptional candidates.<p>If you are interested in engineering or senior engineering roles, please email: jobs (@) archive.org<span>
              </span><div class='reply'>        <p><font size="1">
                      <u><a href="reply?id=11815632&amp;goto=item%3Fid%3D11814828">reply</a></u>
                  </font>
      </div></td></tr>
      </table></td></tr>
'''
DEFAULT_KEYWORDS = ['Remote', 'Postgres', 'Python', 'Javascript', 'React', 'Pandas']


@click.group()
def jobs_detector(parser_function):
    return parser_function


@jobs_detector.command()
@click.option('-i', '--post-id', type=str, required=True, help='[required]')
@click.option('-k', '--keywords', type=str, default=','.join(DEFAULT_KEYWORDS))
@click.option('-c', '--combinations', type=str,
              callback=lambda _, x: x.split(',') if x else x)
def hacker_news(post_id, keywords, combinations):
    r = requests.get(BASE_URL.format(post_id))
    if r.status_code != 200:
        raise InvalidURLException
    
    # Make a HTTP request from URL
    # Make a HTTP request from URL above
    r = requests.get()
    # BeautifulSoup above request
    soup = BeautifulSoup(r.text, 'html.parser')
    # Get all the things (beginning of thread and comments)
    comment_tree = soup.find_all("tr", class_= 'athing comtr ') # list of bs4.element.Tag objects; use .text to get plain-text
    
        
    """
    This subcommand aims to get jobs statistics by parsing "who is hiring?"
    HackerNews posts based on given set of keywords.
    """
    # HINT: You will probably want to use the `BeautifulSoup` tool to
    # parse the HTML content of the website
    
    count_dict = {key:0 for key in keywords}
    for comments in comment_tree:
        for word in keywords:
            if word in comments:
                count_dict['word'] += 1
                
        
    
    expected_list = ['Total job posts: ', 'Keywords: ']
    for key, val in count_dict.items():
        expected_list += '{0}: {1} ({}%)'.format(key, val)
    
    return expected_list


if __name__ == '__main__':
    jobs_detector()
