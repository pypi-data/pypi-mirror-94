import time
import os
import sys
import bz2
import xml.sax
import mwparserfromhell

from ..db.dbinsertion import *

from ...common.preprocesstext import preprocess_text

output=[]
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
        if name == 'page' and self._values['ns'] and int(self._values['ns']) in self._ns:
            self._pages.append(
                                (self._values['title'],self._values['text'],self._values['id'],
                                int(self._values['ns']),self._values["redirect"],self._values["parentid"],
                                self._values["revisionid"]
                                )
                            )
    
def proces_xml_page(page):
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

    #clean text
    clean_text=wiki.strip_code().strip()

    #pre processing using nltk
    preprocessed_text=preprocess_text(clean_text)

    #collect Internal links in wiki page
    wikilinks = [(x.title, x.text) for x in wiki.filter_wikilinks()]

    #collect External links in wiki page
    external_links = [(x.title, x.url) for x in wiki.filter_external_links()]
    
    isredirect=0
    if(len(redirect)!=0):
        isredirect=1

    if title!="":
        if len(title)<=40 and len(preprocessed_text)>100 and ns==0 and len(wikilinks)>5 and len(external_links)>5:
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
        index=0
        start_time = time.time()

        handler = WikiXmlHandler()
        
        # Parsing object
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)

        for i, line in enumerate(bz2.BZ2File(file_name, 'r')):
            parser.feed(line)
            if len(handler._pages)>0:
                proces_xml_page(handler._pages[0])
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
