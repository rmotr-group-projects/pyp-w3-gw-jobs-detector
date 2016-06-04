# [pyp-w3] Jobs Detector

Today we will develop a command line tool which aims to parse certain websites looking for job statistics based on given keywords. In this very first version of the tool, we will only implement a parser for the HackerNews blog, which includes a monthly report of "Who is hiring?". Example: https://news.ycombinator.com/item?id=11814828

The command line tool must be accessible by calling `jobs_detector` command. A `hacker_news` subcommand must be also available as part of this implementation.

## Command usage

To request jobs statistics using a default set of keywords, just call the `hacker_news` subcommand providing a valid HN post id (see the last part of the sample URL above), like this:

```bash
$ jobs_detector hacker_news -i 11814828
Total job posts: 888

Keywords:
Remote: 174 (19%)
Postgres: 81 (9%)
Python: 144 (16%)
Javascript: 118 (13%)
React: 133 (14%)
Pandas: 5 (0%)
```
