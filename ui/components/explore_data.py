import os
import json
import logging
import requests
import io
from urllib.parse import quote
from typing import List, Dict
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

DATA_PATH = "C:\\Users\\ohyeo\\OneDrive\\rip\\open-data-main\\data\\USA\\"
DATA_URL = "https://raw.githubusercontent.com/climatepolicyradar/open-data/main/data/USA/"


def argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)

def val_in_list(val, list_val):
    return any([val in v for v in list_val])

def get_json_from_path(data_path=DATA_PATH):
    data = []
    for fn in os.listdir(data_path):
        if '.json' in fn:
            fname = os.path.join(data_path, fn) 
            with open(fname, 'r', encoding="utf8") as f:
                data.append(json.load(f))
    logging.info(f"There are {len(data)} json files in {data_path}")
    return data

def get_json_from_url(data_url = DATA_URL):
    download = requests.get(data_url).content
    print(download)


def search_relevant_urls(keywords: List[str], n: int=3)-> Dict[str, str]:
    data = get_json_from_path(DATA_PATH)
    dump_all_idx = []
    for k in keywords:
        dump_all_idx.extend([idx for idx, d in enumerate(data) if val_in_list(k.strip().lower(), list(map(str.lower, d["document_keyword"])))])
    unique = list(set(dump_all_idx))
    counts = [dump_all_idx.count(idx) for idx in unique]
    unique = [unique[idx] for idx in argsort(counts)]
    fin_idx = unique[:min(n, len(unique))]
    data = [data[idx] for idx in fin_idx]

    return {title: url.replace(" ", "%20") for title, url in [[d["document_name"], d["document_url"]] for d in data]}

if __name__=="__main__":
    get_json_from_url()