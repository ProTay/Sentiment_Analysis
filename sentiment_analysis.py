# Base and Cleaning
import pandas as pd

#-----------------------*New Code---------------------------------
# - Install openpyxl , textblob , matplotlib
# - Import  textblob , matplotlib
import matplotlib.pyplot as plt
from textblob import TextBlob
import numpy as np
import openpyxl
import os
import re

#-----------------------*New Code---------------------------------
# read an excel file and convert into a dataframe object
# Specify the folder path
folder_path = 'C:/Users/itztt/Downloads/AI-Content'

# Loop over the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        print(f'File: {filename}')
        result_path = filename.rstrip(".csv") + "Result.xlsx" 
        df = pd.read_csv(file_path, encoding='latin1')  # Try 'latin1' or 'utf-16' if 'utf-8' doesn't work
        # -------------------------------------------------------------------

        # Export to a text file
        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write(df.to_string(index=False))

        commentList = list(df.columns[22:32])
        # new_df = df[commentList].values != "NaN"
        df = df.dropna(subset=commentList, how='all')
        df = df.iloc[:,:32]

        with open('output.txt', 'w', encoding= 'utf-8') as f:
            f.write(df.to_string(index =False))

        # read the csv file into dataframe
        # df = pd.read_csv()
        # show the dataframe 
        # df 

        # Sentiment Analysis
        # make sure you have installed textblob in the terminal first: pip install textblob

        # Get the sentiments for each tweet
        print(df)
        cList = ["Comment1" , "Comment2" , "Comment3", "Comment4", "Comment5", "Comment6", "Comment7", "Comment8", "Comment9", "Comment10"]
        sentiment = []
        for i in range(len(df)):
            new_df = df[cList].iloc[i]
            for value in new_df:
                if isinstance(value, float):
                    sentiment.append(0)
                else:
                    sentiment.append(TextBlob(str(value)).sentiment.polarity)
    



        index = 0
        new_sentiment = []
        for i in range(10):
            result = 0
            for j in range(10):
                result+=sentiment[index]
                index+=1
            new_sentiment.append(result)

        #Get the subjectivity of each tweet
        subjectivity = []
        for i in range(len(df)):
            new_df = df[cList].iloc[i]
            for value in new_df:
                subjectivity.append(TextBlob(str(value)).sentiment.subjectivity)

        index = 0
        new_subjectivity = []
        for i in range(10):
            result = 0
            for j in range(10):
                result+=subjectivity[index]
                index+=1
            new_subjectivity.append(result)

        df["sentiment"] = new_sentiment
        df["subjectivity"] = new_subjectivity


        with open('output.txt', 'w', encoding= 'utf-8') as f:
            f.write(df.to_string(index =False))

        print(df)
        sentimenttotal = 0.0
        for i in range(len(df)):
            sentimenttotal += df.iloc[i, 32]

        subjectivitytotal = 0.0
        for i in range(len(df)):
            subjectivitytotal += df.iloc[i, 33]

        with open('output.txt', 'w', encoding= 'utf-8') as f:
            f.write(df.to_string(index =False))


        print(df.columns)
        # Posts with zero engagement
        count = 0
        for i in range(len(df)):
            if (df.iloc[i, 10] == 0 & df.iloc[i, 9] == 0):
                count += 1
        # total posts
        print("num of total posts:", len(df))
        # no engagement tweet
        print("num of posts with no engagement:", count)
        # percent no engagement
        print("percent of posts with no engagement:", count / len(df))

        sentimentavg = sentimenttotal / len(df)
        subjectivityavg = subjectivitytotal / len(df)
        print("sentiment avg:", sentimentavg)
        print("subjectivity:", subjectivityavg)

        liketotal = 0.0
        for i in range(len(df)):
            liketotal += df.iloc[i, 9]

        replytotal = 0.0
        for i in range(len(df)):
            replytotal += df.iloc[i, 10]

        # # retweettotal = 0.0
        # # for i in range(len(df)):
        # #     retweettotal += df.loc[i, "public_metrics.retweet_count"]

        # # quotetotal = 0.0
        # # for i in range(len(df)):
        # #     quotetotal += df.loc[i, "public_metrics.quote_count"]

        # likeavg = liketotal / len(df)
        # replyavg = replytotal / len(df)
        # # retweetavg = retweettotal / len(df)
        # # quoteavg = quotetotal / len(df)
        # print("like avg:", likeavg)
        # print("reply avg:", replyavg)
        # # print("retweet avg:", retweetavg)
        # # print("quote avg:", quoteavg)

        # remove outliers for likes
        pd_series_likes = df['Likes']
        pd_series_adjusted = pd_series_likes[
            pd_series_likes.between(pd_series_likes.quantile(.01), pd_series_likes.quantile(.99))]
        df['Likes_no_outliers'] = pd_series_adjusted

        # remove outliers for replies
        pd_series_reply = df['Comments']
        pd_series_adjusted = pd_series_reply[
            pd_series_reply.between(pd_series_reply.quantile(.01), pd_series_likes.quantile(.99))]
        df['Comments_no_outliers'] = pd_series_adjusted

        with open('output.txt', 'w', encoding= 'utf-8') as f:
            f.write(df.to_string(index =False))


        df.plot(x='sentiment', y='Likes', style='o', figsize=(20, 10))
        df.plot(x='sentiment', y='Comments', style='o', figsize=(20, 10))
        df.plot(x='sentiment', y='Likes_no_outliers', style='o', figsize=(20, 10))
        df.plot(x='sentiment', y='Comments_no_outliers', style='o', figsize=(20, 10))

        # # number of posts with positive sentiment
        print("num of posts with positive sentiment:", (df["sentiment"] > 0).sum())
        # percent
        print("percent of posts with positive sentiment:", (df["sentiment"] > 0).sum() / len(df))

        # number of posts with neutral sentiment
        print("num of posts with neutral sentiment:", (df["sentiment"] == 0).sum())
        # percent
        print("percent of posts with neutral sentiment:", (df["sentiment"] == 0).sum() / len(df))

        # number of posts with negative sentiment
        print("num of posts with negative sentiment:", (df["sentiment"] < 0).sum())
        # percent
        print("percent of posts with negative sentiment:", (df["sentiment"] < 0).sum() / len(df))

        pattern = re.compile(
        r'[^\w\s]|[^\u0600-\u06FF\u0400-\u04FF\u1F600-\u1F64F\u1F300-\u1F5FF\u1F680-\u1F6FF]+',              
                                    # Specific special characters
            #r'|[\u0600-\u06FF]'    # Arabic
            #r'|[\u0400-\u04FF]',   # Cyrillic
            #r'|[\u1F600-\u1F64F]'  # Emoticons
            #r'|[\u1F300-\u1F5FF]'  # Miscellaneous Symbols and Pictographs
            #r'|[\u1F680-\u1F6FF]'  # Transport and Map Symbols
            #r'|[\u1F700-\u1F77F]'  # Alchemical Symbols
            #r'|[\u1F780-\u1F7FF]'  # Geometric Shapes Extended
            #r'|[\u1F800-\u1F8FF]'  # Supplemental Arrows-C
            #r'|[\u1F900-\u1F9FF]'  # Supplemental Symbols and Pictographs
            #r'|[\u1FA00-\u1FA6F]'  # Chess Symbols
            #r'|[\u1FA70-\u1FAFF]'  # Symbols and Pictographs Extended-A
            #r'|[\u1FB00-\u1FBFF]',  # Symbols for Legacy Computing
                                
        re.UNICODE | re.UNICODE
            
        )

        hashtages = []
        for i in range(len(df[cList])):
            my_str = ''
            for j in range(len(cList)):
                my_str+= str(df[cList].iloc[i, j]).lower()
                my_str+= " "
            hashtages.append(pattern.findall(my_str))

        df["hashtags"] = hashtages


        with open('output.txt', 'w', encoding= 'utf-8') as f:
            f.write(df.to_string(index =False))

        # df["hashtags"] = df[cList].str.lower().str.findall(r'#.*?(?=\s|$)')
        # print(df["hashtags"])

        # method to create a hashtag dictionary
        def to_1D(series):
            return pd.Series([x for _list in series for x in _list])

        a = to_1D(df["hashtags"]).value_counts().to_string()[:3000]
        print(a)


        with open('output.txt', 'w', encoding= 'utf-8') as f:
            f.write(df.to_string(index =False))


            

        # Write the DataFrame to an Excel file
        df.to_excel(result_path, index=False)

        print(f"Data has been successfully written to {"xlsx_file_path"}")

    elif os.path.isdir(file_path):
        print(f'Directory: {filename}')

