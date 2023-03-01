from pynytimes import NYTAPI
import pandas as pd
import openpyxl

import os
from dotenv import load_dotenv
import json
import datetime

user_topic = input("Which topic would you like to explore? (50 articles will be returned) ")
user_beginning_date = input("What should be the earliest date for the articles? (enter as: 1/28/2022) ")
user_end_date = input("What should be the latest date for the articles? (enter as: 1/31/2022) ")

def date_string(date):
    year = int(date.split("/")[2])
    month = int(date.split("/")[0])
    day = int(date.split("/")[1])

    return year, month, day

def clean_words(words):
    new_words = ""
    for character in words:
        if character.isalnum() or character == " " or character == "#" or character == "'" or character == "-":
            new_words += character.lower()
    return new_words

load_dotenv() # look in the ".env" file for env vars

API_KEY = os.getenv("NY_API_KEY")

nyt = NYTAPI(API_KEY, parse_dates=True)

beg_year, beg_month, beg_day = date_string(user_beginning_date)
end_year, end_month, end_day = date_string(user_end_date)

articles = nyt.article_search(
    query = user_topic,
    results = 50,
    dates = {
        "begin": datetime.datetime(beg_year, beg_month, beg_day),
        "end": datetime.datetime(end_year, end_month, end_day)
    },
    options = {
        "sort": "oldest",
        "sources": [
            "New York Times",
            "AP",
            "Reuters",
            "International Herald Tribune"
        ],
        "type_of_material": [
            "News"
        ]
    }
)

articles_JSON = json.dumps(articles, default=str)
df = pd.read_json(articles_JSON)

#Sheet 1 - Data
df = df.reset_index()
df["Main Headline"] = df["headline"].apply(lambda x: x["main"])
df["Date"] = df["pub_date"].apply(lambda x: x[:10])
df["Time"] = df["pub_date"].apply(lambda x: x[10:19])

#Sheet 2 - Abstract Words
df_sheet2 = df[["index","abstract"]]

list_sheet2 = []
for i in range(len(df_sheet2)):
    words_list = clean_words(df_sheet2["abstract"].loc[i]).split()
        
    for x in range(len(words_list)):
        index_word = [i, words_list[x]]
        list_sheet2.append(index_word)
        
df_sheet2 = pd.DataFrame(list_sheet2)
df_sheet2 = df_sheet2.rename(columns={0:"Article Id", 1:"Abstract Words"})

#Sheet 3 - Headline Words
df_sheet3 = df[["index","Main Headline"]]

list_sheet3 = []
for i in range(len(df_sheet3)):
    words_list = clean_words(df_sheet3["Main Headline"].loc[i]).split()
        
    for x in range(len(words_list)):
        index_word = [i, words_list[x]]
        list_sheet3.append(index_word)
        
df_sheet3 = pd.DataFrame(list_sheet3)
df_sheet3 = df_sheet3.rename(columns={0:"Article Id", 1:"Main Headline Words"})

#Sheet 4 - Article Keywords
df_sheet4 = df[["index","keywords"]]

list_sheet4 = []
for i in range(len(df_sheet4)):
    for x in range(len(df_sheet4["keywords"].loc[i])):
        keyword = df_sheet4["keywords"].loc[i][x]["value"]
        index_word = [i, keyword]
        list_sheet4.append(index_word)

df_sheet4 = pd.DataFrame(list_sheet4)
df_sheet4 = df_sheet4.rename(columns={0:"Article Id", 1:"Main Headline Words"})

#to Excel!
df = df.rename(columns={"index":"Id"})

file_name = user_topic + " .xlsx"

with pd.ExcelWriter(file_name) as writer:  
    df.to_excel(writer, sheet_name='Data')
    df_sheet2.to_excel(writer, sheet_name='Abstract Words')
    df_sheet3.to_excel(writer, sheet_name='Headline Words')
    df_sheet4.to_excel(writer, sheet_name='Article Keywords')