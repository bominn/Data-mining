import requests
from bs4 import BeautifulSoup
import json
import csv

# global parameter
page_url_data = [] #save the url of home page (ex:page1-6)
rewiew_data = [] #save the url of every review from different page

def get_first_urlOfPage(soup):
    
    blinks = soup.select('.pageNumbers  a')
    for link in blinks:
        page_url_data.append(link['href'])
    page_url_data.pop()
    
def get_other_urlOfPage(page_num):
    
    count = 150
    N = 0
    while N!=page_num:
        print(count)
        count+=30
        N+=1
        str = '/Restaurants-g298564-oa%d-Kyoto_Kyoto_Prefecture_Kinki.html#EATERY_LIST_CONTENTS'%(count)
        page_url_data.append(str)
                             
def get_firstPage_review(soup):
    
    alinks = soup.select('.photo_booking  a')
    for link in alinks:
        rewiew_data.append(link['href'])
        
def get_otherPage_review():
    
    for i in range(len(page_url_data)):
        print("\n---------------------------------------")
        page_res = requests.get('https://www.tripadvisor.com'+page_url_data[i])
        page_soup = BeautifulSoup(page_res.text, "lxml")
        
        clinks = page_soup.select('.photo_booking  a')
        for link in clinks:
            rewiew_data.append(link['href'])
            
def get_review_information():
    
    
    with open('tripAdvisor_Kyoto_info_new.csv', 'w', newline='',encoding="utf-8") as csvfile:
        
        #fieldnames = ['Name','Total Rating','Phone Number', 'Review Count','Price Range','Address Region','Food', 'Service', 'Value','Atmosphere']
        fieldnames = ['Name','Total Rating', 'Review Count','Price Range','Address Region','Food', 'Service', 'Value','Atmosphere', 'Excellent','Very good','Average','Poor','Terrible']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        #len(rewiew_data)
        for i in range(0,len(rewiew_data)):
            res = requests.get('https://www.tripadvisor.com'+rewiew_data[i])
            soup = BeautifulSoup(res.text, "lxml")
            #print(soup)
            
            #dict = {'Name': '', 'Total Rating': '','Phone Number':'', 'Review Count': '','Price Range': '','Address Region': ''}
            dict = {'Name': '', 'Total Rating': '', 'Review Count': '','Price Range': '','Address Region': ''}
            
            data = json.loads(soup.find('script', type='application/ld+json').text)
            #print(data)
            print("#%d"%(i))
            print(data['name'])
            dict['Name'] = data['name'].encode(encoding="utf-8").decode("UTF-8", "ignore")
  
            if 'aggregateRating' in data:
                print(data['aggregateRating']['ratingValue'])
                print(data['aggregateRating']['reviewCount'])
                dict['Total Rating'] = data['aggregateRating']['ratingValue']
                dict['Review Count'] = data['aggregateRating']['reviewCount']
                
            if 'priceRange' in data:
                print(data['priceRange'])
                dict['Price Range'] = data['priceRange']
            
            print(data['address']['addressRegion'])
            dict['Address Region'] = data['address']['addressRegion']    
    
            for item in soup.select(".ratingRow"):
                category = item.select_one(".text").text
                rating = item.select_one(".row span")['alt'].split(" ")[0]
                print("{} : {}".format(category,rating))
                dict[category]=rating
            
            review_detail_label = []
            review_detail_text = []
    
            a = soup.find_all('span',{'class':'row_count row_cell'})
            for item in a:
                print(item.text)
                review_detail_text.append(item.text)
        
            b = soup.find_all('span',{'class':'row_label row_cell'})
            for item in b:
                print(item.text)
                review_detail_label.append(item.text)
        
            for i in range(len(review_detail_label)):
                dict[review_detail_label[i]] = review_detail_text[i]
            
            print(dict)
            writer.writerow(dict)
            print("-----------------------------")
            dict.clear()

if __name__ == '__main__':

    list_res = requests.get('https://www.tripadvisor.com/Restaurants-g298564-Kyoto_Kyoto_Prefecture_Kinki.html')
    list_soup = BeautifulSoup(list_res.text, "lxml")
    
    get_first_urlOfPage(list_soup)
    get_other_urlOfPage(100)
    print(page_url_data)
    
    
    get_firstPage_review(list_soup)
    
    get_otherPage_review()
    
    #print(rewiew_data)
    print("-----------------------------")
    for i in range(0,len(rewiew_data)):
        print(i,rewiew_data[i])
    print("-----------------------------")
    get_review_information()
    