# file_path = r'C:/Users/itztt/Downloads/2019 NatGeo Data_Final(Sheet1).csv'
# df = pd.read_csv(file_path, encoding='latin1')  # Try 'latin1' or 'utf-16' if 'utf-8' doesn't work
# # -------------------------------------------------------------------

# # Export to a text file
# with open('output.txt', 'w', encoding='utf-8') as f:
#     f.write(df.to_string(index=False))

# commentList = list(df.columns[22:32])
# df[commentList]
# # new_df = df[commentList].values != "NaN"
# df = df[df[commentList].notnull().all(axis =1)]
# df = df.iloc[:,:32]

# with open('output.txt', 'w', encoding= 'utf-8') as f:
#     f.write(df.to_string(index =False))

# # read the csv file into dataframe
# # df = pd.read_csv()
# # show the dataframe 
# # df 

# # Sentiment Analysis
# # make sure you have installed textblob in the terminal first: pip install textblob

# # Get the sentiments for each tweet
# cList = ["Comment1" , "Comment2" , "Comment3", "Comment4", "Comment5", "Comment6", "Comment7", "Comment8", "Comment9", "Comment10"]
# sentiment = []
# for i in range(len(df)):
#    new_df = df[cList].iloc[i]
#    for value in new_df:
#       if isinstance(value, float):
#          sentiment.append(0)
#       else:
#         sentiment.append(TextBlob(str(value)).sentiment.polarity)



