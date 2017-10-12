import json
from unidecode import unidecode
import re
from collections import Counter
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import os
import csv


### all regions of italy in english, italian, french, spanish, german, dutch
### cities all have same index
regions_it = ['Abruzzo', 'Basilicata', 'Calabria', 'Campania', 'Emilia-Romagna', 'Friuli-Venezia Giulia', 'Lazio', 'Liguria', 'Lombardia', 'Marche', 'Molise', 'Piemonte', 'Puglia', 'Sardegna', 'Sicilia', 'Toscana', 'Trentino-Alto Adige', 'Umbria', 'Valle d\'Aosta', 'Veneto']
regions_en = ['Abruzzo', 'Basilicata', 'Calabria', 'Campania', 'Emilia-Romagna', 'Friuli-Venezia Giulia', 'Lazio', 'Liguria', 'Lombardy', 'Marches', 'Molise', 'Piedmont', 'Apulia', 'Sardinia', 'Sicily', 'Tuscany', 'Trentino-South Tyrol', 'Umbria', 'Aosta Valley', 'Veneto']
regions_fr = ['Abruzzes', 'Basilicate', 'Calabre', 'Camapanie', 'Emilie-Romagne', 'Frioul-Venetie Julienne', 'Latium', 'Ligurie', 'Lomardie', 'Marches', 'Molise', 'Piemont', 'Pouilles', 'Sardaigne', 'Sicile', 'Toscane', 'Trentin-Haut-Adige', 'Ombrie', 'Vallee d\'Aoste', 'Venetie']
regions_es = ['Abruzos', 'Basilicata', 'Calabria', 'Campania', 'Emilia-Romana', 'Friuli-Venecia Julia', 'Lacio', 'Liguria', 'Lombardia', 'Marcas', 'Molise', 'Piamonte', 'Apulia', 'Cerdena', 'Sicilia', 'Toscana', 'Trentino-Alto Adigio', 'Umbria', 'Valle de Aosta', 'Veneto']
regions_de = ['Abruzzen', 'Basilikata', 'Kalabrien', 'Kampanien', 'Emilia Romagna', 'Friaul-Julisch-Venetien', 'Latium', 'Ligurien', 'Lombardei', 'Marken', 'Molise', 'Piemont', 'Apulien',  'Sardinien', 'Sizilien', 'Toskana', 'Trentino-Sudtirol', 'Umbrien', 'Aostatal', 'Venetien']
regions_nl = ['Abruzzen', 'Basilicata', 'Calabrie', 'Campania', 'Emilia-Romagna', 'Friuli-Venezia Giulia', 'Lazio', 'Ligurie', 'Lombardije', 'Marche', 'Molise', 'Piemont', 'Apulie', 'Sardinie', 'Sicilie', 'Toscane', 'Trentino-Zuid-Tirol', 'Umbrie', 'Valle d\'Aosta', 'Veneto']

OTHERS = [regions_en, regions_fr, regions_es, regions_de, regions_nl]
ALL_REGIONS = regions_it + regions_en + regions_fr + regions_es + regions_de + regions_nl



rootdir = '/Users/sashapaulovich/Desktop/cs/survey'
outputdir = os.path.join(rootdir, r'get_words')
fn = 'TwitterData_FINAL.json'
fname = os.path.join(rootdir,fn)

if not os.path.exists(outputdir):
    os.makedirs(outputdir)

with open(fname) as data:
    corpus = json.load(data)

    
    
### remove @, #, https, degree sign
def clean(text):
    tags = re.compile(r'([@]\S*|[#]\S*|\bhttps\S*)')
    clean = tags.sub('', text)
    clean.replace(u'\u00b0', '')
    return clean



### replaces non-italian translations of regions to italian translations
def change_region(loc):
    for i in range(len(OTHERS)):
        for j in range(len(OTHERS[i])):
            if loc == OTHERS[i][j]:
                loc = regions_it[j]
    return loc


### getting 50 most discriminating words for each region; output to csv file
def get_words(loc):
    
    savefile = os.path.join(outputdir, loc + '.csv')

    cities = []
    regions = []
    content = []

    ### all cities, regions, and content
    for tweet in corpus:
            place = tweet['placeFullName'].split(', ')

            ### ignores tweets with only country information
            ### ignores tweets from non-italian regions

            if (len(place) == 2) and (place[1] in ALL_REGIONS):

                region = change_region(unidecode(place[1]))

                if (region == loc):
                    text = clean(unidecode(tweet['content']))

                    ### only append tweet if it's unique
                    if text not in content:

                        ### unidecode removes non-words, replaces accents w ascii equivalents
                        cities.append(unidecode(place[0]))
                        regions.append(region)
                        content.append(text)

    ### separate 80/20 content train/test
    TRAIN = int(len(content)*0.8)
    TEST = len(content) - TRAIN
    X_train = content[:TRAIN]
    y_train = regions[:TRAIN]
    X_test = content[TRAIN:TEST]
    y_test = regions[TRAIN:TEST]
    
    
    # using pipeline
    steps = [
        ('vectorizer', TfidfVectorizer(analyzer='word',strip_accents='unicode', ngram_range=(1,2), max_features=5000, max_df=0.85)),
        ('classifier', MultinomialNB()),
    ]
    pipeline = Pipeline(steps)

    pipeline.fit(X_train, y_train)
    
    
    
    vec, clf = pipeline.named_steps['vectorizer'],pipeline.named_steps['classifier']
    coefs = pd.Series(clf.coef_[0], index=vec.get_feature_names())

    words = coefs[coefs.abs().sort_values(ascending=False).index][:50]
    print words
    
    words.to_csv(savefile)
    

    
    
for region in regions_it:
    get_words(region)



