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

def clean_text(text):
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
    df['clean_text'] = df['clean_text'].apply(lambda x: x[x.find(']')+1:])
    df.drop(columns='Text', inplace=True)
    return df 

def text_by_year(df):
    '''
    input: dataframe with cleaned, prepped Arabic text in "Text" column
    output: dictionary of dataframes, keyed by year where each value represents a dataframe sliced for that year 
    '''
    
    df['year'] = pd.DatetimeIndex(df['Dateline']).year

    year_set = set(df['year'])

    df_holder = []
    for year in year_set:
        df_holder.append("df"+"_"+str(year))

    year_dict = {}
    for dfh, year in zip(df_holder, year_set):
        year_dict[dfh] = df[df['year'] == year]

    return year_dict

#tokenizing and modeling 

def token_and_model(year_dict):
    '''
    input: dictionary of dataframes sliced by year with cleaned, prepped Arabic text
    output: list of models for each dataframe
    '''
    df_set = set(year_dict.keys())
    
    model_names = []
    for df in df_set:
        model_names.append('model'+'_'+str(df))

    model_dict = {}

    for i, (df, model_name) in enumerate(zip(year_dict.items(), model_holder)):
        sentences = [] 
        for line in df[1]['clean_text']:
            sentences.append(utils.simple_preprocess(line))
    model = gensim.models.Word2Vec(sentences)

    model_dict[model_name] = model

    return model_dict
#dimensionaltiy reduction for isu

def reduce_dimensions(model):
    num_dimensions = 2  # final num dimensions (2D, 3D, etc)

    # extract the words & their vectors, as numpy arrays
    vectors = np.asarray(model.wv.vectors)
    labels = np.asarray(model.wv.index_to_key)  # fixed-width numpy strings

    # reduce using t-SNE
    tsne = TSNE(n_components=num_dimensions, random_state=0)
    vectors = tsne.fit_transform(vectors)

    x_vals = [v[0] for v in vectors]
    y_vals = [v[1] for v in vectors]
    
    return x_vals_2d, y_vals_2d, labels_2d

def plot_n_closest(model, word, n):

    word_dict = {}
    for i, w in enumerate(labels):
        word_dict[w] = (x_vals[i], y_vals[i])


    label_list = []
    x_list = []
    y_list = []
    sim_list = model.wv.most_similar(positive=[word], topn=n)
    for i, v in enumerate(sim_list):
        label_list.append(sim_list[i][0])
        x_list.append(word_dict[sim_list[i][0]][0])
        y_list.append(word_dict[sim_list[i][0]][1])
    

    return plot_function(x_list, y_list, label_list)



print("helper functions loaded successfully!")