# This is a project for english & id fr 
import pandas as pd
import os
import re
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dictionary.__init__ import *


class ReadSave:
    def __init__ (self, Dataset='dataset', Rs_GT='gt', Final_GT='prep_gt', Rs_Pyabsa='rs_pyabsa', Rs_Group='rs_group', Rs_Pict='rs_pict'):
        self.Dataset=Dataset
        self.Rs_GT=Rs_GT
        self.Final_GT=Final_GT
        self.Rs_Pyabsa=Rs_Pyabsa
        self.Rs_Group=Rs_Group
        self.Rs_Pict = Rs_Pict

        #creating dir if dont exist
        os.makedirs(self.Dataset, exist_ok=True)
        os.makedirs(self.Rs_GT, exist_ok=True)
        os.makedirs(self.Final_GT, exist_ok=True)
        os.makedirs(self.Rs_Pyabsa, exist_ok=True)
        os.makedirs(self.Rs_Group, exist_ok=True)
        os.makedirs(self.Rs_Pict, exist_ok=True)
    
    def _path (self,name_dir, name_file):
        path = os.getcwd()
        path = os.path.join(path,name_dir,name_file)
        return path
    
    def read_dataset(self,name_file):
        data = pd.read_csv(self._path(self.Dataset,name_file),index_col=False)
        return data
    
    def read_gt(self,name_file):
        data = pd.read_excel(self._path(self.Rs_GT,name_file),index_col=False)
        return data   
    
    def read_prep(self,name_file):
        data = pd.read_excel(self._path(self.Final_GT,name_file),index_col=False)
        return data
    def read_pyabsa(self,name_file):
        data = pd.read_csv(self._path(self.Rs_Pyabsa,name_file),index_col=False)
        return data
    
    def save_data(self,data,name_file):
        data.to_csv(self._path(self.Dataset,name_file),index=False)

    def save_gt(self,data,name_file):
        data.to_csv(self._path(self.Rs_GT,name_file),index=False)

    def save_prep(self,data,name_file):
        data.to_excel(self._path(self.Final_GT,name_file),index=False)
    
    def save_pyabsa(self,data,name_file):
        data.to_csv(self._path(self.Rs_Pyabsa,name_file),index=False)
    
    def save_group(self,data,name_file):
        data.to_csv(self._path(self.Rs_Group,name_file),index=False)
    
    #def save_pict(self,data,name_file):
        #data.to_csv(self._path(self.Rs_Pict,name_file),index=False)

class Cleaning(ReadSave):
    def __init__(self, column='ulasan',trans_column='review'):
        super().__init__()
        self.column=column
        self.trans_column=trans_column

    def first_clean(self,sentence):
        #sentence = unicodedata.normalize("NFKD", sentence)
        sentence = str(sentence)  
        sentence = re.sub(r"\s+", " ", sentence)  # Remove multiple spaces
        sentence = re.sub(r"\.{2,}", " ", sentence)  # Remove ellipsis (e.g., ...)
        sentence = re.sub(r"(?<=\w)-(?=\w)", " ", sentence)  # Replace hyphens between words
        sentence = re.sub(r"\d+", "", sentence)  # Remove numbers
        sentence = re.sub(r"[^\w\s.,']", "", sentence)  # Remove punctuation
        sentence = sentence.strip()
        # doc = nlp(sentence)
        # Remove leading/trailing whitespace
        # Tokenize and process
        filtered_words = [word for word in sentence.split() if len(word) > 1]
        # Check for single-token comments
        if len(filtered_words) <= 1:
            return None  # Return empty string for single-token comments
        
        return " ".join(filtered_words)
    
    def clean_column(self, data):
        data[self.column] = data[self.column].apply(self.first_clean)
        data = data.dropna(subset=[self.column])
        return data
            
    def change_merk (self,data,dictionary={}):    
        data[self.column] = data[self.column].str.lower()
        data[self.column] = data[self.column].replace(dictionary, regex=True)
        return data
    
    def droping_merk (self,data, list_word=[]):
        if list_word:
            pattern = '|'.join(re.escape(word) for word in list_word)  # Escapes special characters
            data = data[~data[self.column].str.contains(pattern, flags=re.IGNORECASE, na=False)]
        return data
    
    def apply_change (self,data_scrape, name_file, dictionary={}, list_word=[]):
        data = self.read_dataset(data_scrape)
        data = self.clean_column(data)              #preprocess
        data = self.change_merk(data,dictionary)    #handling merk name accoding to dictionary
        data = self.droping_merk(data, list_word)   #handling list_word that wnat to be drop
        self.save_prep(data, name_file)
        return data
    
