"""
File for scraping hyurservice.com
"""
from bs4 import BeautifulSoup
import requests
import regex as re
import pandas as pd

total_data = {
    'tour title':[],
    'tour description':[],
    'tour duration':[],
    'tour date':[],
    'tour picture':[]
    }

subgroups = ['hiking-trekking','jeep','horseback-riding','cycling']
possible_links = ['https://wildarmenia.com/armenia-tours/'+gr for gr in subgroups]

scraped_data = []
for index,link in enumerate(possible_links):
    sample = link
    result = requests.get(sample)
    content = result.text
    soup = BeautifulSoup(content, "html.parser")
    
    all_title_outers = soup.find_all('h4',{'class':'evc-iwt-title'})
    all_titles = [title_outer.text.replace('\n','').replace('\t','') for title_outer in all_title_outers]
    
    all_desc_outers = soup.find_all('p',attrs={'class':'evc-iwt-text'})
    all_descriptions = [desc_outer.text for desc_outer in all_desc_outers]
    
    if index in [1,2,3]:
        all_descriptions = [None for i in all_titles]
    
    all_duration_outers = soup.find_all('span',{'class':'evc-ili-text'})
    all_durations = [duration.text for duration in all_duration_outers][1::4]
    
    regex = re.compile('evc-iwt-image*')
    all_image_outers = soup.find_all('div',{'class':regex})
    if index==1 or index==3:
        all_images = [outer.find('img')['src'] for outer in all_image_outers]
    else:
        all_images = [outer.find('a').find('img')['src'] for outer in all_image_outers]
    
    all_dates = [date.text for date in all_duration_outers][0::4]
    
    assert len(all_dates)==len(all_images)==len(all_durations)==len(all_titles)==len(all_descriptions)
    
    data = {
    'tour title':all_titles,
    'tour description':all_descriptions,
    'tour duration':all_durations,
    'tour date':all_dates,
    'tour picture':all_images
    }
    scraped_data.append(data)

def merge_dicts(dicts,total_data = total_data):
    for key in total_data.keys():
        for dictionary in dicts:
            total_data[key].extend(dictionary[key])
    
    return total_data

if __name__=='__main__':

    total_data = merge_dicts(scraped_data)
    df = pd.DataFrame.from_dict(total_data)
    df.to_csv('./wild_armenia.csv',index = False)
