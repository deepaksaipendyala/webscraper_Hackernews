import requests
from bs4 import BeautifulSoup
# import pprint
import csv

fields = ['link', 'title', 'votes'] 
filename = "data.csv"

hn = []


def create_custom_hn(hn):
    p = 2  #p no of pages
    for i in range(p):
        res = requests.get(f'https://news.ycombinator.com/news?p={i+1}')
        # print(res.text)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.titlelink')
        subtext = soup.select('.subtext')
        # print(soup)
        # print(links)
        for idx, item in enumerate(links):
            title = item.getText()
            href = item.get('href', None)
            vote = subtext[idx].select('.score')
            if len(vote):
                points = int(vote[0].getText().replace(' points', ''))
                if points > 99:
                    hn.append({'title': title, 'link': href, 'votes': points})
    # print(hn)
    return hn


hn = create_custom_hn(hn)


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


st = sort_stories_by_votes(hn)
# print(st)
# pprint.pprint(st)
# print("done")
title=[]
link=[]
for i in st:
  title.append(i['title'])
  print("Title:",i['title'])
  link.append(i['link'])
  print("Link:",i['link'])


with open(filename, 'w') as csvfile: 
    # creating a csv dict writer object 
    writer = csv.DictWriter(csvfile, fieldnames = fields) 
        
    # writing headers (field names) 
    writer.writeheader() 
        
    # writing data rows 
    writer.writerows(st) 

    print("Data is stored in data.csv file")