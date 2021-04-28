import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_read_xml as pdx 
import re

import gensim
from gensim.test.utils import datapath
from gensim import utils
import gensim.models

from plotly.subplots import make_subplots
from plotly.offline import init_notebook_mode, iplot, plot
import plotly.graph_objs as go

from nltk import ngrams

from sklearn.decomposition import IncrementalPCA    
from sklearn.manifold import TSNE 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
#import src.stop_words

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

    for i, (df, model_name) in enumerate(zip(year_dict.items(), model_names)):
        sentences = [] 
        for line in df[1]['clean_text']:
            sentences.append(utils.simple_preprocess(line))
        model = gensim.models.Word2Vec(sentences)

        model_dict[model_name] = model

    return model_dict

def reduce_dimensions(model_dict):
    '''
    inputs: dictionary of models 
    outputs: dictionary keyed by country_year where each item is a dataframe with three columns, x_vals,
    y_vals, and labels that correspond to the x and y coordiantes for each label (tokenized word) in the model
    '''
    dim_red_dict = {}

    year = []
    for m in model_dict.items():
        year.append(str(m[0][-4:]))
    

    for model, y in zip(model_dict.values(), year):
        num_dimensions = 2  # final num dimensions (2D, 3D, etc)
        print('done with setting dimensions')
    
        # extract the words & their vectors, as numpy arrays
        vectors = np.asarray(model.wv.vectors)
        labels = np.asarray(model.wv.index_to_key)  # fixed-width numpy strings
        print('done with vectors and labels')
    
        # reduce using t-SNE
        tsne = TSNE(n_components=num_dimensions, random_state=0)
        vectors = tsne.fit_transform(vectors)
        print('done with tsne')
    
        x_vals = [v[0] for v in vectors]
        y_vals = [v[1] for v in vectors]
        print('done assigning x_vals and y_vals')

        dim_red_dict[y] = pd.DataFrame({'year': y, 'x_vals':x_vals, 'y_vals':y_vals, 'labels':labels})
        print('done with dataframing')    
    
    final_df = pd.concat(dim_red_dict.values(), ignore_index=True)
    
    print('ALL done')

    return final_df
 

def plot_n_closest(final_df, model_dict, word, n, year_a, year_b):
    '''
    inputs: dimensionally reduced dictionary for specific country, word of interest, n nearest neighbors to 
    that word, year a and year b for comparison 
    '''
    #selects models associated with year_a and year_b
    for m in model_dict.items():
        if year_a == int(m[0][-4:]):
            model_a = m[1]
        if year_b == int(m[0][-4:]):
            model_b = m[1]
        else:
            None 

    #generates list of similar words based on input word for each year(a or b) model
    sim_list_a = model_a.wv.most_similar(positive=[word], topn=n)
    sim_list_b = model_b.wv.most_similar(positive=[word], topn=n)

    #holders for values to be graphed
    label_list_a = []
    x_list_a = []
    y_list_a = []

    label_list_b = []
    x_list_b = []
    y_list_b = []

    for i, v in enumerate(sim_list_a):
        curr_label = sim_list_a[i][0]
        label_list_a.append(curr_label)
        x_list_a.append(final_df.loc[final_df['labels'] == curr_label, 'x_vals'].iloc[0])
        y_list_a.append(final_df.loc[final_df['labels'] == curr_label, 'y_vals'].iloc[0])
    
    for i, v in enumerate(sim_list_b):
        curr_label = sim_list_b[i][0]
        label_list_b.append(curr_label)
        x_list_b.append(final_df.loc[final_df['labels'] == curr_label, 'x_vals'].iloc[0])
        y_list_b.append(final_df.loc[final_df['labels'] == curr_label, 'y_vals'].iloc[0])
    
    fig = make_subplots(rows=1, cols=2)
    
    trace_a = go.Scatter(x=x_list_a, y=y_list_a, mode='text', text=label_list_a, name=f"{word}, {year_a}")
    trace_b = go.Scatter(x=x_list_b, y=y_list_b, mode='text', text=label_list_b, name=f"{word}, {year_b}")
 
    fig.add_trace((trace_a), row=1, col=1)
    fig.add_trace((trace_b), row=1, col=2)

    fig.update_layout(height=600, width=800, 
    title_text=f"Word Embedding Comparison: {n} nearest neighbors for {word}, between {year_a} and {year_b}")
           


    return fig.show() 


def lda_vectorizer(df, col, num_topics, num_features):
    '''
    Input: dataframe, column for vectorizing, number of topics, number of features
    Output: Df with columns that represented featurized topics for a column of text values

    '''
    docs = df[col]

    tf_vectorizer = CountVectorizer(max_df=0.95,
                                    min_df=2,
                                    max_features=num_features,
                                    stop_words=src.stop_words.ar_stop_words)

    tf = tf_vectorizer.fit_transform(docs)
    tf_feature_names = tf_vectorizer.get_feature_names() # theses are the words in our bag of words
    tf

    #LDA on 'description' column for 10 topics
    lda = LatentDirichletAllocation(n_components=num_topics,
                                    max_iter=5,
                                    learning_method='online',
                                    random_state=0,
                                    n_jobs=-1)
    lda.fit(tf)

    #Add dataframe back to df showing how topic-y each document is for each of the n topics

    #lda.transform(tf) is the matrix showing topicy-ness for each document and its n topics
    # convertiny lda array into dataframe for concatentation 
    lda_desc_df = pd.DataFrame(lda.transform(tf))
    df = pd.concat([df, lda_desc_df], axis=1)
    
    return df 


print("helper functions loaded successfully!")