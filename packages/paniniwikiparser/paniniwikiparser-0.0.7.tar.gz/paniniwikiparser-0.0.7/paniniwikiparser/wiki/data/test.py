
title="128 dfdkhf"
def get_counters():
    
    return {"raw_pages": 0,

            "non_redirect_pages":0,

            "title_timeline": 0,

            "title_listof": 0,

            "title_indexof": 0,

            "title_not_ascii": 0,

            "title_size_0_1": 0,

            "title_size_2": 0,

            "title_size_3_5": 0,

            "title_size_6_9": 0,

            "title_size_10_19": 0,

            "title_size_20_29": 0,

            "title_size_30_39": 0,

            "title_size_40_49": 0,

            "title_size_50": 0,

            "title_disambiguation": 0,

            "title_number" : 0,

            "page_disambiguation" : 0,

            "page_external_links_0_2" : 0,

            "page_external_links_3_4": 0,

            "page_external_links_5_9": 0,

            "page_external_links_10": 0,

            "page_internal_links_0_2": 0,

            "page_internal_links_3_4": 0,

            "page_internal_links_5_9": 0,

            "page_internal_links_10": 0,

            "page_non_stop_words_less_100": 0, 

            "final_content": 0         

           }

def number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False;


counters=get_counters()
def start():

    if "(number)" in title:
        counters["title_number"] += 1
    if  number(title):
            counters["title_number"] += 1
    print(counters)
start()