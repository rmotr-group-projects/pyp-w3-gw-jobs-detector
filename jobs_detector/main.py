import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings

DEFAULT_KEYWORDS = [
            'Remote',
            'Postgres',
            'Python',
            'Javascript',
            'React',
            'Pandas'
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
    """
    This subcommand aims to get jobs statistics by parsing "who is hiring?"
    HackerNews posts based on given set of keywords.
    """
    # HINT: You will probably want to use the `BeautifulSoup` tool to
    # parse the HTML content of the website
    
    target_url = settings.BASE_URL.format(post_id)
    
    page_html = requests.get(target_url)
    soup = BeautifulSoup(page_html.text, 'html.parser')
    tags = soup.find_all("td", class_="ind")
    
    keyword_list = keywords.split(",")
    keyword_count_dict = {}
    for keyword in keyword_list:
        keyword_count_dict[keyword] = 0
    
    if combinations is not None:
        combo_tuples = [tuple(combo.split("-")) for combo in combinations]
        # now combo_tuples == [('python', 'django'), ('python', 'django', 'remote')]
        combo_count_dict = {}
        for combo_tuple in combo_tuples:
            combo_count_dict[combo_tuple] = 0
    
    total_job_posts = 0
    for tag in tags:
        if tag.img.get("width") == "0":
            # winner!
            try:
                comment = tag.parent.find("span", class_="c00").text
                # print(comment)
                #print(tag.parent.find("span", class_="c00").text)
                for keyword in keyword_list:
                    if keyword.lower() in comment.lower():
                        keyword_count_dict[keyword] += 1
                
                if combinations is not None:
                    for combo in combo_tuples:
                        if all([keyword.lower() in comment.lower() for keyword in combo]):
                            combo_count_dict[combo] += 1

                total_job_posts += 1
            except AttributeError:
                pass
        
    print("Total job posts: {}".format(total_job_posts))
    print("Keywords:")
    for keyword in keyword_list:
        key_count = keyword_count_dict[keyword]
        print("{}: {} ({}%)".format(keyword.title(), key_count, (key_count * 100 // total_job_posts)))
       
    if combinations is not None:    
        print("Combinations:")
        for combo_tuple in combo_tuples:
            name_string = "{}".format("-".join(keyword.title() for keyword in combo_tuple))
            combo_count = combo_count_dict[combo_tuple]
            print("{}: {} ({}%)".format(name_string, combo_count, (combo_count * 100 // total_job_posts)))
    
            
    # keywords might be something like "python,django,remote"
    
    # now keyword_list == ["python", "django", "remote"]
    
    # combinations might be something like ['python-django', 'python-django-remote']
    # 
    
    # print("{} {} {}".format(post_id, keywords, combinations))


if __name__ == '__main__':
    jobs_detector()





