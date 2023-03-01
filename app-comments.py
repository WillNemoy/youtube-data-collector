
import pandas as pd
import openpyxl

import os
from dotenv import load_dotenv
import json
import datetime

load_dotenv() # look in the ".env" file for env vars

API_KEY = os.getenv("NY_API_KEY")
