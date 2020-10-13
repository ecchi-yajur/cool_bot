from bs4 import BeautifulSoup
import requests
#anime = "bleach"
def anime_desc(anime):
	URL = "https://myanimelist.net/search/all?q="+anime+"&cat=all"
	r = requests.get(URL) 
	#print(r.content) 
	soup = BeautifulSoup(r.content, 'html.parser')
	#print(soup.prettify())
	table = soup.find('article')  
	#print(table)
	urlval = []
	for row in table.findAll('div',attrs = {'class':'picSurround di-tc thumb'}):
		urlval.append(row.a['href'])
		#print(row)
	#print(urlval)
	urlscrape = urlval[0]
	r1 = requests.get(urlscrape)
	soup1 = BeautifulSoup(r1.content,'html.parser')
	#print(soup1.prettify())
	descanime = soup1.find('p',attrs = {'itemprop':'description'})
	descmanga = soup1.find('span',attrs = {'itemprop':'description'})
	#print(descanime.text)
	if descanime == None:
		return descmanga.text
	return descanime.text
#description = anime_desc(anime)
#print(description)


