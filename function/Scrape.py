#Never run this program this only for documentation
from google_play_scraper import Sort, reviews_all
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from function.ReadSave import ReadSave

languages = ['en', 'id']
# List of languages to scrape reviews for
names = [
    'com.jiwa.jiwagroup',
    'com.tomoro.indonesia.android',
    'coffee.fore2.fore',
    'com.jagocoffee.app',
    'com.starbucks.id'
]

'''
names:
Names is a list of url that support google_play_scraper
code is exist in every last word in url in playstore
languages:
is list of code for google play scraper
'''

def scraper(names=names, language=languages ):
    rd =ReadSave()
    if not isinstance(names, list):
        names = [names]
    if not isinstance(language, list):
        language = [language]
    
    final_reviews = []
    for name in names:
        all_reviews = []
        for lang in languages:
            try:
                print(f"Scraping reviews in language: {lang.upper()} for app: {name}")  
                reviews = reviews_all(
                    name,
                    sleep_milliseconds=0,  
                    lang=lang,  
                    country='id',  
                    sort=Sort.NEWEST, 
                )
                all_reviews.extend(reviews)

            except Exception as e:
                print(f"Error for app {name} in language {lang}, please check apk names")

        # Print the total number of reviews collected for this app
        print(f"Total reviews collected for {name}: {len(all_reviews)}")
        
        if all_reviews:
            df = pd.DataFrame(all_reviews)
            df = df[['userName','score','content','at']]
            df.columns = ['nama', 'skor', 'ulasan','waktu']
            df = df.dropna(subset='ulasan')
            rd.save_data(df,f'{name}.csv')
            final_reviews.append(df)
        else:
            print(f"No reviews try change apk name {name}")
    return pd.concat(final_reviews, ignore_index=True)

