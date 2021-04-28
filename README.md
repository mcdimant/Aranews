# Aranews

## Introduction
How does a national media cover a specific topic? How does this change over time? Is it possible to discern subtle (or not so subtle) changes in the discourse around a single "word" by looking at thousands of news articles over sevearl years? Answering these questions inspired this project, which examines a corpus of Arabic news articles using word embeddings to see changes in word-associations for specific key-words over time. This analysis gives us the ability to see trends in how Arabic medias covered specific topics over time, for instance, the association of words around "Democracy" (ديمقراطية) may be different in 2009 (pre-Arab Spring) than in 2014. 

## Word Embedding
Word embedding is technique in natural language processing (NLP) that quantifies distance between words based on proximate association of those words. For example, a word embedding on a corpus of English litearture, if given the word "king" would likely return "queen, royal, prince, castle, ruler, monarch". 

## Data Source
Analysis of word embedding in [corpus of Arabic news articles](https://abuelkhair.net/index.php/en/arabic/abu-el-khair-corpus) prepared by Egyptian research Ibrahim Abu el-Khair from 8 Arabic-speaking countries. Each country's data was accessible as an XML file but since they required extensive cleanup to remove offending characters, this analysis uses the smallest file (Yemen) to demonstrate a proof of concept. 

### Yemen News Data
The Yemeni part of the corpus contains ___ articles comprising ___ words from December 2009 to May 2014. All of the articles are from the [Saba News Agency](https://www.sabanew.net/), a state run media outlet. Abu el-Khair's methodology for choosing articles is unclear, so I performed a Latent Dirichlet Analysis (LDA) to discern topics within the Yemeni articles. After experimenting with various numbers of topics, I found that I could identify 5 more-or-less distinct topics within the Yemeni part of the corpus:


##### LDA 




## The pipeline

## 