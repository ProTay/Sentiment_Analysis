#SMAL 2024
#Written by Ahmad Y.
#Code for running sentiment analysis
import nltk
import pandas as pd
import re
import plotly.graph_objs as go
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# This is a Sentiment Analysis by using existed csv.file
# you have to set your own word_dictionary to help deal with data

# set Sentiment dictory
word_dict = {'manipulate': -1, 'manipulative': -1, 'jamescharlesiscancelled': -1, 'jamescharlesisoverparty': -1,
             'pedophile': -1, 'pedo': -1, 'cancel': -1, 'cancelled': -1, 'cancel culture': 0.4, 'teamtati': -1,
             'teamjames': 1,
             'teamjamescharles': 1, 'liar': -1, 'goat' : 1, 'Goat': 1} # ----- Added 'goat' and 'Goat' to the list -----

# twitter data cleaner

nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()
sid.lexicon.update(word_dict)
nltk.download('words')
words = set(nltk.corpus.words.words())
folder_path = 'C:/Users/itztt/Downloads/AI-Content' # ----- Added 'C:/Users/itztt/Downloads/AI-Content' as the folder_path -----



# Loop over the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        print(f'File: {filename}')
        result_path = filename.rstrip(".csv") + "Result_V2.xlsx" 
        df = pd.read_csv(file_path, encoding='latin1')  # Try 'latin1' or 'utf-16' if 'utf-8' doesn't work
        # -------------------------------------------------------------------

        # it will return you a number, Closer to -1, more negative, closer to 1，more positive
        cList = ["Comment1" , "Comment2" , "Comment3", "Comment4", "Comment5", "Comment6", "Comment7", "Comment8", "Comment9", "Comment10"]
        df = df.dropna(subset= cList, how="all")
        print(df[cList] , "Just Comments \n")
        
        for i in df[cList].iloc[:]:
          print(sid.polarity_scores(i)['compound'])
        
        with open('output2.txt', 'w', encoding= 'utf-8') as f:
            f.write(df.to_string(index =False))

        # a filter for data cleaning
        
        def capitalize_sentence(match):
           return match.group(1) + match.group(2).upper()
        def cleaner(text):
            if (pd.isna(text)):
                text =''       
            text = re.sub(r'\d+', '', text)
            text = re.sub("@[A-Za-z0-9]+", "", text)  # Remove @ sign
            text = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", text)  # Remove http links
            text = " ".join(text.split())
            text = text.replace("#", "").replace("_", " ")  # Remove hashtag sign but keep the text
            text = " ".join(w for w in nltk.wordpunct_tokenize(text)
                            if w.lower() in words or not w.isalpha())
            text = re.sub(r'[^a-zA-Z\s]', " ", text)
            try:
                if detect(text) == 'en':
                    text = re.sub(r'([.!?]\s+)(\w)', capitalize_sentence, text)
    
                    # Capitalize the very first letter if it's a sentence start
                    text = text[0].upper() + text[1:]
                    
                    # Ensure proper spacing around punctuation
                    text = re.sub(r'\s*([.,!?])\s*', r'\1 ', text)
                    text = re.sub(r'\s{2,}', ' ', text)  # Replace multiple spaces with a single space
                    text = re.sub(r'\s+([.,!?])', r'\1', text)  # Remove space before punctuation
                    
                    # Strip leading/trailing spaces
                    text = text.strip()
                    return text
                else:
                    return ''
            except LangDetectException:
                return ''
            
            

        # deploying the filter
        for i in cList:
            df[i+'_clean'] = df[i].apply(cleaner)
        
        with open('output2.txt', 'w', encoding= 'utf-8') as f:
            f.write(df.to_string(index =False)) 
            
        new_cList = df.columns[32:42] 
        

        list1 = []
        for i in range(len(df[new_cList])):
            result = 0
            for v in df[new_cList].iloc[i]:
                result+=(sid.polarity_scores(str(v)))['compound']
            list1.append(result)

        df['sentiment'] = list1
        
        with open('output2.txt', 'w', encoding= 'utf-8') as f:
            f.write(df.to_string(index =False)) 


        def sentiment_category(sentiment):
            label = ''
            if sentiment > 0:
                label = 'positive'
            elif sentiment == 0:
                label = 'neutral'
            else:
                label = 'negative'
            return label


        df['sentiment_category'] = df['sentiment'].apply(sentiment_category)
        
        with open('output2.txt', 'w', encoding= 'utf-8') as f:
            f.write(df.to_string(index =False)) 
            
        print(df.columns)
        print(new_cList)
        
        select_column = ["ID", 'Post Created','sentiment_category']
        for i in new_cList:
            select_column.append(i)
        print(select_column, "New Columns")
        
        # Write the DataFrame to an Excel file
        df.to_excel(result_path, index=False)
        
        
        df = df[select_column]
        print(df.head())
        with open('output2.txt', 'w', encoding= 'utf-8') as f:
            f.write(df.to_string(index =False)) 

        # Sets what properties to use as criteria for line charts
        neg = df[df['sentiment_category']=='negative']
        neg = neg.groupby(['Post Created'],as_index=False).count()
        pos = df[df['sentiment_category']=='positive']
        pos = pos.groupby(['Post Created'],as_index=False).count()
        pos = pos[['Post Created','ID']]
        neg = neg[['Post Created','ID']]

        # draw line graph
        fig = go.Figure()
        for col in pos.columns:
            fig.add_trace(go.Scatter(x=pos['Post Created'], y=pos['ID'],
                                    name = col,
                                    mode = 'markers+lines',
                                    line=dict(shape='linear'),
                                    connectgaps=True,
                                    line_color='green'
                                    )
                        )
        for col in neg.columns:
            fig.add_trace(go.Scatter(x=neg['Post Created'], y=neg['ID'],
                                    name = col,
                                    mode = 'markers+lines',
                                    line=dict(shape='linear'),
                                    connectgaps=True,
                                    line_color='red'
                                    )
                        )
        fig.update_layout(title= filename)
        fig.show()
        
    elif os.path.isdir(file_path):
        print(f'Directory: {filename}')