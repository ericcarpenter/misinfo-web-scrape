import csv
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import cchardet
import re
import urllib
import warnings
import requests
import io
warnings.filterwarnings('ignore', category=DeprecationWarning)

class AppURLopener(urllib.request.FancyURLopener):
  version = "Mozilla/5.0"


def ReadInData():
  # Get CSV from file location
  csvlocation = 'D:\Misinformation Intentiment Analysis\misinfo-web-scrape\sources\sources.csv'
  f = open(csvlocation, 'r')
  reader = csv.reader(f)

  sitelist = []
  skipfirstrow = True

  # Read in csv after first row
  for row in reader:
    if(skipfirstrow == True):
      skipfirstrow = False
      continue
    sitelist.append(row[0])
  f.close()
  return sitelist


def OutputBeautifulSoup(siteURL):
  page = "http://"
  page = page + (siteURL)
  opener = AppURLopener()
  try:
    response = opener.open(page)
    soup = BeautifulSoup(response, 'html.parser')
    soup.encode("utf-8")
    soup = str(soup)
    return soup

  except ValueError:
    print("Ope, we're having trouble with " + siteURL.upper())
    try:
      response = requests.get(page)
    except ValueError:
      print("yikes yeah " + siteURL + " ain't it chief")
      return "e"
    try:
      soup = BeautifulSoup(response, 'html.parser')
    except TypeError:
      print("yikes yeah " + siteURL + " ain't it chief")
      return "e"
    else:
      soup.encode("utf-8")
      soup = str(soup)
      return soup


  except Exception as e:
    print("Yeah, we couldn't get to " + siteURL + " at all. Here's the error:")
    print(e)
    errorMessage = "e"
    return errorMessage

  else:
    return "e"


def createFile(url):
  filename = url
  filename = url.replace(".", "%")
  filename = url.replace("/", "SLASH")

  textfile = ".txt"
  filename += textfile

  filelocation = "D:\Misinformation Intentiment Analysis\misinfo-web-scrape\webscrape\Raw HTML Pages\ "
  filelocation.strip()

  finalfile = filelocation + filename
  finalfile.strip()
  return finalfile

def addToErrorList(url, writefunction):
  filelocation = "D:\Misinformation Intentiment Analysis\misinfo-web-scrape\webscrape\ "
  filelocation.strip()
  filename = "InaccessibleSites.txt"
  file = filelocation + filename

  f = open(file, writefunction)
  f.write(url + "\n")

def addToAccessibleSiteList(url, writefunction):
  filelocation = "D:\Misinformation Intentiment Analysis\misinfo-web-scrape\webscrape\ "
  filelocation.strip()
  filename = "ListOfAccessibleSites.txt"
  file = filelocation + filename

  f = open(file, writefunction)
  f.write(url + "\n")


def main():
  listOfFakeNewsWebsites = ReadInData()
  failCounter = 167
  i = 811

  while(i < 833):

    link = listOfFakeNewsWebsites[i]
    corpus = OutputBeautifulSoup(link)
    if(corpus != "e"):
      flocation = createFile(link)
      file = open(flocation, "w")
      try:
        file.write(corpus)
      except UnicodeEncodeError:
        with io.open(flocation, "w", encoding="utf-8") as f:
          f.write(corpus)
      finally:
        print(link + " successful")
        addToAccessibleSiteList(link, "a")

    elif(failCounter == 0):
      addToErrorList(link, "w")
      failCounter += 1
    else:
      addToErrorList(link, "a")
      failCounter += 1

    print(" ")
    i+=1
  #/end for
  total = i
  success = total - failCounter + 2

  print("----------------------------")
  print("    Number of sites: " + str(total))
  print("----------------------------")
  print("Sites saved: " + str(success))
  print("Websites Unavailable: " + str(failCounter))

#main()

#Everything after this line might come in handy later
#can be ignored for now.
#########################

def test():
  listOfFakeNewsWebsites = ReadInData()
  siteURL = listOfFakeNewsWebsites[810]
  print(siteURL)


#test()

def strip_html_tags(text):
    [s.extract() for s in text(['iframe','script'])]
    stripped_text = text.get_text()
    stripped_text = re.sub(r'[\r|\n|\r\n]+', '\n', stripped_text)
    return stripped_text

def getStatusList():
  statusList = [True, False, True, True, True, True, True, True, True, True, False, True, False, False, False, True, True, True, True, True, True, True, True, "Mixed", "Moved", "Mixed", True, True, False, False, True, True, True, False, True, True, True, False, True]
  return statusList

def misc(siteList):
  page = OutputBeautifulSoup(siteList[24])
  print(page)
  if (page != "e"):
    cleaned = strip_html_tags(page)
    print("------------------------------------------------")
    cleanedlength = str(len(cleaned))
    print("length of cleaning: " + cleanedlength)
    print(cleaned)

def WebsiteIsUnvailable(htmlpage):
  availability = False
  errorMessages = getListOfErrorCodes()

  for error in errorMessages:
    if (htmlpage.find(error) == True):
      availability = False
      break
  return availability

def ScanContentForPoliticalMessages(htmlpage):
  wordsFound = False
  wordlist = getListOfCommonPoliticalWords()
  tokens = strip_html_tags(htmlpage.lower())
  for token in tokens:
    for word in wordlist:
      if (token == word.lower()):
        wordsFound = True
        break
  return wordsFound

def getListOfErrorCodes():
  listOfErrorCodes = ['id="error-information-popup-container"',
  'site is not available',
  'this website was generated by the domain owner',
  'may be for sale'
  'id="errorMessage"',
  ]
  return listOfErrorCodes

def getListOfCommonPoliticalWords():
  wordList = ['biden',
  'trump',
  'antifa',
  'wing',
  'fake',
  'state',
  'democrats',
  'republicans',
  'aoc',
  'liberals',
  'culture',
  'fox',
  'cnn',
  'news',
  'law',
  'laws']

  return wordList
