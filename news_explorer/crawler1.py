from urllib2 import urlopen
from bs4 import BeautifulSoup
import os

dir_path = "/Users/bharat/Desktop/crawler"
if not os.path.exists(dir_path):
	os.mkdir(dir_path)
base_url = 'http://www.democracynow.org/'
year = 2013

dir_path = '/Users/bharat/Desktop/crawler/data/' + str(year)
if not os.path.exists(dir_path):
	os.mkdir(dir_path)

for month in range(1,13):
	
	dir_path = '/Users/bharat/Desktop/crawler/data/' + str(year) + '/' + str(month)
	if not os.path.exists(dir_path):
		os.mkdir(dir_path)
	
	for date in range(1,32):
		complete_url = base_url + str(year) + '/' + str(month) + '/' + str(date) + '/headlines'
		try:
			soup = BeautifulSoup(urlopen(complete_url))
			file_name = str(year) + '-' + str(month) + '-' + str(date) + '.news'
			f = open( os.path.join(dir_path, file_name), 'w+' )
			articles = soup.select('div.headlinetext')
			titles = soup.find_all("h3", attrs={"itemprop": "name"})

			for article, title in zip(articles,titles):
	    			#print 'Title : ', title.text.encode('utf-8').strip(), '\n'
	    			#f.write('Title : ' + title.text.encode('utf-8').strip() + '\n')
				#htmlspaced = html.replace('\r\n', ' ')
	    			f.write(title.text.encode('utf-8').strip().replace('\n',' ') + '$###$')
	    			#print 'Article : ', article.text.encode('utf-8').strip(), '\n'
	    			f.write(article.text.encode('utf-8').strip().replace('\n',' ')  + '\n')
			f.close()
		except:
			pass

