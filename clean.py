import json
from unidecode import unidecode
import re


with open('/Users/sashapaulovich/Desktop/cs/survey/TwitterData_FINAL.json') as data:
	corpus = json.load(data)


### all regions of italy in english, italian, french, spanish, and german
### what's a better way to do this?
regions_en = ['Abruzzo', 'Aosta Valley', 'Apulia', 'Basilicata', 'Calabria', 'Campania', 'Emilia-Romagna', 'Friuli-Venezia Giulia', 'Lazio', 'Liguria', 'Lombardy', 'Marches', 'Molise', 'Piedmont', 'Sardinia', 'Sicily', 'Trentino-South Tyrol', 'Tuscany', 'Umbria', 'Veneto']
regions_it = ['Abruzzo', 'Basilicata', 'Calabria', 'Campania', 'Emilia-Romagna', 'Friuli-Venezia Giulia', 'Lazio', 'Liguria', 'Lombardia', 'Marche', 'Molise', 'Piemonte', 'Puglia', 'Sardegna', 'Sicilia', 'Toscana', 'Trentino-Alto Adige', 'Umbria', 'Valle d\'Aosta', 'Veneto']
regions_fr = ['Abruzzes', 'Vallee d\'Aoste', 'Basilicate', 'Calabre', 'Camapanie', 'Emilie-Romagne', 'Frioul-Venetie Julienne', 'Latium', 'Ligurie', 'Lomardie', 'Marches', 'Molise', 'Ombrie', 'Piemont', 'Pouilles', 'Sardaigne', 'Sicile', 'Toscane', 'Trentin-Haut-Adige', 'Venetie']
regions_es = ['Abruzos', 'Apulia', 'Basilicata', 'Calabria', 'Campania', 'Cerdena', 'Emilia-Romana', 'Friuli-Venecia Julia', 'Lacio', 'Lombardia', 'Marcas', 'Molise', 'Piamonte', 'Sicilia', 'Toscana', 'Trentino-Alto Adigio', 'Umbria', 'Valle de Aosta', 'Veneto']
regions_de = ['Abruzzen', 'Aostatal', 'Apulien', 'Basilikata', 'Emilia Romagna', 'Friaul-Julisch Venetien', 'Friaul-Julisch-Venetien','Kalabrien', 'Kampanien', 'Latium', 'Ligurien', 'Lombardei', 'Marken', 'Molise', 'Piemont', 'Sardinien', 'Sizilien', 'Toskana', 'Trentino-Sudtirol', 'Umbrien', 'Venetien']
all_regions = regions_en + regions_it + regions_fr + regions_es + regions_de
all_regions.append('Lombardije')
all_regions = sorted(list(set(all_regions)))

# print len(all_regions)
# for region in all_regions:
#     print region



def clean(text):
    tags = re.compile(r'([@]\S*|[#]\S*|\bhttps\S*)')
    return tags.sub('', text)


cities = []
regions = []
content = []

### all cities, regions, and content
for tweet in corpus:
        place = tweet['placeFullName'].split(', ')
        
        ### ignores tweets with no city (usually only country information is given)
        ### ignores tweets from non-italian regions
        
        if (len(place) == 2) and (place[1] in all_regions):
            
            ### unidecode removes non-words, replaces accents w ascii equivalents
            cities.append(unidecode(place[0]))
            regions.append(unidecode(place[1]))
            
            content.append(clean(unidecode(tweet['content'])))
                          

# print len(set(cities)) #4288
# print len(set(regions)) #55
# print len(content) #96340


### print sample
for i in range(50):
    print content[i]

