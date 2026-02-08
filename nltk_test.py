
import nltk
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("punkt_tab")

#Tokenization
from nltk.tokenize import word_tokenize

#Stopwords list
from nltk.corpus import stopwords

#Stemming
from nltk.stem import PorterStemmer

#Lemmatization
from nltk.stem import WordNetLemmatizer

sentences=[
    "i am learning python and Python..",
    "we are happy today",
    "i am sad today",
    "hello, How are you?",
    "i WAS WonDERing that why   was i wondering at all? Quite an interesting thought isn't it!!..."
]

import string
punctuations=string.punctuation
english_stopwords=stopwords.words("english")
wnet=WordNetLemmatizer()

def preprocess_text(documents):
  result=[]
  for line in documents:
    line=line.lower()

    tokens=word_tokenize(line)
    filtered_tokens=[]
    for word in tokens:
      if word not in english_stopwords:
        filtered_tokens.append(word)

    clean_tokens=[word for word in filtered_tokens if word not in punctuations]

    lemmatized_words=[]
    for word in clean_tokens:
      lemmatized_words.append(wnet.lemmatize(word,"v"))

    final_tokens=[]
    for word  in lemmatized_words:
      if word.isalpha():
        final_tokens.append(word)

    cleaned_text=" ".join(final_tokens)
    result.append(cleaned_text)



  return result

cleaned_sentences=preprocess_text(sentences)
print(cleaned_sentences)