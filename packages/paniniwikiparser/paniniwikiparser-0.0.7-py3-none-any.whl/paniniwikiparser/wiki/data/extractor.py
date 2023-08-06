import time
import os
import sys
import bz2
import xml.sax
import mwparserfromhell

from ..db.dbinsertion import *

from ..common.preprocesstext import preprocess_text

import re
import codecs

output=[]
TITLE_LENGHT_LIMIT=40
TEXT_LENGHT_LIMIT=100
WIKI_LINKS_LIMIT=5
EXTERNAL_LINKS_LIMIT=5
class stack:
    def __init__ (self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.items:
            return self.items.pop()
        else:
            raise Exception("stack is empty")

    def top(self):
        return self.items[-1] if self.items else None

class WikiXmlHandler(xml.sax.handler.ContentHandler):
    """Parse through XML data using SAX"""
    def __init__(self, ns = [0]):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self._pages = []
        self._ns = ns
        self._stack =  stack()
        self._redirect = False

    def characters(self, content):
        """Characters between opening and closing tags"""
        if self._current_tag:
            self._buffer.append(content)


    def startElement(self, name, attrs):
        """Opening tag of element"""
        self._stack.push(name)
        
        if name =="page":
            self._values["redirect"]=""
            self._values["parentid"]=""
            self._values["revisionid"] =""

        if name in ('title', 'text', 'timestamp', 'ns', 'id',"parentid","redirect"):
            self._current_tag = name
            self._buffer = []

            if name == 'redirect':
                self._values[name] = attrs["title"] #for rediret
                self._redirect=True

    def endElement(self, name):
        """Closing tag of element"""
        self._stack.pop()
        if name == self._current_tag:
            if name == "id":
                if self._stack.top() =="page":
                    v = ' '.join(self._buffer)
                    if isinstance(v, str):
                        self._values[name] = int(v)  # For PageID 
                if self._stack.top() =="revision":
                    v = ' '.join(self._buffer)
                    if isinstance(v, str):
                        self._values["revisionid"] = int(v)  #For revision ID 
            elif name != "redirect":
                self._values[name] = ' '.join(self._buffer)
        # if name == 'page' and self._values['ns'] and int(self._values['ns']) in self._ns:
        #     self._pages.append(
        #                         (self._values['title'],self._values['text'],self._values['id'],
        #                         int(self._values['ns']),self._values["redirect"],self._values["parentid"],
        #                         self._values["revisionid"]
        #                         )
        #                     )
        if name == 'page' and self._values['ns'] and int(self._values['ns']) in self._ns:
            if not self._redirect: #add self_redirect in __init__ and give value False
                self._values['redirect'] = None
                
            self._pages.append([self._values['title'], self._values['text'], self._values['id'], int(self._values['ns']), self._values['redirect']])

            self._redirect = False

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


def is_good_string(s):
    d = codecs.escape_decode(s)[0].decode('utf-8')
    for c in d:
        if ord(c) < 32 or ord(c) > 128:
            return False
    return True

def number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def proces_xml_page(page,counters):
    ''' this will accept parsed wiki data and process it and insert it into db'''
    global output
    #print(f'Title is {page[0]}')  #0- title, 1- text,2- id, 3- ns,
                                    #4- redirect,5-parentid,6-revisionid
    title=page[0]
    raw_text=page[1]
    page_id=page[2]
    ns=page[3]
    redirect=page[4]
    parentid=page[5]
    revisionid=page[6]

    #Collect page text
    wiki = mwparserfromhell.parse(raw_text)

    ref = re.compile(r'\s< ref > .* < /ref >\s|==References==|< references / >|==External links==|Category:')

    clean_text = ref.sub(r' ', wiki.strip_code().strip())
    isredirect=0
    if(len(redirect)!=0):
        isredirect=1
    if ns == 0:
        counters["raw_pages"] += 1

    if isredirect==0:
    # every thing under "Category:Integers"
    # everything under "Category:person"
        counters["non_redirect_pages"] += 1

        if title.startswith("Timeline of"):       
            counters["title_timeline"] += 1
            return                    
        elif title.startswith("List of"):
            counters["title_listof"] += 1
            return
        elif title.startswith("Index of"):
            counters["title_indexof"] += 1
            return
        if not is_good_string(title):                   
            counters["title_not_ascii"] += 1
            return
        if len(title) <=1:
            counters["title_size_0_1"] += 1
            return
        elif len(title) ==2:    
            counters["title_size_2"] += 1
        elif len(title) >=3 and len(title) < 6:    
            counters["title_size_3_5"] += 1
        elif len(title) >=6 and len(title) < 10:    
            counters["title_size_6_9"] += 1
        elif len(title) >=10 and len(title) < 20:     
            counters["title_size_10_19"] += 1
        elif len(title) >=20 and len(title) < 30:    
            counters["title_size_20_29"] += 1
        elif len(title) >=30 and len(title) < 40:    
            counters["title_size_30_39"] += 1
        elif len(title) >=40 and len(title) < 50:    
            counters["title_size_40_49"] += 1
            return
        elif len(title) >=50:    
            counters["title_size_50"] += 1
            return
        '''  
        if len(page[0]) <=1 or len(page[0].split(' ')) >= 40: #adjust this per statistics
            print(page[0], page[2], page[3])
            return
        '''

        if "(disambiguation)" in title:
            counters["title_disambiguation"] += 1
            return

        if "(number)" in title or number(title):
            counters["title_number"] += 1
            return
        if "This is a disambiguation page" in clean_text:
            counters["page_disambiguation"] += 1
            return

        internal_links = len(wiki.filter_wikilinks())
        external_links = len(wiki.filter_external_links())

        if external_links < 3:
            counters["page_external_links_0_2"] += 1
            return
        elif external_links >=3 and external_links <5:
            counters["page_external_links_3_4"] += 1
            return
        elif external_links >=5 and external_links <10:
            counters["page_external_links_5_9"] += 1
        elif external_links >=10:
            counters["page_external_links_10"] += 1

        if internal_links < 3:
            counters["page_internal_links_0_2"] += 1
            return
        elif internal_links >=3 and internal_links <5:
            counters["page_internal_links_3_4"] += 1
            return
        elif internal_links >=5 and internal_links <10:
            counters["page_internal_links_5_9"] += 1
        elif internal_links >=10:
            counters["page_internal_links_10"] += 1
        
        '''text = ref.sub(r' ', wiki.strip_code().strip())
            word_tokens = word_tokenize(text)

            #Remove stop words in content

            non_stopwords = [w.lower() for w in word_tokens if not w in stop_words]

            if len(non_stopwords) < 100:

            counters["page_non_stop_words_less_100"] += 1'''

        # final content
    counters["final_content"] += 1


    #clean text
    # clean_text=wiki.strip_code().strip()

    #pre processing using nltk
    preprocessed_text=preprocess_text(clean_text)

    #collect Internal links in wiki page
    wikilinks = [(x.title, x.text) for x in wiki.filter_wikilinks()]
    #collect External links in wiki page
    external_links = [(x.title, x.url) for x in wiki.filter_external_links()]
    


    if title!="":
        if is_good_string(title) and len(title)<=TITLE_LENGHT_LIMIT and len(preprocessed_text)>TEXT_LENGHT_LIMIT and ns==0 and len(wikilinks)>WIKI_LINKS_LIMIT and len(external_links)>EXTERNAL_LINKS_LIMIT:
            #Intiating db insertion 
            load_articles(
            {
                    "page_id":page_id,
                    "Page_title":title,
                    "ns":ns,
                    "raw_text":raw_text,
                    "clean_text":clean_text,
                    "processed_text":preprocessed_text,
                    "redirect":redirect,
                    "parentid":parentid,
                    "revision_id":revisionid,
                    "isredirect":isredirect,
                    "isdeleted":0
            })
        else:
            #Intiating db insertion 
            load_articles(
            {
                    "page_id":page_id,
                    "Page_title":title,
                    "ns":ns,
                    "raw_text":raw_text,
                    "clean_text":clean_text,
                    "processed_text":preprocessed_text,
                    "redirect":redirect,
                    "parentid":parentid,
                    "revision_id":revisionid,
                    "isredirect":isredirect,
                    "isdeleted":1
            })
    

    # if preprocessed_text!="":
    #     obj={
    #     "page_id":page[2],
    #     "Page_title":page[0],
    #     "ns":page[3],
    #     "raw_text":page[1],
    #     "clean_text":clean_text,
    #     "processed_text":preprocessed_text,
    #     "redirect":page[4],
    #     "parentid":page[5],
    #     "revision_id":page[6],
    #     "isdeleted":page[3]
    #     }
    #     output.append(obj)
    
def readxml_data(file_name):

    try:
        counters=get_counters()
        index=0
        start_time = time.time()

        handler = WikiXmlHandler()
        
        # Parsing object
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)

        for i, line in enumerate(bz2.BZ2File(file_name, 'r')):
            parser.feed(line)
            if len(handler._pages)>0:
                proces_xml_page(handler._pages[0],counters)
                index=index+1
                handler._pages=[]
            # if(index>5):
            #     res=json.dumps(output,default=vars)
            #     with open('result_clean_markup.json','w') as f:
            #         json.dump(res,f)
            #         break;

        elapsed_time = time.time() - start_time
        print("file reading finished")
        print(elapsed_time);
    except Exception as e:
        print(e)
readxml_data("C:\enwiki-latest-pages-articles11.xml-p6899367p7054859.bz2")