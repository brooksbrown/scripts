from bs4 import BeautifulSoup
import urllib.request
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('function_title')
parser.add_argument('--full', action='store_true')
args = parser.parse_args()

page = urllib.request.urlopen('http://php.net/function.' + args.function_title)
html = page.read()
soup = BeautifulSoup(html)
refpurpose = soup.find_all("p", attrs={"class": "refpurpose"})[0]
title = refpurpose.span.get_text()
desc = refpurpose.find_all('span', class_='dc-title')[0].get_text()
synopsis = soup.find_all('div', class_='methodsynopsis')[0].get_text().replace('\n', '')
synopsis = ' '.join(synopsis.split())
comment = soup.find_all('p', class_='rdfs-comment')[0].get_text()
print('\n\n' + title + ' - ' + desc + '\n\n' + synopsis + '\n' + comment)
if args.full:
    parameters = soup.find_all('div', class_='refsect1 parameters')[0].get_text()
    parameters = os.linesep.join([s for s in parameters.splitlines() if s])
    print('\n\n' + parameters)


