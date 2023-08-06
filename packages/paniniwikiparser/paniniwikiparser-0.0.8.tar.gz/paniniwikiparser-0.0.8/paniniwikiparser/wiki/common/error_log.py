import json
import os

def write_log(error,filename):
    '''
        logging all the exceptions here with input file  name
        a .txt file will be created for every input file
    '''
    errorlogfile=filename.replace(":","_").replace("\\","_")
    res=json.dumps(error,default=vars)
    if os.path.isfile(errorlogfile+".txt"):
        with open(errorlogfile+".txt",'a') as f:
            json.dump(res,f)
    else:
        with open(errorlogfile+".txt",'w') as f:
            json.dump(res,f)