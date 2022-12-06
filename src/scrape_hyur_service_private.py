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
    'tour category':[],
    'tour picture':[]
    }

def generate_possible_links(k = 10):
    """
    possible links are
    """
    generated_links = [f'https://hyurservice.com/en/private-tours-armenia?f%5Bprivate_tours_name%5D=0&f%5Bsorting%5D=&page={i}' for i in range(1,k)]
    return generated_links

def get_info_for_link(link):
    result = requests.get(link)
    content = result.text
    soup = BeautifulSoup(content,features="html.parser")
    all_title_outers = soup.find_all('div',attrs={'class':'tours__item-title-outer'})
    all_titles = [title_outer.find('a',).text for title_outer in all_title_outers]
    all_desc_outers = soup.find_all('div',attrs={'class':'tours__item-desc-out'})
    all_descriptions = [desc_outer.find('a',).text for desc_outer in all_desc_outers]

    regex = re.compile('tours__time*')
    all_duration_outers = soup.find_all('p',{'class':regex})
    all_durations = [duration.find('span').text for duration in all_duration_outers]

    regex = re.compile('tours__main-price*')
    all_price_outers = soup.find_all('p',{'class':regex})
    all_prices = [price['data-price']+' AMD' for price in all_price_outers]

    regex = re.compile('list__category-type*')
    all_category_outers = soup.find_all('div',{'class':regex})
    all_categories = [category.text for category in all_category_outers]

    regex = re.compile('list__thumb-img*')
    all_image_outers = soup.find_all('img',{'class':regex})
    all_images = ['https://hyurservice.com'+image['src'] for image in all_image_outers]

    assert len(all_categories)==len(all_images)==len(all_durations)==len(all_prices)==len(all_titles)==len(all_descriptions)

    scraped_dict = {
    'tour title':all_titles,
    'tour description':all_descriptions,
    'tour duration':all_durations,
    'tour price':all_prices,
    'tour category':all_categories,
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
    df.to_csv('./hyurservice_private.csv',index = False)
