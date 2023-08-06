import time
import os
import sys
import bz2
import xml.sax
import mwparserfromhell
from datetime import datetime,timezone
from ..db.dbinsertion import *
import json
from multiprocessing import Pool

import re
import codecs
import subprocess
from ..common.preprocesstext import preprocess_text

output=[]
TITLE_LENGHT_LIMIT=40
TEXT_LENGHT_LIMIT=100
WIKI_LINKS_LIMIT=5
EXTERNAL_LINKS_LIMIT=5

work = (["A", 5], ["B", 2], ["C", 1], ["D", 3])

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
    #ns value need to read from xml
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
                
            self._pages.append([self._values['title'], self._values['text'], self._values['id'], int(self._values['ns']), self._values['redirect'],self._values["parentid"],self._values["revisionid"]])

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

def proces_xml_page(page,counters,filename):
    ''' this will accept parsed wiki data and process it and insert it into db'''
   
    #print(f'Title is {page[0]}')  #0- title, 1- text,2- id, 3- ns,#4- redirect,5-parentid,6-revisionid
    
    isvalid=1  # this will be set to zero when a record is invalid                           
    
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
    if(redirect is not None):
        isredirect=1
        isvalid=0

    if ns == 0:
        counters["raw_pages"] += 1
    else:
        isvalid=0


    if isredirect==0:
    # every thing under "Category:Integers"
    # everything under "Category:person"
        counters["non_redirect_pages"] += 1

        if title.startswith("Timeline of"):       
            counters["title_timeline"] += 1
            isvalid=0                    
        elif title.startswith("List of"):
            counters["title_listof"] += 1
            isvalid=0
        elif title.startswith("Index of"):
            counters["title_indexof"] += 1
            isvalid=0



        if not is_good_string(title):                   
            counters["title_not_ascii"] += 1
            isvalid=0



        if len(title) <=1:
            counters["title_size_0_1"] += 1
            isvalid=0
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
            isvalid=0
        elif len(title) >=50:    
            counters["title_size_50"] += 1
            isvalid=0


        if "(disambiguation)" in title:
            counters["title_disambiguation"] += 1
            isvalid=0

        if "(number)" in title or number(title):
            counters["title_number"] += 1
            isvalid=0

        if "This is a disambiguation page" in clean_text:
            counters["page_disambiguation"] += 1
            isvalid=0

        internal_links = len(wiki.filter_wikilinks())
        external_links = len(wiki.filter_external_links())



        if external_links < 3:
            counters["page_external_links_0_2"] += 1
            isvalid=0
        elif external_links >=3 and external_links <5:
            counters["page_external_links_3_4"] += 1
            isvalid=0
        elif external_links >=5 and external_links <10:
            counters["page_external_links_5_9"] += 1
        elif external_links >=10:
            counters["page_external_links_10"] += 1



        if internal_links < 3:
            counters["page_internal_links_0_2"] += 1
            isvalid=0
        elif internal_links >=3 and internal_links <5:
            counters["page_internal_links_3_4"] += 1
            isvalid=0
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



        #pre processing using nltk
        preprocessed_text=preprocess_text(clean_text,filename)

        if(len(preprocessed_text.split(" ")))<TEXT_LENGHT_LIMIT:
            counters["page_non_stop_words_less_100"] += 1
            isvalid=0

        

        #collect Internal links in wiki page
        wikilinks = [(x.title, x.text) for x in wiki.filter_wikilinks()]

        #collect External links in wiki page
        external_links = [(x.title, x.url) for x in wiki.filter_external_links()]
    


        if title!="":
            if isvalid==1: # if isvalid=1 we are taking this article into cosideration
                # final content
                counters["final_content"] += 1
                
                #is_good_string(title) and len(title)<=TITLE_LENGHT_LIMIT and len(preprocessed_text)>TEXT_LENGHT_LIMIT and ns==0 and len(wikilinks)>WIKI_LINKS_LIMIT and len(external_links)>EXTERNAL_LINKS_LIMIT:
                #Intiating db insertion 
                load_articles(
                {
                        "page_id":page_id,
                        "Page_title":title,
                        "ns":ns,
                        "raw_text":raw_text,
                        "clean_text":clean_text,
                        "processed_text":preprocessed_text,
                        "parentid":parentid,
                        "revision_id":revisionid,
                },filename)
            else: # we are inserting invalid article into article_deleted table for further usage
                #Intiating db insertion 
                load_deleted_articles(
                {
                    "page_id":page_id
                },filename)
    else: # we are inserting  redirected article into article_deleted table for further usage
        load_deleted_articles(
        {
            "page_id":page_id
        },filename)
    
def readxml_data(file):
    '''
        this method will take bz2 filepath as arguemnt and parse the articles 
    '''
    try:
        head, tail = os.path.split(file)
        file_name=tail
        print(file_name)
        now_utc = datetime.now(timezone.utc)
        
        file_status=isfile_already_read(file_name)
        
        if(file_status):
           write_log("this file is already processed",file_name)
           return
          
        write_log("File parsing started at time :"+now_utc.strftime("%m/%d/%Y, %H:%M:%S"),file_name)
        
        counters=get_counters()
        
        #logging file read status in database to avoid duplicate file processing
        insert_filestatus(file_name,"file reading started");

        
        start_time = time.time()
        handler = WikiXmlHandler()
        
        # Parsing object
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        with bz2.BZ2File(file, 'r') as file:
            for i, line in enumerate(file):
                parser.feed(line)

                # once a page is available in handler,it will process and remove the page from pages object 
                if len(handler._pages)>0: 
                    proces_xml_page(handler._pages[0],counters,file_name)
                    handler._pages=[] 
                    
        json_object = json.dumps(counters, indent = 4) 

        #logging file read status in database to avoid duplicate file processing  
        insert_filestatus(file_name,json_object);
        elapsed_time = time.time() - start_time
        now_utc = datetime.now(timezone.utc)
        
        write_log("File parsing finished at time :"+now_utc.strftime("%m/%d/%Y, %H:%M:%S"),file_name)
        
        json_object = json.dumps(counters, indent = 4)   
        write_log('Counter info {0}  :'.format(json_object),file_name)
        
        print(file)
        print("is processed successfully")
        print(elapsed_time); 
    except Exception as e:
        print(e)
