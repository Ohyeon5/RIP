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

all_fnames = ["American_Recovery_and_Reinvestment_Act_11094.json",
"Bipartisan_Budget_Act_of_2018_(H.R.1892)_12791.json",
"Clean_Air_Act_11405.json",
"Consolidated_Appropriations_Act,_2016_12897.json",
"Duncan_Hunter_National_Defense_Authorisation_Act_for_Fiscal_Year_2009_-_Energy_Provisions_11400.json",
"Electrify_Africa_Act_11043.json",
"Energy_Independence_and_Security_Act_of_2007_12857.json",
"Energy_Policy_Act_2005_(Energy_Bill)_11127.json",
"Environmental_Protection_Agency_40_CFR_Parts_9_and_84_12416.json",
"Executive_Order_13423:_Strengthening_Federal_Environmental,_Energy,_and_Transportation_Management_10.json",
"Executive_Order_13677:_Climate-Resilient_International_Development_11819.json",
"Executive_Order_14008_on_Tackling_the_Climate_Crisis_at_Home_and_Abroad_10342.json",
"Executive_Order_14017_on_America's_Supply_Chains_10518.json",
"Executive_Order_on_Catalyzing_Clean_Energy_Industries_and_Jobs_Through_Federal_Sustainability_12539.json",
"Executive_Order_on_Climate-Related_Financial_Risk_12272.json",
"Executive_Order_on_Protecting_Public_Health_and_the_Environment_and_Restoring_Science_to_Tackle_the_.json",
"Executive_Order_on_Strengthening_American_Leadership_in_Clean_Cars_and_Trucks_12269.json",
"Federal_Sustainability_Plan:_Catalyzing_America's_Clean_Energy_Industries_and_Jobs_12432.json",
"Federal_Sustainability_Plan_12397.json",
"Federal_water_pollution_control_act_(Clean_Water_Act)_10661.json",
"Final_Rule_-_Phasedown_of_Hydrofluorocarbons:_Establishing_the_Allowance_Allocation_and_Trading_Prog.json",
"Food,_Conservation,_and_Energy_Act_of_2008_(revised_2014)_-_Title_IX-Renewable_Energy_Provisions_116.json",
"Global_Change_Research_Act_of_1990_11873.json",
"H.R._133_(116th):_H.R._133:_Consolidated_Appropriations_Act,_2021_[Including_Coronavirus_Stimulus_&_.json",
"Hydrogen_Program_Plan_10421.json",
"Infrastructure_Investment_and_Jobs_Act_11136.json",
"Interior_Department_Suspends_Oil_and_Gas_Leases_in_Arctic_National_Wildlife_Refuge_12347.json",
"Revised_2023_and_Later_Model_Year_Light-Duty_Vehicle_Greenhouse_Gas_Emissions_Standards_12605.json",
"Stafford_Disaster_Relief_and_Emergency_Assistance_Act_12489.json",
"The_Biden-?Harris_Plan_to_Revitalize_American_Manufacturing_and_Secure_Critical_Supply_Chains_in_202.json",]


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
    data = []
    for fn in all_fnames:
        url = data_url+fn
        response = requests.get(url).content
        try:
            data.append(json.loads(response.decode("utf-8")))
        except:
            continue
    logging.info(f"There are {len(data)} json files in {data_url}")
    return data
    

def search_relevant_urls(keywords: List[str], n: int=3)-> Dict[str, str]:
    data = get_json_from_url(DATA_URL)
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