# index = 0
# new_sentiment = []
# for i in range(10):
#    result = 0
#    for j in range(10):
#     result+=sentiment[index]
#     index+=1
#    new_sentiment.append(result)

# #Get the subjectivity of each tweet
# subjectivity = []
# for i in range(len(df)):
#     new_df = df[cList].iloc[i]
#     for value in new_df:
#      subjectivity.append(TextBlob(str(value)).sentiment.subjectivity)

# index = 0
# new_subjectivity = []
# for i in range(10):
#    result = 0
#    for j in range(10):
#     result+=subjectivity[index]
#     index+=1
#    new_subjectivity.append(result)

# df["sentiment"] = new_sentiment
# df["subjectivity"] = new_subjectivity


# with open('output.txt', 'w', encoding= 'utf-8') as f:
#     f.write(df.to_string(index =False))

# print(df)
# sentimenttotal = 0.0
# for i in range(len(df)):
#      sentimenttotal += df.iloc[i, 32]

# subjectivitytotal = 0.0
# for i in range(len(df)):
#      subjectivitytotal += df.iloc[i, 33]

# with open('output.txt', 'w', encoding= 'utf-8') as f:
#     f.write(df.to_string(index =False))


# print(df.columns)
# # Posts with zero engagement
# count = 0
# for i in range(len(df)):
#     if (df.iloc[i, 10] == 0 & df.iloc[i, 9] == 0):
#         count += 1
# # total posts
# print("num of total posts:", len(df))
# # no engagement tweet
# print("num of posts with no engagement:", count)
# # percent no engagement
# print("percent of posts with no engagement:", count / len(df))

# sentimentavg = sentimenttotal / len(df)
# subjectivityavg = subjectivitytotal / len(df)
# print("sentiment avg:", sentimentavg)
# print("subjectivity:", subjectivityavg)

# liketotal = 0.0
# for i in range(len(df)):
#     liketotal += df.iloc[i, 9]

# replytotal = 0.0
# for i in range(len(df)):
#     replytotal += df.iloc[i, 10]

# # # retweettotal = 0.0
# # # for i in range(len(df)):
# # #     retweettotal += df.loc[i, "public_metrics.retweet_count"]

# # # quotetotal = 0.0
# # # for i in range(len(df)):
# # #     quotetotal += df.loc[i, "public_metrics.quote_count"]

# # likeavg = liketotal / len(df)
# # replyavg = replytotal / len(df)
# # # retweetavg = retweettotal / len(df)
# # # quoteavg = quotetotal / len(df)
# # print("like avg:", likeavg)
# # print("reply avg:", replyavg)
# # # print("retweet avg:", retweetavg)
# # # print("quote avg:", quoteavg)

