import urllib, urlparse
import re
import csv
from bs4 import BeautifulSoup
import time
from threading import Thread

class Site:

    def __init__(self, baseURL):
        self.baseURL = baseURL
        self.visited = []
        self.count = 0
        self.urls = [baseURL]
        self.emails = []
        


    #def __getLinkList__(self):
        '''
        gather links with same domain up2 100 iterations of search
        '''
        while len(self.urls) > 0:
            self.count += 1
            print "number of urls %s at count: %s" % (str(len(self.visited)), str(self.count))
            if self.count > 20 :
                break
            try:
                htmltext = urllib.urlopen(self.urls[0]).read()
                
            except:
                print 'not recognized as a valid url: %s' % self.urls[0]
            try:
                soup = BeautifulSoup(htmltext)
            #    for tag in soup.findAll('a', href = True):
            #        tag['href'] = urlparse.urljoin(self.baseURL , tag['href'])
            #        #if tag['href'].find('www.') != -1:
            #        #    tag['href'].replace('www.', '')
            #        if self.baseURL in tag['href'] and tag['hreraf'] not in self.visited:
           #             self.urls.append(tag['href'])
          #              self.visited.append(tag['href'])
                for tag in soup.findAll('a', href = True):
                    tag['href'] = urlparse.urljoin(self.baseURL , tag['href'])
                    if tag['href'].find('www.') != -1:
                        tag['href'].replace('www.', '')
                        if self.baseURL in tag['href'].replace('www.', '') and tag['href'] not in self.visited:
                            self.urls.append(tag['href'])
                            self.visited.append(tag['href'])
                    if self.baseURL in tag['href'] and tag['href'] not in self.visited:
                        self.urls.append(tag['href'])
            except:
                soup = None
            self.urls.pop(0)
            
        #return self.visited #not need within class the self.visited is update

    def getEmails(self):
        emailList =[]
        count = 0
        print 'searching through email list of %s' % str(len(self.visited))
        for link in self.visited:
            print '%s/%s' % (str(count), str(len(self.visited)))
            count += 1
            try:
                f = urllib.urlopen(link)
                s = f.read()
                #number = re.findall(r"\+d{2}\s?0?\d{10}", s)
                emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",s)
                if emails:
                    emailList.extend(emails)
            except:
                print 'URL not valid'
            

        self.emails.extend(set(emailList))
        if self.emails == []:
            self.emails = ['email not found search ' + str(len(self.visited))+ ' urls']
        
        return self.emails
            



def baseDomain(url):
    temp = urlparse.urlparse(url)
    if temp.netloc[:3] == 'www':
        straight = temp.netloc[4:]
        path = temp.scheme + '://' + straight
    else:
        path = temp.scheme + '://' + temp.netloc
    return path
    

def getFile():
    f = csv.reader(open('siteList.csv'))
    s = []
    for line in f:
        name, url = line[0], line[-1]
        domain = baseDomain(url.strip())
        s.append([name.strip(), domain, url])
    return s[34:35]




def main():
    raceList = getFile()
    for race in xrange(len(raceList)):
        print raceList[race][1] , race
        #url = 'http://taggrun.com ----'
        
        
        scrape = Site(raceList[race][1])
        fd = open('results.csv', 'a')
        mycsvrow = [raceList[race][0], raceList[race][1], raceList[race][2], ', '.join(scrape.getEmails()), '\n']
        print "done with %s, @ url: %s found %s email(s)"  % (str(raceList[race][0]), str(raceList[race][1]), str(len(scrape.emails)))
        fd.write(', '.join(mycsvrow))
        fd.close()
        #time.sleep(float('{:.2f}'.format(random.random())))
    '''
    url = 'http://www.runlehighvalley.com'
    scrape = Site(url)
    print scrape.getEmails()
    
    
    
    
    #scrape = Site(url)
    #print scrape.getEmails()
    '''



    





if __name__ == '__main__':
    main()



