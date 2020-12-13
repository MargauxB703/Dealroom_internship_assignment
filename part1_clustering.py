import pandas as pd
pd.set_option('display.max_columns', 25)
pd.set_option('display.max_colwidth', None)
import re
from keywords_extractor import *
from nltk.corpus import wordnet
from openpyxl import load_workbook
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger') #Keyword extractor
    
data = pd.read_excel (r'Data_Science_Internship_Assignment.xlsx', sheet_name='Data')
data = data[["TAGLINE", "TAGS", "LAUNCH DATE", "TYPE"]]

#---------------------------Get keywords from TAGLINE-------------------------
def convert_tagline_to_string(row):
    return(str(row))
data["TAGLINE_STRING"] = data["TAGLINE"].apply(convert_tagline_to_string)

data = data_treatment_pandas(data, "TAGLINE_STRING")
data = data.drop(["TAGLINE", "TAGLINE_STRING"], axis=1)

#------------------------------------Clean TAGS-------------------------------
def treatment_tags(row):
    new_list = str(row).split(";")
    if new_list != ['nan']:
        new_list = split_dash(new_list)
        new_list = remove_stopwords(new_list)
        new_list = lemmatize_text(new_list)
        new_list = remove_duplicate(new_list)
    return(new_list)

data["KEYWORDS_TAGS"] = data["TAGS"].apply(treatment_tags)
del data["TAGS"]

#------------------------Find words to describe entities----------------------
Startups = ["startup", "company", "innovation", "technology", "science"]
Mature = ["mature", "company", "multinational", "established", "sustainable"]
University = ["university", "primary", "secondary", "education", "school", "student"]
Government = ["government", "non-profit", "organisation", "governmental", "charitable", "philanthropic"]
all_entities = [Startups, Mature, University, Government]

def get_synonyms(all_entities):
    all_synonyms = []
    for i in range(len(all_entities)):
        synonyms = []
        for word in all_entities[i]:
            for syn in wordnet.synsets(word):
            	for l in syn.lemmas():
                    if l.name().lower() not in synonyms :
                        synonyms.append(l.name().lower())
        all_synonyms.append(synonyms)
    return(all_synonyms)

keywords_entities = get_synonyms(all_entities)

def treatment_keywords_entities(keywords_entities):
    new_keywords_entities = []
    for i in range(len(keywords_entities)):
        new_list = split_dash(keywords_entities[i])
        new_list = remove_stopwords(new_list)
        new_list = lemmatize_text(new_list)
        new_list = remove_duplicate(new_list)
        new_keywords_entities.append(new_list)
    return(new_keywords_entities)

new_keywords_entities = treatment_keywords_entities(keywords_entities)
#Add some extra words
to_startup = ["ai", "machine", "learning", "network"]
for word in to_startup:
    new_keywords_entities[0].append(word)
    
#----------------------------------Get max overlap----------------------------
data["ALL_KEYWORDS"] = data["KEYWORDS_TAGS"] + data["KEYWORDS_TAGLINE"]

def get_max_overlap(row, new_keywords_entities):
    all_overlaps = []
    for i in range(len(new_keywords_entities)):
        count = 0
        for word in row:
            if word in new_keywords_entities[i]:
                count += 1
        all_overlaps.append(count)
    indexs_max = [i for i, j in enumerate(all_overlaps) if j == max(all_overlaps)]
    return(indexs_max[0])

data['MAX_OVERLAP'] = data.apply(lambda x: get_max_overlap(x["ALL_KEYWORDS"], new_keywords_entities), axis=1)
data = data.drop(["ALL_KEYWORDS", "KEYWORDS_TAGS", "KEYWORDS_TAGLINE"], axis=1)

#---------------------------Data Management-----------------------------------
#Clean LAUNCH DATE
def clean_date(row):
    year = int(re.sub('\D', '', str(row)))
    dummy = 0
    if year < 1990 :
        dummy = 1
    return(dummy)

data["YEAR_DUMMY"] = data["LAUNCH DATE"].apply(clean_date)
del data["LAUNCH DATE"]

before_1990 = data[data["YEAR_DUMMY"]== 1]
after_1990 = data[data["YEAR_DUMMY"]== 0]
#before_1990.apply(pd.Series.value_counts)
#after_1990.apply(pd.Series.value_counts)

#---------------------------------Result--------------------------------------
def get_type(row_max_overlap, row_year):
    row_type = row_max_overlap
    if row_year == 0 and row_max_overlap == 1: #after 1990
        row_type = 0
    if row_year == 1 and row_max_overlap == 0: #before 1990
        row_type = 1
    
    if row_type == 0:
        row_type = "Startup"
    if row_type == 1:
        row_type = "Mature company"
    if row_type == 2:
        row_type = "University/School"
    if row_type == 3:
        row_type = "Government/Non-profit"
    return(row_type)

data["TYPE"] = data.apply(lambda x: get_type(x["MAX_OVERLAP"], x["YEAR_DUMMY"]), axis=1)
#data.head()
#data["TYPE"].value_counts()

#-----------------------------Export result to Excel--------------------------
export_data = data[["TYPE"]]
book = load_workbook(r'Data_Science_Internship_Assignment_Answer.xlsx')
writer = pd.ExcelWriter(r'Data_Science_Internship_Assignment_Answer.xlsx', engine='openpyxl') 
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
export_data.to_excel(writer, "Data", startcol = 10, index = False)
writer.save()
