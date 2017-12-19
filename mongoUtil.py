import pandas as pd
import numpy as np
from datetime import datetime
from pymongo import MongoClient
from dateutil.relativedelta import relativedelta
import csv
import time
import sys

class mongoUtil:
    def __init__(self):
        print("Initialized.")

    def get_client(self):
        return MongoClient('localhost', 27017)

    def get_cif_info(self,cif_id):
        client = self.get_client()
        db = client.npsdb
        collection = db['NPS']
        return collection.find({"_id":cif_id})


