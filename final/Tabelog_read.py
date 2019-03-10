import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# global parameter
page_url_data = [] #save the url of home page (ex:page1-6)
rewiew_data = [] #save the url of every review from different page

def get_first_urlOfPage(soup):
    
    blinks = soup.select('#js-map-search-result-nav  a')
    #print(blinks)
    for link in blinks:
        #print(link['href'])
        page_url_data.append("https://tabelog.com"+link['href'])

def get_urlOfPage(page_num):
    
    for i in range(2,page_num+1):
        str = "https://tabelog.com/en/tokyo/rstLst/"+"%d"%(i)+"/?SrtT=rt"
        page_url_data.append(str)

def get_firstPage_reviewURL(soup):
    
    alinks = soup.select('#js-map-search-result-list  a')
    count = 0
    for link in alinks:
        if count%3 == 0:
            #print(link['href'])
            rewiew_data.append(link['href'])
        count+=1

def get_review_information():
    
    with open('tabelog_tokyo_info.csv', 'w', newline='',encoding="utf-8") as csvfile:
        
        fieldnames = ['JapneseName','EnglishName', 'TotalRating', 'NearstStation','FoodCategory','LunchRating', 'DinnerRating', 'ReviewCounts', 'Dishes', 'Service', 'Atmosphere', 'Cost performance','Drink']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        dict = {'JapneseName':'','EnglishName':'', 'TotalRating':'', 'NearstStation':'','FoodCategory':'','LunchRating':'', 'DinnerRating':'', 'ReviewCounts':''}
        
        for i in range(0,len(rewiew_data)):
    
            res = requests.get(rewiew_data[i])
            soup = BeautifulSoup(res.text, "lxml")
        
            print("#%d"%(i))
    
            # get name
            link_japan_name = soup.select('.rd-header__rst-name-ja')
            dict['JapneseName'] =  link_japan_name[0].text[1:len(link_japan_name[0].text)-1]
            print(link_japan_name[0].text[1:len(link_japan_name[0].text)-1])
            
            link_english_name = soup.select('.rd-header__rst-name-main')
            dict['EnglishName'] =  link_english_name[0].text
            print(link_english_name[0].text)
    
            # get total rating
            link_rate = soup.select('.rd-header__rst-rate')
            rating_str = link_rate[0].text[1:5]
            dict['TotalRating'] = rating_str.strip()
            print(rating_str.strip())
    
            #get basic info - nearst station, food category , phone-number
            #nearst station
            basic_info = soup.find_all('div',{'class':'rd-header__info-table'})
            station_str = basic_info[0].find_all('dd')[0].text[10:35]
            dict['NearstStation'] = station_str.strip() 
            print(station_str.strip())
            
            #food category
            category_div_tag = basic_info[0].find_all('div',{'class':'rd-header__linktree'})
            category_p_tag = category_div_tag[1].find_all('p',{'class':'rd-header__linktree-parent'})
            category = category_p_tag[0].find_all('span')
            dict['FoodCategory'] = category[0].text
            print(category[0].text)
            
            '''
            #phone-number
            tel_num = basic_info[0].find_all('dd')[2].text
            tel_str = tel_num[50:70].strip()
            tel_str = tel_str.lstrip('(').rstrip(')')
            dict['PhoneNumber'] = str(tel_str)
            print(tel_str)
            '''
            
            # get launch & dinner rating
            c_rating = soup.find_all('li',{'class':'c-rating c-rating--lg'})
            dict['LunchRating'] = c_rating[0].find_all('b')[0].text
            print(c_rating[0].find_all('b')[0].text)
            
            dict['DinnerRating'] = c_rating[1].find_all('b')[0].text
            print(c_rating[1].find_all('b')[0].text)
    
            # get review counts
            review_num = soup.find_all('a',{'class':'rd-header__rst-reviews-target gly-b-review'})
            dict['ReviewCounts'] = review_num[0].find_all('b')[0].text
            print(review_num[0].find_all('b')[0].text)
  
            info = soup.find_all('dl', {'id': 'js-rating-detail', 'class': 'rd-header__rating-detail'})
            comp_info = pd.DataFrame()
            cleaned_id_text = []
            for i in info[0].find_all('dt'):
                cleaned_id_text.append(i.text.strip())
            cleaned_id__attrb_text = []
            for i in info[0].find_all('dd'):
                cleaned_id__attrb_text.append(i.text)
            

            comp_info['Id'] = cleaned_id_text
            comp_info['point'] = cleaned_id__attrb_text
            print(comp_info)
            
            for i in range(0,5):
                dict[cleaned_id_text[i]] = cleaned_id__attrb_text[i]
            
            print(dict)
            print('-------------------------------------------')
            writer.writerow(dict)
            dict.clear()
if __name__ == '__main__':
    
    page_1 = 'https://tabelog.com/en/tokyo/rstLst/1/?SrtT=rt'
    page_url_data.append(page_1)
    get_urlOfPage(60)
    
    for i in range(0,len(page_url_data)):
        
        res = requests.get(page_url_data[i])
        f_soup = BeautifulSoup(res.text, "lxml")
    
        get_firstPage_reviewURL(f_soup)
        
    for i in range(0,len(rewiew_data)):
        print("#%d"%(i),rewiew_data[i])
    print('-------------------------------------------')          
    get_review_information()
    
