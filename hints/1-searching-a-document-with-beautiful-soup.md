# Hint 1

The main part of this project involves retrieving a page from hackernews and then parsing it with BeautifulSoup.

The first step in doing this is going to be to retrieve the document from the web. To do this we'll use the `requests` package.

Here is an example of retrieving a document:

```
import requests

r = requests.get('http://myurl.com')
if r.status_code == requests.codes.ok:
	# Do stuff here
```

Nice and easy right? the `get` method retrieves the page and returns the response.
Doing `if r.status_code == requests.codes.ok:` causes processing to proceed only if the page was retrieved successfully. (ie. We did not get an error like 404/403/500/etc.)


From there we may bring the document into BeautifulSoup for processing.

```
from bs4 import BeautifulSoup

soup = BeautifulSoup(r.text, 'html.parser')
```

We can now use our `soup` to interact and search through the html document.

Let's say for example that this is the html document we retrieved:

```
<html>
<head>
<title>My Awesome Page</title>
</head>
<body>
<h1 class="welcome">Welcome to My Awesome Page</h1>
<h1 class="favourites">My Favourite Things</h1>

<span id="stuff">Here are some of my favourite things:</span>
<ul>
  <li>Python</li>
  <li>Swallows carrying coconuts</li>
  <li>Strange women lying in ponds distributing swords</li>
</ul>
</body>
</html>
```

BeautifulSoup allows you to search through the document based on tags. For example if I wanted to print all the favourite things I could do:

```
for fav in soup.findall('li'):
    print(fav.text)
```
Which would result in:
```
Python
Swallows carrying coconuts
Strange women lying in ponds distributing swords
```

You can also retrieve just a single item, or restrict your search based on tag attributes. If I wanted to just get the first h1 tag that has a `class` of `favourites` I could do:
```
fav = soup.find('h1', class_='favourites')
print(fav.text)
```
*IMPORTANT:* Notice that we use `class_` not `class`, class is a special word and thus soup expects a trailing underscore to differentiate.

You can also navigate up and down the DOM(Document Object Model) tree. Say we do find an item but we want to get it's parent tag. (Example: we found the `li` tags, but what we really want is the parent `ul` tag)

```
li = soup.find('li')
ul = li.parent
``
And if we want the children of something (in this case getting the `li` tags once we have the `ul`) we can do that too.

```
for li in ul.children:
  print(li.text)
```
```
Python
Swallows carrying coconuts
Strange women lying in ponds distributing swords
```

You can also directly reference a child from the parent, if there are multiple children of the same tag it will just grab the first one.
```
ul = soup.find('ul')
print(ul.li.text)
```
```
Python
```

You can also perform searches on any soup sub-object, not just the main one.
```
ul = soup.find('ul')
for li in ul.findall('li'):
	print(li.text)
```
```
Python
Swallows carrying coconuts
Strange women lying in ponds distributing swords
```

Finally, you can get any attribute of any element. Say we found the following image tag: `<img src='my_pic.jpg' alt='My pic'>` and have it stored in the variable `img`:
```
print(img.get('alt'))
```
```
My pic
```

You can find more information at the [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).