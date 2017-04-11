from bs4 import BeautifulSoup
import random
import copy

MAX_TOTAL_POSTS = 883

KEYWORDS = {
	'remote': 174,
	'postgres': 81,
	'python': 143,
	'javascript': 118,
	'react': 133,
	'pandas': 5,
	'django': 36}

KEYWORDS_COMBINATIONS = {
	('python','remote'): 25,
	('django', 'remote'): 6,
	('python', 'django'): 35
}

class JobPosting(object):
	KEYWORDS_INIT = {
		'remote': False,
		'postgres': False,
		'python': False,
		'javascript': False,
		'react': False,
		'pandas': False,
		'django': False
	}

	def __init__(self, posting):
		self.keywords = copy.copy(self.KEYWORDS_INIT)
		self.posting = posting
		self._scan_keywords()

	def _scan_keywords(self):
		for keyword in self.keywords.keys():
			if keyword in self.posting.text:
				self.keywords[keyword] = True

	def check_combo(self, combo):
		for key in combo:
			if self.keywords[key] == False:
				return False
		return True

	def no_keywords(self):
		for key in self.keywords.keys():
			if self.keywords[key] == True:
				return False
		return True


fixture_header = """<html op="item"><head><meta name="referrer" content="origin"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" type="text/css" href="news.css?jl2CRL58yH4prTqwRTQH">
        <link rel="shortcut icon" href="favicon.ico">
        <script type="text/javascript">
function hide(id) {
  var el = document.getElementById(id);
  if (el) { el.style.visibility = 'hidden'; }
}
function vote(node) {
  var v = node.id.split(/_/);
  var item = v[1];
  hide('up_'   + item);
  hide('down_' + item);
  var ping = new Image();
  ping.src = node.href;
  return false;
  }
    </script><title>Ask HN: Who is hiring? (June 2016) | Hacker News</title></head><body><center><table id="hnmain" border="0" cellpadding="0" cellspacing="0" width="85%" bgcolor="#f6f6ef">
        <tr><td bgcolor="#ff6600"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="padding:2px"><tr><td style="width:18px;padding-right:4px"><a href="http://www.ycombinator.com"><img src="y18.gif" width="18" height="18" style="border:1px white solid;"></a></td>
                  <td style="line-height:12pt; height:10px;"><span class="pagetop"><b class="hnname"><a href="news">Hacker News</a></b>
              <a href="newest">new</a> | <a href="newcomments">comments</a> | <a href="show">show</a> | <a href="ask">ask</a> | <a href="jobs">jobs</a> | <a href="submit">submit</a>            </span></td><td style="text-align:right;padding-right:4px;"><span class="pagetop">
                              <a href="login?goto=item%3Fid%3D11814828">login</a>
                          </span></td>
              </tr></table></td></tr>
<tr style="height:10px"></tr><tr><td><table border="0">
        <tr class='athing'>
      <td align="right" valign="top" class="title"><span class="rank"></span></td>      <td valign="top" class="votelinks"><center><a id="up_11814828" href="vote?for=11814828&amp;dir=up&amp;goto=item%3Fid%3D11814828"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><a href="item?id=11814828" class="storylink">Ask HN: Who is hiring? (June 2016)</a></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_11814828">627 points</span> by <a href="user?id=whoishiring">whoishiring</a> <span class="age"><a href="item?id=11814828">2 days ago</a></span>  | <a href="https://hn.algolia.com/?query=Ask%20HN%3A%20Who%20is%20hiring%3F%20(June%202016)&sort=byDate&dateRange=all&type=story&storyText=false&prefix&page=0">past</a> | <a href="https://www.google.com/search?q=Ask%20HN%3A%20Who%20is%20hiring%3F%20(June%202016)">web</a> | <a href="item?id=11814828">914 comments</a>              </td></tr>
      <tr style="height:2px"></tr><tr><td colspan="2"></td><td>Please lead with the location of the position and include the keywords
REMOTE, INTERNS and&#x2F;or VISA when the corresponding sort of candidate is welcome.
When remote work is not an option, please include ONSITE. A one-sentence summary of
your interview process would also be helpful.<p>Submitters: please only post if you personally are part of the hiring company—no
recruiting firms or job boards.<p>Readers: please only email submitters if you personally are interested in the
job—no recruiters or sales calls.<p>You can also use kristopolous&#x27; console script to search the thread:
https:&#x2F;&#x2F;news.ycombinator.com&#x2F;item?id=10313519.</td></tr>
        <tr style="height:10px"></tr><tr><td colspan="2"></td><td>
          <form method="post" action="comment"><input type="hidden" name="parent" value="11814828"><input type="hidden" name="goto" value="item?id=11814828"><input type="hidden" name="hmac" value="ad40d9236f21c19f024423494d2dd53c0e239112"><textarea name="text" rows="6" cols="60"></textarea>
                <br><br><input type="submit" value="add comment"></form>
      </td></tr>
  </table><br><br>
  <table border="0" class='comment-tree'>"""

