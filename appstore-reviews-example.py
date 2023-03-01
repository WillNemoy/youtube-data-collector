
from pprint import pprint
import json
import datetime

import requests
import pandas as pd
import numpy as np

from openpyxl import Workbook, load_workbook

def appleAPI(appId):

    dfs = []

    for i in range(10):
        try:
            page = i + 1
            
            apple_request = ("https://itunes.apple.com/us/rss/customerreviews/page="
                            + str(page)
                            + "/id="
                            + appId
                            + "/sortBy=mostHelpful/json")

            apple_Json = requests.get(apple_request).json()

            df = pd.DataFrame(apple_Json["feed"]["entry"])

            #fix up the df (convert json to content)
            df["author"] = df["author"].apply(lambda x: x["name"]["label"])
            df["updated"] = df["updated"].apply(lambda x: x["label"])
            df["im:rating"] = df["im:rating"].apply(lambda x: x["label"])
            df = df.rename(columns={"im:rating": "rating"})

            df["im:version"] = df["im:version"].apply(lambda x: x["label"])
            df = df.rename(columns={"im:version": "version"})

            df["id"] = df["id"].apply(lambda x: x["label"])
            df["title"] = df["title"].apply(lambda x: x["label"])
            df["content"] = df["content"].apply(lambda x: x["label"])

            df["link"] = df["link"].apply(lambda x: x["attributes"]["href"])
            df["im:voteSum"] = df["im:voteSum"].apply(lambda x: x["label"])
            df = df.rename(columns={"im:voteSum": "voteSum"})

            df["im:contentType"] = df["im:contentType"].apply(lambda x: x["attributes"]["label"])
            df = df.rename(columns={"im:contentType": "contentType"})

            df["im:voteCount"] = df["im:voteCount"].apply(lambda x: x["label"])
            df = df.rename(columns={"im:voteCount": "voteCount"})


            #create a day and time column
            df["updated day"] = df["updated"].apply(lambda x: x.split("T")[0])
            df["updated time"] = df["updated"].apply(lambda x: "T" + x.split("T")[1])

            df = df.drop("updated", axis=1)

            dfs.append(df)
            
        except:
            break

    df_all = pd.concat(dfs).reset_index()
    df_all = df_all.drop("index", axis=1)

    file_name = appId + " Apple Store Reviews.xlsx"
    df_all.to_excel(file_name)

    return df_all

#run the function
user_search = input("Please Enter an App Id: ")
appleAPI(user_search)

#Spotify ID: 324684580
