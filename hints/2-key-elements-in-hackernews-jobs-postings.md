# Hint 2
Looking at the HTML of a hackernews posting can be a bit of a daunting task. 
By identifying a few key elements it can make parsing significantly easier.

# Step 1: Identifying a comment

All jobs postings are comments on a hackernews page. 
All contents are contained in a `<tr>` tag with a CSS class of `'.athing'`. 
By searching for those specific things we are able to retrieve all the comments. 
However this leads to an issue: This will also retrieve all the replies to postings 
as they are also comments. This leads us to step 2.

# Step 2: Identifying top level comments

There is a way to identify if a particular comment is 
a top level comment(not a reply to something) or not. 
Each comment has a `<td>` tag in it of class `'c00'`, and within that tag 
is an `<img>` tag. This image is a spacer that determines the indentation of a comment. 
Top level comments have `img`'s with a width of 0.