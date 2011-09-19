from BeautifulSoup import BeautifulSoup
import urllib, sys
import simplejson as json

class Countdown(object):

  def getCountdownJSON(self, *stop_number):
    if(len(stop_number) == 0):
	doc = urllib.urlopen("http://accessible.countdown.tfl.gov.uk/arrivals/50980")
    else:
	doc = urllib.urlopen("http://accessible.countdown.tfl.gov.uk/arrivals/" + str(stop_number[0]))
    soup = BeautifulSoup(doc)
    doc.close()
    rawTable = soup.body.div.tbody

    texts = [textOf(n) for n in soup.findAll('td')]   
    cleanTexts = []
    for tagText in texts[:]:
      #cleanStr = str(tagText).strip().strip("&#160;")
      cleanStr = str(tagText).strip()
      cleanTexts.append(cleanStr)
    
    textGroups = groupByThree(cleanTexts)
    
    json_data = json.dumps(textGroups)
    return json_data

def textOf(soup):
  return u''.join(soup.findAll(text=True))

def groupByThree(lst):
	"""
	Given input [1,2,3,4,5,6,7,8,9]
	outputs: [(1,2,3),(4,5,6),(7,8,9)]
	"""
	return zip(*[lst[x::3] for x in (0, 1, 2)])

def __init__(self):
	print getCountdownJSON()
