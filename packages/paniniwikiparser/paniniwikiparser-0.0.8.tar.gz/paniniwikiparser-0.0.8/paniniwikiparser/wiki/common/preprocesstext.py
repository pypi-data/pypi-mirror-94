import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from dateutil import parser
from .error_log import write_log

# Need to preprocess to check for stopwords. Need to load here as we cant load from setup.py
nltk.download('stopwords')
nltk.download("punkt")

def is_valid_date(date_str):
    try:
        parser.parse(date_str)
        return True
    except:
        return False

#preprocessing
def preprocess_text(input_text,filename):
    processed_text=""
    try:
        #Collecting  stop_words from NLTK library
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(input_text)

        #Remove stop words in content
        non_stopwords = [w.lower() for w in word_tokens if not w in stop_words]

        if len(non_stopwords)>100:

            #Remove date related information in 'text'
            words=[' '.join([w for w in line.split() if not is_valid_date(w)]) for line in non_stopwords]
            text=' '.join(words)
            #print(text)
            
            #Remove number, contains number, separate punctuation
            tokenizer = nltk.RegexpTokenizer(r"\b[a-zA-Z][a-zA-Z]+\b")
            new_words=tokenizer.tokenize(text)
            processed_text=' '.join(new_words)
            #print(processed_text)
        return processed_text
    except Exception as e:
        write_log(e.args,filename)
        return processed_text