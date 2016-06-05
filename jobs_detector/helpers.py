import re
from collections import defaultdict

def _keyword_search(comment, keyword):
    """
    Return True if the keyword is found in the search and add to keywords_dict
    and comments_dict dictonaries.
    
    keywords_dict = {Python:[12345,09876,45677], 
                     Remote:[12345,98752,15973]}
                    
    comments_dict = {12345:'This is the comment test of the post'}
                    {98765:'This is another comment test of the post'}                
    """
    if re.search(re.compile(keyword, re.IGNORECASE), str(comment)):
        parent = comment.find_parent('tr', {'class':'athing'})
        get_id = parent.find('a', {"id":re.compile('up_.*')})['id'].split('_')[1]
        
        keywords_dict[keyword].append(get_id)
        
        if get_id not in comments_dict:
            comments_dict.update({get_id:comment.get_text()})
        
        return True
    return False

def _check_combinations(combination):
    for combo in combination.split(','):
        # reduce(lambda x, y: x+y, [1, 2, 3, 4, 5])
        combo_list = combo.replace('-', ',')
        # num_found = reduce(lambda keyword, keyword2: 
        #     True if keyword in keywords_dict[keyword], 
        #     combo_list)
        
        num_found = 0
        for id_num in keywords_dict[keyword1]:
            if id_num in keywords_dict[keyword2]:
                num_found += 1

        
        # num_found = 0
        # for keyword in combo.split('-'):
        #     if keyword in keywords_dict[keyword]:
        #         num_found += 1
    return num_found
#    print(combo.split('-'))


        # Remote-Python-Flask
        
        # keywords_dict passed here and processed
        # if id in one dict exists in another, save in combos list    

    # for keyword in keywords:
    #     for comment in soup.find_all('span', class_='c00'):
    #         if _keyword_search(comment, keyword):
    #             count += 1




def _get_percent(small_num, big_num):
    return small_num / float(len(big_num)) * 100