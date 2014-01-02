#Christopher Reeves Web Scraping Tutorial
#simple web spider that returns array of urls. 
#http://youtube.com/creeveshft
#http://christopherreevesofficial.com
#http://twitter.com/cjreeves2011

import urllib
from bs4 import BeautifulSoup
import urlparse
import mechanize
import time
import csv

def swc(url):
    '''
    take a url and returns all urls within that domain
    '''
    #url = "http://sparkbrowser.com"
    br = mechanize.Browser()


    urls = [url]
    visited = [url]
    email_list = []
    count = 0
    while len(urls)>0:
        try:
            br.open(urls[0])
            urls.pop(0)
            for link in br.links():
                #time.sleep(0.2) #reduce load on single site
                newurl =  urlparse.urljoin(link.base_url,link.url)
                count += 1
                if count > 100:
                    print count
                    break
                elif newurl not in visited and url in newurl:
                    visited.append(newurl)
                    urls.append(newurl)
                elif newurl.find('mailto') != -1:
                    email_list.append(newurl[7:])
                
        except:
            print "error"
            try:
                urls.pop(0)
            except:
                print "nothing in url"
           
    return (visited, set(email_list))

def email_search(url):
    pass

def valid_domain(url):
    temp = urlparse.urlparse(url)
    path = temp.scheme + '://' + temp.netloc
    return path

def grab_base_domain(url):
    ''' check to make sure not facebook, and return base domain
    '''
    pass


def main():
    f = csv.reader(open('newlist.csv'))
    fz = csv.writer(open('parsed_v5.csv', 'w'))
    site_directory = []
    print 'opening file list'
    for race in f:
        name, url = race[0], race[-1]
        site_directory.append([name.strip(), url.strip()])
    site_directory= site_directory[33:]
    #site = site_directory[-5]
    #site_list, email_list = swc(site[-1])
    for i in xrange(len(site_directory)):
        race, site = site_directory[i][0], site_directory[i][1]
        site = valid_domain(site)
        print site + ' --> ' + str(i) 
        site_list, email_list = swc(site)
        fz.writerow([name, site, ', '.join(email_list)])
    
    """ 
    for i in xrange(len(site_directory[5])):
        race, web = site_directory[i][0], site_directory[i][1]
        time.sleep(.3)
        site = valid_domain(web)
        print site
        site_list, email_list = swc(site)
        fz.writerow([name, email_list])
        print name, site
     """    


if __name__ == '__main__':
    main()
