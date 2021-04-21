import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_read_xml as pdx 
import re

import gensim
from gensim.test.utils import datapath
from gensim import utils
import gensim.models

from nltk import ngrams

from sklearn.decomposition import IncrementalPCA    
from sklearn.manifold import TSNE 

#Cleaning function

def date_cleaner(df):
    '''
    input: dataframe with 'Dateline' column with Arabic strings for months
    outut: dataframe with 'Dateline' column as (English) Datetime object
    '''
    ar_jan = 'يناير'
    ar_feb = 'فبراير'
    ar_mar = 'مارس'
    ar_apr = 'أبريل'
    ar_may = 'مايو'
    ar_jun = 'يونيو'
    ar_jul = 'يوليو'
    ar_aug = 'أغسطس'
    ar_sep = 'سبتمبر'
    ar_oct = 'أكتوبر'
    ar_nov = 'نوفمبر'
    ar_dec = 'ديسمبر'

    month_dict = {ar_jan:'01', ar_feb:'02', ar_mar:'03', ar_apr:'04', ar_may:'05', 
    ar_jun:'06', ar_jul:'07', ar_aug:'08', ar_sep:'09', ar_oct:'10', ar_nov:'11', 
    ar_dec:'12'}
    
    #substitues 01-12 code for month instead of Arabic name
    df['Dateline'] = df['Dateline'].apply(lambda x: x.replace(x.split('/')[1], 
    month_dict[x.split('/')[1]]))
    
    df['Dateline'] = pd.to_datetime(df['Dateline'])

    return df

def general_clean_text(text):
    search = ["أ","إ","آ","ة","_","-","/",".","،"," و "," يا ",'"',"ـ","'","ى","\\",'\n', '\t','&quot;','?','؟','!']
    replace = ["ا","ا","ا","ه"," "," ","","",""," و"," يا","","","","ي","",' ', ' ',' ',' ? ',' ؟ ',' ! ']  
    p_tashkeel = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    text = re.sub(p_tashkeel,"", text)
    p_longation = re.compile(r'(.)\1+')
    subst = r"\1\1"
    text = re.sub(p_longation, subst, text)
    text = text.replace('وو', 'و')
    text = text.replace('يي', 'ي')
    text = text.replace('اا', 'ا')
    
    for i in range(0, len(search)):
        text = text.replace(search[i], replace[i])
        
    text = text.strip()
    
    return text

def prep_df_text(df):
    '''
    input: dataframe with text in "Text" column
    output: dataframe with cleaned Arabic text in 'Text' col
    '''
    df['clean_text'] = df['Text'].apply(lambda x: clean_text(x))
    df['new_clean_text'] = df['clean_text'].apply(lambda x: x[x.find(']')+1:])

    return df 

def token_and_model(df):
    '''
    input: dataframe with cleaned, prepped Arabic text
    output: model made from tokenized docs
    '''

    sentences = []
    for line in df['Text']:
        sentences.append(utils.simple_preprocess(line))
    
    model = gensim.models.Word2Vec(sentences)

    return model

print("you made it!")