import csv
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import cchardet
import re
import urllib
import warnings
import requests
import io
import os


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


def getDirectory(siteURL):
  #
  folder_name = siteURL
  folder_directory = "D:\Misinformation Intentiment Analysis\Webpages\Main Pages\\"

  strPath = folder_directory + folder_name
  path = os.path.join(folder_directory, folder_name)
  try:
    os.mkdir(path)
  except FileExistsError:
    print("Looks like this directory already exists. Continuing program...")
  finally:
    return strPath



def getNewURL(siteURL):
  link = "http://"
  link += siteURL
  r = requests.get(link)
  newurl = r.url
  if(newurl.endswith('/')):
    newurl = newurl[0:-1]

  return newurl

def createHTMLfile(siteURL, directory, corpus):
  text = "\\"
  filename = text + siteURL
  html = ".html"
  HTMLfile = filename + html

  flocation = directory + HTMLfile

  file = open(flocation, "w")
  try:
    file.write(corpus)
  except UnicodeEncodeError:
    with io.open(flocation, "w", encoding="utf-8") as f:
      f.write(corpus)
  finally:
    file.close()

def createTextFile(siteURL, directory, corpus):
  text = "\\"
  textfile = text + siteURL
  text = ".txt"
  textfile += text

  flocation = directory + textfile

  file = open(flocation, "w")
  try:
    file.write(corpus)
  except UnicodeEncodeError:
    with io.open(flocation, "w", encoding="utf-8") as f:
      f.write(corpus)
  finally:
    file.close()

def addToErrorList(url, writefunction):
  filelocation = "D:\Misinformation Intentiment Analysis\Webpages\Main Pages\\"
  filelocation.strip()
  filename = "InaccessibleSitesList-1.txt"
  file = filelocation + filename

  f = open(file, writefunction)
  f.write(url + "\n")

def addToOnlineSites(url, writefunction):
  filelocation = "D:\Misinformation Intentiment Analysis\Webpages\Main Pages\\"
  filelocation.strip()
  filename = "NewOnlineSitesList-1.txt"
  file = filelocation + filename

  f = open(file, writefunction)
  f.write(url + "\n")


def main():
  listOfFakeNewsWebsites = ReadInData()
  failCounter = 0
  i = 0

  while(i < 833):
    print("+++++++++++++++++++++++++++++++++++++++")
    print("i = " + str(i))
    print("failCounter = " + str(failCounter))

    if(i == 810 or i == 638 or i == 425):
      i+=1
      failCounter += 1
      continue

    link = listOfFakeNewsWebsites[i]
    corpus = OutputBeautifulSoup(link)

    if(corpus != "e"):
      try:
        url = getNewURL(link) # For redirected URL's
        addToOnlineSites(url, "a")

      except Exception:
        print("Note: URL that is saved may have a redirect")
        oldurl = link + "+++" #not getting the "latest" URL will add three '+' to the old URL
        addToOnlineSites(oldurl, "a")

      finally:
        link = link.replace("/","%") # slashes cause errors in File Explorer
        directory = getDirectory(link)
        createTextFile(link, directory, corpus)
        createHTMLfile(link, directory, corpus)# Errors occur when opening page as html, so we'll stick with .txt files
      print()
    else:
      addToErrorList(link, "a")
      failCounter += 1

    i+=1
  #/end for
  total = i
  success = total - failCounter + 2

  print("----------------------------")
  print("    Number of sites: " + str(total))
  print("----------------------------")
  print("Sites saved: " + str(success))
  print("Websites Unavailable: " + str(failCounter))

main()

#Everything after this line might come in handy later
#can be ignored for now.
#########################

def test():
  listOfFakeNewsWebsites = ReadInData()
  siteURL = listOfFakeNewsWebsites[534]
  siteURL = siteURL.replace("/", "%")
  print(siteURL)

#test()