fixture_footer = """</table><br><br>
</td></tr>
<tr><td><img src="s.gif" height="10" width="0"><table width="100%" cellspacing="0" cellpadding="1"><tr><td bgcolor="#ff6600"></td></tr></table><br><center><span class="yclinks"><a href="newsguidelines.html">Guidelines</a>
        | <a href="newsfaq.html">FAQ</a>
        | <a href="mailto:hn@ycombinator.com">Support</a>
        | <a href="https://github.com/HackerNews/API">API</a>
        | <a href="security.html">Security</a>
        | <a href="lists">Lists</a>
        | <a href="bookmarklet.html">Bookmarklet</a>
        | <a href="dmca.html">DMCA</a>
        | <a href="http://www.ycombinator.com/apply/">Apply to YC</a>
        | <a href="mailto:hn@ycombinator.com">Contact</a></span><br><br><form method="get" action="//hn.algolia.com/">Search:
          <input type="text" name="q" value="" size="17" autocorrect="off" spellcheck="false" autocapitalize="off" autocomplete="false"></form>
            </center></td></tr>      </table></center></body></html>
"""


soup = BeautifulSoup(open('fixture_data.html'), 'html.parser')

postings = []

for td in soup.find_all('td', class_='ind'):
	if td.img.get('width') == '0':
		postings.append(JobPosting(td.parent.parent.parent.parent))



post_count = 0

keyword_count = {key: 0 for key in KEYWORDS.keys()}
combination_count = {t: 0 for t in KEYWORDS_COMBINATIONS.keys()}

fixtures = []

def go_over_max(posting):
	for keyword in posting.keywords.keys():
		if posting.keywords[keyword] and keyword_count[keyword] + 1 > KEYWORDS[keyword]:
			return True
		for t in KEYWORDS_COMBINATIONS.keys():
			if keyword in t:
				if len(t) == len([k for k in t if posting.keywords[k] == True]):
					if combination_count[t] + 1 > KEYWORDS_COMBINATIONS[t]:
						return True
	return False

def pick_random(source, retry=0):
	for post in source:
		if not go_over_max(post):
			return post
	raise ValueError("[Total posts:{}] Unable to find posting in {} that does not break constraints.".format(len(fixtures), source))


def tally_keywords(post):
	global keyword_count
	global combination_count
	track_combo = []
	for key in post.keywords.keys():
		if post.keywords[key] == True:
			keyword_count[key] +=1
			for combo in combination_count.keys():
				if combo not in track_combo:
					if key in combo:
						all_combo_pieces = True
						for c in combo:
							if post.keywords[c] == False:
								all_combo_pieces = False
						if all_combo_pieces:
							combination_count[combo] += 1
							track_combo.append(combo)

placeholder_combinations = copy.copy(KEYWORDS_COMBINATIONS)
# populate based on combinations
for i in range(len(KEYWORDS_COMBINATIONS)):
	key = min(placeholder_combinations, key=placeholder_combinations.get)
	print("Populating {}".format(key))
	while combination_count[key] < KEYWORDS_COMBINATIONS[key]:
		post = pick_random([p for p in postings if p.check_combo(key) == True])
		tally_keywords(post)
		fixtures.append(post)
	print("Finished ({} entries).".format(combination_count[key]))
	placeholder_combinations.pop(key)


placeholder_keywords = copy.copy(KEYWORDS)
# populate remaining keywords
for i in range(len(KEYWORDS)):
	key = min(placeholder_keywords, key=placeholder_keywords.get)
	print("Populating {}".format(key))
	while keyword_count[key] < KEYWORDS[key]:
		post = pick_random([p for p in postings if p.keywords[key] == True])
		tally_keywords(post)
		fixtures.append(post)
	print("Finished ({} entries).".format(keyword_count[key]))
	placeholder_keywords.pop(key)



# check if still short of max posts and fill with empty posts
print("Padding out totals.")
while len(fixtures) < MAX_TOTAL_POSTS:
	post = pick_random([p for p in postings if p.no_keywords() == True])
	fixtures.append(post)



print("Finished. ({} total records)".format(len(fixtures)))

for key in sorted(keyword_count.keys()):
	print("{}: {} records  ACTUAL:{}".format(key, keyword_count[key], sum([1 for f in fixtures if f.keywords[key] == True])))


with open("./fixtures/11814828.html", "w") as file:
	file.write(fixture_header)
	for f in fixtures:
		file.write(str(f.posting))
	file.write(fixture_footer)