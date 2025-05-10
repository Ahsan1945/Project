# Google Play Review Sentiment Analyzer
This project builds a complete pipeline to collect, clean, analyze, and visualize customer sentiment and aspect-based opinions from Google Play reviews in English and Indonesian.



## 🧠 What It Does
'''
✅ Scrapes app reviews from Google Play using google_play_scraper
✅ Cleans and normalizes multilingual review text
✅ Applies aspect-based sentiment analysis (ABSA) using PyABSA
✅ Groups aspects and sentiments to reveal key themes and trends
✅ Visualizes top aspects using seaborn
'''

## 📁 Project Structure

```
.
├── function/
│   ├── Absa.py           # Aspect-based sentiment pipeline
│   └── ReadSave.py       # Class for reading/saving data
├── dictionary/
│   └── __init__.py       # Contains word maps and groupings
├── main_script.py        # Wrapper function and runner
├── dataset/              # Raw scraped CSVs
├── gt/                   # Google Translate
├── prep_gt/              # Cleaned & processed reviews
├── rs_pyabsa/            # ABSA results (CSV)
├── rs_group/             # Grouped aspect result (CSV)
├── rs_pict/              # Visual data (Seaborn saves)
└── README.md
```



## 🚀 How to Run
'''
1. Install dependencies
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm

1. Run the scraper function with 
    names = list of application code
    lenguage = language data that use

2. Run apply_change(
    data_scrape = 'result_sraper_.csv' in dataset,
    dictionary  = dictionary: normalize word/brand
    name_file   = 'name_file_.xlsx' save in prep gt
    list_word   = list word that want to drop
    )

3. Translate the doc using thirdparty tools, 
    (Unfortunately, the integration for translation tools is not implemented). Plese save it in
    gt folder

4. Run Wrapper function with
    wrapper_apply_all(
    dataset_xlsx='your_cleaned_data.xlsx',
    data_gt_xlsx='your_ground_truth.xlsx',
    name_data_absa='result_absa.csv',
    name_data_group='result_grouped.csv'
    )
'''

## 🎯 Use Case
This project helps businesses:
- Monitor app feedback in two languages
- Understand what users like/dislike (features, UI, service)
- Prioritize fixes or features based on real sentiment data


Scraper model are based on 
- https://github.com/JoMingyu/google-play-scraper

PyAbsa model
- https://github.com/yangheng95/PyABSA
