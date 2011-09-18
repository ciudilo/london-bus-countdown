#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
import urllib, sys, json	

if (len(sys.argv) > 1):
  doc = urllib.urlopen("http://accessible.countdown.tfl.gov.uk/arrivals/" + sys.argv[1])
else:
  doc = urllib.urlopen("http://accessible.countdown.tfl.gov.uk/arrivals/50980")
soup = BeautifulSoup(doc)
doc.close()
rawTable = soup.body.div.tbody

def textOf(soup):
    return u''.join(soup.findAll(text=True))

texts = [textOf(n) for n in soup.findAll('td')]
cleanTexts = []

for tagText in texts[:]:
  cleanStr = str(tagText).strip().strip("&#160;")
  cleanTexts.append(cleanStr)

#for a in texts:
#  text = str(a).strip().strip("&#160;")
#  print text
textGroups = zip(*[cleanTexts[x::3] for x in (0, 1, 2)])

for i in textGroups:
  busNum = str(i[0])
  dest = str(i[1])
  duein = str(i[2])
  print busNum + " " + dest + " " + duein

json_data = json.dumps(textGroups)
print json_data
