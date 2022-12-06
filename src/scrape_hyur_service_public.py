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
    'tour price':[],
    'tour date':[],
    'tour picture':[]
    }

def generate_possible_links(k = 11):
    """
    possible links are
    """
    generated_links = [f'https://hyurservice.com/en/group-tours-armenia?page={i}' for i in range(1,k)]
    return generated_links

def get_info_for_link(link):
    result = requests.get(link)
    content = result.text
    soup = BeautifulSoup(content,features="html.parser")
    
    all_title_outers = soup.find_all('div',attrs={'class':'tours__item-title-outer'})
    all_titles = [title_outer.find('a',).text for title_outer in all_title_outers]

    all_desc_outers = soup.find_all('div',attrs={'class':'tours__item-desc-out'})
    all_descriptions = [desc_outer.find('a',).text for desc_outer in all_desc_outers]

    regex = re.compile('tours__time-info*')
    all_duration_outers = soup.find_all('p',{'class':regex})
    all_durations = [duration.find_all('span')[0].text for duration in all_duration_outers][::2]

    regex = re.compile('tours__main-price*')
    all_price_outers = soup.find_all('p',{'class':regex})
    all_prices = [price['data-price']+' AMD' for price in all_price_outers]

    regex = re.compile('tours__right-title*')
    all_date_outers = soup.find_all('p',{'class':regex})
    all_dates = [date.text for date in all_date_outers]

    regex = re.compile('tours__left*')
    all_image_outers = soup.find_all('div',{'class':regex})
    all_image_tags = [outer.find('img') for outer in all_image_outers]
    all_images = ['https://hyurservice.com'+image['src'] for image in all_image_tags]

    assert len(all_dates)==len(all_images)==len(all_durations)==len(all_prices)==len(all_titles)==len(all_descriptions)

    scraped_dict = {
    'tour title':all_titles,
    'tour description':all_descriptions,
    'tour duration':all_durations,
    'tour price':all_prices,
    'tour date':all_dates,
    'tour picture':all_images
    }
    return scraped_dict

def merge_dicts(dicts,total_data = total_data):
    for key in total_data.keys():
        for dictionary in dicts:
            total_data[key].extend(dictionary[key])
    
    return total_data

if __name__=='__main__':
    possible_links=generate_possible_links(k=7)
    scraped_data = [get_info_for_link(link) for link in possible_links]
    total_data = merge_dicts(scraped_data)
    df = pd.DataFrame.from_dict(total_data)
    df.to_csv('./hyurservice_public.csv',index = False)
