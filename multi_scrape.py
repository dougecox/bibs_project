import urllib, re
from threading import Thread
from bs4 import BeautifulSoup
import urlparse
import csv

def in_parallel(fn, l):
    for i in l:
        Thread(target=fn, args =(i,)).start()

def sample():
    f = csv.reader(open("newlist.csv"))
    s = []
    for line in f:
        name, url = line[0], line[-1]
        s.append([name.strip(), url.strip()])
    return s

def scrape(race,url):

    fd = open('newfilewritetest.csv', 'a')
    urls = [url] # stack of urls to scrape
    visited = [url] # historic record of urls
    count = 0
    emails = []


    while len(urls) > 0:
        count += 1
        if count >100:
            #return visited
            return emails
        try: 
            htmltext = urllib.urlopen(urls[0]).read()
            if emailfind(urls[0]):
                emails.extend(emailfind(urls[0]))
        except:
            print urls[0]
        soup = BeautifulSoup(htmltext)

        
        urls.pop(0)
        print 'current url count ' + str(len(urls))
        print 'count is at %i' % count
        print '-'*12

        for tag in soup.findAll('a', href = True):
            tag['href'] = urlparse.urljoin(url , tag['href'])
            if url in tag['href'] and tag['href'] not in visited:
                urls.append(tag['href'])
                visited.append(tag['href'])
                #print tag['href']
    #print set(emails)
    mycsvrow = ['\n',race, url,', '.join(set(emails)), '\n']
    print race,url, set(emails)
    fd.write(', '.join(mycsvrow))
    fd.close()
    return set(emails)
    #return visited



def emailfind(url):
    try:
        f = urllib.urlopen(url)
        s = f.read()
        #number = re.findall(r"\+d{2}\s?0?\d{10}", s)
        emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",s)
    except:
        print 'nofind'
    return emails #returns emails
    
def domain_check(url):
    html = urlparse.urlparse(url)
    return html.scheme + "://" +  html.netloc

def main():
    s = sample()
    #new version up to 23
    # new new version up to 61
    s = s[61:]
    r = []
    threadlist = []

    #count = 0
    #count = 23
    count = 61 #www.arlingtonrunnersclub.org
    for races in xrange(len(s)):
        name = s[races][0]
        html = s[races][1]
        count += 1
        print "currently at %s" % domain_check(html)
        print '-----> ', count
        
        site_index = scrape(name,domain_check(html))
        #print site_index
        #for item in site_index:
            #if emailfind(item):
              #  r.append(emailfind(item))
        #r.append(in_parallel(emailfind, scrape(domain_check(html))))
        for u in site_index:
            try: 
                t = Thread(target=emailfind, args=(u,))
                threadlist.append(t)
                t.start()
            except:
                nnn = True
        for g in threadlist:
            g.join()
    print r
    print b











if __name__ == '__main__':
    main()

