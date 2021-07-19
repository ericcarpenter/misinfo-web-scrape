# Because some of these sites could have redirects

def readindata(loc):
  # Get list of urls from text file location  
  f = open(loc, 'r')
  sitelist = []

  # Read in csv after first row
  for url in f:
    sitelist.append(url.rstrip())
  f.close()
  return sitelist

def main():
  # get 
  locnorobotslist = "D:\\Misinformation Intentiment Analysis\\misinfo-web-scrape\\urldatabase\\NoRobotsFileList.txt"
  norobotslist = readindata(locnorobotslist)
  
  locfullurllist = "D:\\Misinformation Intentiment Analysis\\misinfo-web-scrape\\urldatabase\\FullURLfinal.txt"
  fullurllist = readindata(locfullurllist)
  
  noredirectlist = []
  redirectlist = []
  
  i=0
  while (i < 53):
    urlrobot = norobotslist[i]
    j = 0
    while (j < 482):
      fullurl = fullurllist[j]
      urlfound = fullurl.find(urlrobot)
      
      if (urlfound == -1):
        j+=1 
        continue
      else:
        break
    if (j == 482):
      redirectlist.append(urlrobot)
    else:
      noredirectlist.append(urlrobot)
    i += 1
  for url in redirectlist:
    print(url)
  
main()