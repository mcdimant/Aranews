# Aranews

## Introduction
How does a national media cover a specific topic? How does this change over time? Is it possible to discern subtle (or not so subtle) changes in the discourse around a single "word" by looking at thousands of news articles over sevearl years? Answering these questions inspired this project, which examines a corpus of Arabic news articles using word embeddings to see changes in word-associations for specific key-words over time. This analysis gives us the ability to see trends in how Arabic medias covered specific topics over time, for instance, the association of words around "Democracy" (ديمقراطية) may be different in 2009 (pre-Arab Spring) than in 2014 (post or in the middle of political transitions/upheaval). 

## Word Embedding
Word embedding is technique in natural language processing (NLP) that quantifies distance between words based on proximate association of those words. For example, a word embedding on a corpus of English litearture, if given the word "king" would likely return "queen, royal, prince, castle, ruler, monarch". 

## Data Source
Analysis of word embedding in [corpus of Arabic news articles](https://abuelkhair.net/index.php/en/arabic/abu-el-khair-corpus) prepared by Egyptian research Ibrahim Abu el-Khair from 8 Arabic-speaking countries. Each country's data was accessible as an XML file but since they required extensive cleanup to remove offending characters, this analysis uses the smallest file (Yemen) to demonstrate a proof of concept. 

### Yemen News Data
The Yemeni part of the corpus contains 92148 articles comprising 283983 distinct words from December 2009 to May 2014. All of the articles are from the [Saba News Agency](https://www.sabanew.net/), a state run media outlet. Abu el-Khair's methodology for choosing articles is unclear, so I performed a Latent Dirichlet Analysis (LDA) to discern topics within the Yemeni articles. After experimenting with various numbers of topics, I found that I could identify 6 more-or-less distinct topics within the Yemeni part of the corpus:

* Histogram of Yemeni News Article Length
![](images/histogram.png)


#### TFIDF and LDA 

| TFIDF Vectorizer | |LDA Hyperparameters   |       
| ------------- |--------------------| ----------------|-------|
| max_df        | .95                | n_component     |6      |
| min_df        | 2                  | max_iter        |5      |
| max_features  | 1000               | learning_method |online |
| stop_words    | (Arabic stop words)| random_state    |0      |


* Topic 0: Security / Defense Affairs
الامن الامنيه قوات المسلحه القوات العسكريه اللواء الشرطه الدفاع مدينه منطقه الجيش الداخليه جنوب المنطقه المواطنين وزاره الركن محافظه الانباء

* Topic 1: Economy / development
عدن اليمنيه الدوره الصحه مجال الانباء المجتمع لوكاله مدير صنعاء اليمن العامه الاطفال العام للتنميه العمل مشروع الصحيه الورشه بعدن

* Topic 2: Local politics
المحافظه بالمحافظه العامه الاجتماع محمد اهميه وكيل المحليه اللجنه مدير مكتب المجلس العام محافظه صنعاء احمد عبد العمل المحلي الدكتور

* Topic 3: National politics
اليمن رئيس الوطني الحوار وزير العربيه الرئيس صنعاء مجلس التعاون الاخ مؤتمر اليمنيه الجمهوريه السياسيه اللقاء الدكتور محمد عبد اليمني

* Topic 4: Regional Arab politics / sports
نقطه الاحتلال المركز فريق الفلسطينيه الاسرائيلي سوريا القدم القاهره لكره الاولي الاتحاد البطوله المصريه فيما المصري الفلسطيني مصر القدس الدور

* Topic 5: International politics
المتحده العام الحكومه المائه الخارجيه الامريكيه الاوروبي الامم الامريكي الدولي الدوليه الاتحاد الانسان الولايات الصين الدول بنسبه بشان بيان مستوي

(Even when I added additional topics, the LDA appeared to conflate terms associaed with sports and regional Arab news)


## The pipeline

## 