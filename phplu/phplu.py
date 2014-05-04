from bs4 import BeautifulSoup
import urllib.request
import os
import sys

page = urllib.request.urlopen('http://php.net/function.' + sys.argv[1])
html = page.read()
soup = BeautifulSoup(html)
refpurpose = soup.find_all("p", attrs={"class": "refpurpose"})[0]
title = refpurpose.span.get_text()
desc = refpurpose.find_all('span', class_='dc-title')[0].get_text()
synopsis = soup.find_all('div', class_='methodsynopsis')[0].get_text().replace('\n', '')
synopsis = ' '.join(synopsis.split())
comment = soup.find_all('p', class_='rdfs-comment')[0].get_text()
parameters = soup.find_all('div', class_='refsect1 parameters')[0].get_text()
parameters = os.linesep.join([s for s in parameters.splitlines() if s])
print('\n\n' + title + ' - ' + desc + '\n\n' + synopsis + '\n' + comment + '\n\n' + parameters)


