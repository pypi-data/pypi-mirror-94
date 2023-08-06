import pymysql 
from .db_config import HOST,USER,PASSWORD,DATABASE_NAME
from ..common.error_log import write_log
from datetime import datetime,timezone



def load_articles_without_cleantext(article,filename):
    '''
        this method is implemented for if any failure in article table due to cleantext
        here we are inserting article without clean text
    '''
    try:
        conn  = pymysql.connect(host=HOST, user=USER, password=PASSWORD,db=DATABASE_NAME) 
        # Create a cursor object 
        cur  = conn.cursor() 
        try:
            page_title = article["Page_title"].replace("'","''")
            page_id = article["page_id"]
            text = article["processed_text"].replace("'","''")
            revision_id=article["revision_id"]
            isdeleted=0


            query = f"INSERT INTO article (page_title, page_id, content,revisionid,isdeleted,file_name) VALUES ('{page_title}', '{page_id}', '{text}','{revision_id}','{isdeleted}','{filename}')"
            cur.execute(query)

        except Exception as e:
            write_log('page id is {0}  error info {1}'.format(str(article["page_id"]),e.args),filename)
            #print(e.args)
        finally:
            #print(f"{cur.rowcount} details inserted after cleaning") 
            conn.commit() 
            conn.close()
    except Exception as e:
        print(e.args)

def isfile_already_read(filename):
    try:
        conn  = pymysql.connect(host=HOST, user=USER, password=PASSWORD,db=DATABASE_NAME) 
        # Create a cursor object 
        cur  = conn.cursor() 
        try:
            sql="select filename from fileread_status where filename=%s"
            param=(filename)
            cur.execute(sql,param)
            myresult = cur.fetchall()
            if(len(myresult)>0):
                return True
            else:
                return False
        except Exception as e :
            print(e)
            pass
        print(f"{cur.rowcount} details inserted before preprocess ") 
        conn.commit() 
        conn.close()
    except Exception as e:
        print(e.args)
        return False

def insert_filestatus(filename,counters):
    try:
        conn  = pymysql.connect(host=HOST, user=USER, password=PASSWORD,db=DATABASE_NAME) 
        # Create a cursor object 
        cur  = conn.cursor()
        now_utc = datetime.now(timezone.utc)
        date_string=now_utc.strftime('%Y-%m-%d %H:%M:%S')
        query = f"INSERT INTO fileread_status (filename,tran_date_time,counters) VALUES ('{filename}','{date_string}','{str(counters)}')"
        try:
            cur.execute(query) 
        except Exception as e:
            print(e.args)
        conn.commit() 
        conn.close()
    except Exception as e:
        print(e.args)

def load_articles(article,filename):
    '''
     this will accept page data and insert into artile table
    '''
    try:
        query=""
        conn  = pymysql.connect(host=HOST, user=USER, password=PASSWORD,db=DATABASE_NAME) 
        # Create a cursor object 
        cur  = conn.cursor() 
        try:
            page_title = article["Page_title"].replace("'","''")
            page_id = article["page_id"]
            text = article["processed_text"].replace("'","''")
            revision_id=article["revision_id"]
            clean_tex=article["clean_text"].replace("'","''")
            isdeleted=0

            query = f"INSERT INTO article (page_title, page_id, content, revisionid,isdeleted,clean_text,file_name) VALUES ('{page_title}', '{page_id}', '{text}','{revision_id}','{isdeleted}','{clean_tex}','{filename}')"
            cur.execute(query)

        except Exception as e:
            #print(query)
            load_articles_without_cleantext(article,filename)
            #write_log('page id is {0}  error info {1}'.format(str(article["page_id"]),e.args),filename)
            #print(e.args)
        finally:
            #print(f"{cur.rowcount} details inserted after cleaning") 
            conn.commit() 
            conn.close()
    except Exception as e:
        print(e.args)

def load_deleted_articles(article,filename):
    '''
        this will accept invalid page data and insert into artile_delete table
    '''
    try:
        conn  = pymysql.connect(host=HOST, user=USER, password=PASSWORD,db=DATABASE_NAME) 
        # Create a cursor object 
        cur  = conn.cursor() 
        try:
            page_id = article["page_id"]
            query = f"INSERT INTO article_deleted (page_id,file_name) VALUES ('{page_id}','{filename}')"
            cur.execute(query) 
        except Exception as e:
            write_log('page id is {0}  error info {1}'.format(str(article["page_id"]),e.args),filename)
        finally:
            conn.commit() 
            conn.close()
    except Exception as e:
        print(e.args)