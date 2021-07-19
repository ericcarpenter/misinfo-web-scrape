from bs4 import BeautifulSoup
import urlib.robotparser as rp

def readindata():
  # Enter your filelocation of the html content (which must be saved as a .txt)
  flocation = 'D:\Misinformation Intentiment Analysis\misinfo-web-scrape\Article Examples\\article-example.txt'

  f = open(flocation, "r", encoding = 'utf-8')
  return f

def getsoupobject(html):
  soup = BeautifulSoup(html, 'html.parser')
  return soup

#def find_useful_links(soup):
  # find all a tags
  # remove tags that do not have the website URL
  # remove tags that are images
  # remove tags that are hidden or have hexcolor codes (ex. #FFF) <-- IMPPORTANT)

def main():
  f = readindata()
  soup = getsoupobject(f)
  print(soup.get_text())
  f.close()

main()
