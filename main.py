import requests
from bs4 import BeautifulSoup
import pprint


hn = []
p=2 #p no of pages
for i in range(p):
  res = requests.get(f'https://news.ycombinator.com/news?p={i+1}')
  soup = BeautifulSoup(res.text, 'html.parser')

  links = soup.select('.storylink')
  subtext = soup.select('.subtext')

  def create_custom_hn(links, subtext):
    for idx, item in enumerate(links):
      title = item.getText()
      href = item.get('href', None)
      vote = subtext[idx].select('.score')
      if len(vote):
        points = int(vote[0].getText().replace(' points', ''))
        if points > 99:
          hn.append({'title': title, 'link': href, 'votes': points})
    return hn
  create_custom_hn(links, subtext)

def sort_stories_by_votes(hnlist):
  return sorted(hnlist, key= lambda k:k['votes'], reverse=True)    
 
pprint.pprint(sort_stories_by_votes(hn))