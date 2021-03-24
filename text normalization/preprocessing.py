from bs4 import BeautifulSoup
import csv

def get_list_of_inaccessible_sites():
  # Get text from file location
  txtlocation = 'D:\Misinformation Intentiment Analysis\misinfo-web-scrape\webscrape\InaccessibleSites.txt'
  f = open(txtlocation, 'r')

  offlinesiteslist = []
  for line in f:
    url = str(line)
    offlinesiteslist.append(url)
  f.close()
  return offlinesiteslist

def get_list_of_all_sites():
  # Get text from file location
  txtlocation = 'D:\Misinformation Intentiment Analysis\misinfo-web-scrape\webscrape\Allsites.txt'
  f = open(txtlocation, 'r')

  sitelist = []
  for line in f:
    url = str(line)
    sitelist.append(url)
  f.close()
  return sitelist



def generate_list_of_accessible_sites(allsites, inaccessiblesites):

  f = open('D:\Misinformation Intentiment Analysis\misinfo-web-scrape\webscrape\AccessibleSites.txt', "w")
  counter = 0

  for site in allsites:
    available = True
    for url in inaccessiblesites:
      if(url.casefold().__eq__(site.casefold())):
        available = False

    if(available == True):
      f.write(site)
      counter += 1

  f.close()
  print(counter)





def main():
  unavailablesites = get_list_of_inaccessible_sites()
  sitelist = get_list_of_all_sites()

  generate_list_of_accessible_sites(sitelist, unavailablesites)


main()
