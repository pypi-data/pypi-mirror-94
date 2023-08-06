import pymysql 
from db_config import HOST,USER,PASSWORD,DATABASE_NAME

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

def insert_filestatus(filename):
    try:
        conn  = pymysql.connect(host=HOST, user=USER, password=PASSWORD,db=DATABASE_NAME) 
        # Create a cursor object 
        cur  = conn.cursor() 
        query = f"INSERT INTO fileread_status (filename) VALUES ('{filename}')"
        try:
            cur.execute(query) 
        except Exception as e:
            print(e.args)
        conn.commit() 
        conn.close()
    except Exception as e:
        print(e.args)

def load_articles(article):
    try:
        conn  = pymysql.connect(host=HOST, user=USER, password=PASSWORD,db=DATABASE_NAME) 
        # Create a cursor object 
        cur  = conn.cursor() 
        try:
            page_title = article["Page_title"].replace("'","")
            page_id = article["page_id"]
            text = article["processed_text"]
            isredirect= article["isredirect"]
            redirect_title=article["redirect"]
            revision_id=article["revision_id"]
            isdeleted=article["isdeleted"]
        except Exception as e :
            print(e)
            pass
        query = f"INSERT INTO article (page_title, page_id, content, isredirect, redirect_title, revisionid,isdeleted  ) VALUES ('{page_title}', '{page_id}', '{text}','{isredirect}','{redirect_title}','{revision_id}','{isdeleted}')"
        try:
            cur.execute(query) 
        except Exception as e:
            print(e.args)
            pass
        #print(f"{cur.rowcount} details inserted after cleaning") 
        conn.commit() 
        conn.close()
    except Exception as e:
        print(e.args)