# # remove outliers for likes
# pd_series_likes = df['Likes']
# pd_series_adjusted = pd_series_likes[
#     pd_series_likes.between(pd_series_likes.quantile(.01), pd_series_likes.quantile(.99))]
# df['Likes_no_outliers'] = pd_series_adjusted

# # remove outliers for replies
# pd_series_reply = df['Comments']
# pd_series_adjusted = pd_series_reply[
#     pd_series_reply.between(pd_series_reply.quantile(.01), pd_series_likes.quantile(.99))]
# df['Comments_no_outliers'] = pd_series_adjusted

# with open('output.txt', 'w', encoding= 'utf-8') as f:
#     f.write(df.to_string(index =False))


# df.plot(x='sentiment', y='Likes', style='o', figsize=(20, 10))
# df.plot(x='sentiment', y='Comments', style='o', figsize=(20, 10))
# df.plot(x='sentiment', y='Likes_no_outliers', style='o', figsize=(20, 10))
# df.plot(x='sentiment', y='Comments_no_outliers', style='o', figsize=(20, 10))

# # # number of posts with positive sentiment
# print("num of posts with positive sentiment:", (df["sentiment"] > 0).sum())
# # percent
# print("percent of posts with positive sentiment:", (df["sentiment"] > 0).sum() / len(df))

# # number of posts with neutral sentiment
# print("num of posts with neutral sentiment:", (df["sentiment"] == 0).sum())
# # percent
# print("percent of posts with neutral sentiment:", (df["sentiment"] == 0).sum() / len(df))

# # number of posts with negative sentiment
# print("num of posts with negative sentiment:", (df["sentiment"] < 0).sum())
# # percent
# print("percent of posts with negative sentiment:", (df["sentiment"] < 0).sum() / len(df))

# pattern = re.compile(
#    r'[^\w\s]|[^\u0600-\u06FF\u0400-\u04FF\u1F600-\u1F64F\u1F300-\u1F5FF\u1F680-\u1F6FF]+',              
#                             # Specific special characters
#     #r'|[\u0600-\u06FF]'    # Arabic
#     #r'|[\u0400-\u04FF]',   # Cyrillic
#     #r'|[\u1F600-\u1F64F]'  # Emoticons
#     #r'|[\u1F300-\u1F5FF]'  # Miscellaneous Symbols and Pictographs
#     #r'|[\u1F680-\u1F6FF]'  # Transport and Map Symbols
#     #r'|[\u1F700-\u1F77F]'  # Alchemical Symbols
#     #r'|[\u1F780-\u1F7FF]'  # Geometric Shapes Extended
#     #r'|[\u1F800-\u1F8FF]'  # Supplemental Arrows-C
#     #r'|[\u1F900-\u1F9FF]'  # Supplemental Symbols and Pictographs
#     #r'|[\u1FA00-\u1FA6F]'  # Chess Symbols
#     #r'|[\u1FA70-\u1FAFF]'  # Symbols and Pictographs Extended-A
#     #r'|[\u1FB00-\u1FBFF]',  # Symbols for Legacy Computing
                           
#    re.UNICODE | re.UNICODE
    
# )

# hashtages = []
# for i in range(len(df[cList])):
#    my_str = ''
#    for j in range(len(cList)):
#       my_str+= df[cList].iloc[i, j].lower()
#       my_str+= " "
#    hashtages.append(pattern.findall(my_str))

# df["hashtags"] = hashtages


# with open('output.txt', 'w', encoding= 'utf-8') as f:
#     f.write(df.to_string(index =False))

# # df["hashtags"] = df[cList].str.lower().str.findall(r'#.*?(?=\s|$)')
# # print(df["hashtags"])

# # method to create a hashtag dictionary
# def to_1D(series):
#    return pd.Series([x for _list in series for x in _list])

# a = to_1D(df["hashtags"]).value_counts().to_string()[:3000]
# print(a)


# with open('output.txt', 'w', encoding= 'utf-8') as f:
#     f.write(df.to_string(index =False))


    

# # Write the DataFrame to an Excel file
# df.to_excel("output.xlsx", index=False)

# print(f"Data has been successfully written to {"xlsx_file_path"}")