#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
import urllib, sys, json	

class Countdown(object)

  def getCountdownJSON()
    if (len(sys.argv) > 1):
      doc = urllib.urlopen("http://accessible.countdown.tfl.gov.uk/arrivals/" + sys.argv[1])
      doc = urllib.urlopen("http://accessible.countdown.tfl.gov.uk/arrivals/50980")
    soup = BeautifulSoup(doc)
    doc.close()
    rawTable = soup.body.div.tbody

	texts = [textOf(n) for n in soup.findAll('td')]   
    cleanTexts = []
    for tagText in texts[:]:
      cleanStr = str(tagText).strip().strip("&#160;")
      cleanTexts.append(cleanStr)
    
    textGroups = zip(*[cleanTexts[x::3] for x in (0, 1, 2)])
    
    json_data = json.dumps(textGroups)
    return json_data

def textOf(soup):
  return u''.join(soup.findAll(text=True))