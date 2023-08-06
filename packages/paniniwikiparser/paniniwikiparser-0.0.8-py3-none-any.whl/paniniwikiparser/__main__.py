from multiprocessing import Pool

from pymysql import STRING
from .wiki.data.extractor import readxml_data
import time
import os;
import sys;


#base, the data directory
#files, the list of the all file names
#processors, the number of processors the execution machine
def main(base, files, processors):

    paths = [os.path.join(base, x) for x in files]
    
    with Pool(processors) as pool:
        result = pool.map(readxml_data, paths)
    
    print("all files are processed successfully")



if __name__ == '__main__':
    '''
        command line arguments need to be passed as follows
        1. base file path
        2. comma seperated file names
        3. a integer value for number of processes
    '''
    filelist=[]
    basepath=sys.argv[1]
    fileinfo = sys.argv[2]
    noofprocessors=int(sys.argv[3])

    list2 = [str(c) for c in sys.argv[2].split(',')] 
    for file in list2:
        filelist.append(file)
    
    main(base = basepath, 
    files=filelist,processors = noofprocessors)  