class CountAspect(Cleaning):
    def __init__(self, trans_column='review'):
        super().__init__(trans_column)
        import spacy
        self.nlp = spacy.load('en_core_web_sm')
    
    def cleaning_sign(self,data):
        cleaned = re.sub(r"[\[\]'\"]", '', str(data))
        cleaned = cleaned.lower()
        return cleaned.strip()
    
    def replace_nan (self,data):
        if data=='':
            return np.nan
        else: 
            return data
        
    def apply_cleaning(self,data, list_drop=list_merk):
        data['sentiment']=data['sentiment'].apply(self.cleaning_sign)
        data['sentiment']=data['sentiment'].apply(self.replace_nan)
        data['aspect']=data['aspect'].apply(self.cleaning_sign)
        data['aspect']=data['aspect'].apply(self.replace_nan)
        data = data[~data['aspect'].isin(list_drop)]
        return data.dropna(subset='aspect')   

    def replace(self,text, dictionary=synonim_word_map):
        text = str(text).lower()
        for key, value in dictionary.items():
            if key in text:
                return value
        return text

    def  nlp_lema(self,data):
        data = self.nlp(data)
        return data

    def apply_replace(self,data,dictionary=synonim_word_map):
        
        data['aspect'] =  data['aspect'].apply(self.nlp_lema)
        data['aspect']=data['aspect'].apply(lambda x: self.replace(x, dictionary))
        data = data.dropna(subset='aspect')
        return data


    def reverse(self,data):
        pairs = []
        for i, row in data.iterrows():
            aspect=[a.strip() for a in row['aspect'].split(',')]
            sentiment=[b.strip() for b in row['sentiment'].split(',')]
            min_length = min(len(aspect), len(sentiment))
            for k,v in zip(aspect[:min_length],sentiment[:min_length]):
                pairs.append({'aspect':k,'sentiment':v})
        data = pd.DataFrame(pairs)
        data = data.reset_index()
        return data.dropna(subset='aspect')

    def apply_reverse(self,data):
        data = self.reverse(data)
        data = data.groupby(['aspect','sentiment']).size().unstack(fill_value=0)
        sentiment_order = ['positive', 'neutral', 'negative']
        data = data.reindex(columns=sentiment_order, fill_value=0)
        data = data.reset_index()
        data['total_count'] = data['positive'] + data['neutral'] + data['negative']
        data['pos_perc'] = (data['positive']/data['total_count'])*100
        data['pos_perc'] =data['pos_perc'].round(2)
        data['neg_perc'] = (data['negative']/data['total_count'])*100
        data['neg_perc'] =data['neg_perc'].round(2)
        data['tot_perc'] = (data['total_count']/data['total_count'].sum())*100
        data['tot_perc'] =data['tot_perc'].round(2)
        return data
    
    def apply_group(self,data, file_group_name):
        data = self.apply_cleaning(data)
        data = self.apply_replace(data)
        data = self.apply_reverse(data)
        data = data.sort_values('total_count', ascending=False)
        self.save_group(data, file_group_name)
        return data
        

class VisulGroup(ReadSave):    
       
    def visul(self,data, nama, sorted):
        import seaborn as sns
        import matplotlib.pyplot as plt
        
        data = data.head(30) # 40 aspect 
        plt.figure(figsize=(10,5))
        ax = sns.barplot(data=data,x=sorted, y='aspect',
                    color='blue',)
        for i in ax.containers:
            ax.bar_label(i, fmt='%d', padding=3)
        
        plt.title(nama, fontdict={'size':15})
        plt.xlabel('Total')
        plt.ylabel('Aspect')
        image_path = self._path(self.Rs_Pict, f'{nama}.png')
        plt.savefig(image_path, bbox_inches='tight')
        plt.show()

    def apply_visul(self,data):
        datas_count = data.sort_values('total_count',ascending=False)
        datas = datas_count.head(20)
        self.visul(datas, 'Top 20 Aspect by Total Count','total_count')
        data = data.sort_values('positive', ascending=False)
        datas = data.head(20)
        self.visul(datas, 'Top 20 Aspect by Positive','positive')
        data = datas.sort_values('negative', ascending=False)
        datas = data.head(20)
        self.visul(datas, 'Top 20 Aspect by Negative','negative')
        data = data.sort_values('pos_perc', ascending=False)
        datas = data.head(20)
        self.visul(datas, 'Top 20 Aspect by Pos_Perct','pos_perc')
        data = data.sort_values('neg_perc',ascending=False)
        datas =data.head(20)
        self.visul(datas, 'Top 20 Aspect by Neg_Perct','neg_perc')       
        return datas_count
    
    def category(self, aspect, group_dict=group_dict):
        for category, keywords in group_dict.items():
            if aspect in keywords:
                return category
        return None
    
    def apply_category(self,data,aspect, group_dict=group_dict):
        data['category'] = data['aspect'].apply(lambda x: self.category(x, group_dict))
        self.save_group(data,'grouping_result.csv')
        return data
     
def wrapper_apply_all(prepdata_xlsx, data_gt_xlsx,name_data_absa,name_data_group):
    from function.Absa import My_Absa
    cl = Cleaning()
    ma = My_Absa()
    ca = CountAspect()
    vg = VisulGroup()
    data = ma.process_absa(prepdata_xlsx, data_gt_xlsx,name_data_absa)
    data = ca.apply_group(data,name_data_group)
    print(data.head(5))
    data = vg.apply_visul(data)
    return data
