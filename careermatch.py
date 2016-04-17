#!/usr/bin/env python
import mechanize
from bs4 import BeautifulSoup
import unicodedata
import re
import urllib2
import os.path
import time

def careermatch(username, password):
	browser = mechanize.Browser(factory=mechanize.RobustFactory())
	browser.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)')]
	browser.set_handle_robots(False)
	browser.open("http://training.careermatch-uk.com/eco_login.php")
	browser.select_form(nr=0)
	browser.form.set_all_readonly(False)
	browser["txtUserId"] = username
	browser["txtPassword"] = password
	browser.submit()
	browser.open("http://training.careermatch-uk.com/eco_learn.php?filter=enrolled")
	html1 = browser.response().read()
	for course in re.findall(r'<dt>(.*?)</dt>', html1):
		if "href" in course:
		    soup1 = BeautifulSoup(course, "html.parser")
		    tag1 = soup1.find("a")
		    url1 = "http://training.careermatch-uk.com/"+tag1["href"]
		    name1 = soup1.getText()
		    print name1
		    browser.open(url1)
		    html2 = browser.response().read()
		    for topic in re.findall(r'<dt>(.*?)</dt>', html2):
		        if "href" in topic:
		            soup2 = BeautifulSoup(topic, "html.parser")
		            tag2 = soup2.find("a")
		            url2 = "http://training.careermatch-uk.com/"+tag2["href"]
		            name2 = soup2.getText()
		            print "\t"+name2
		            browser.open(url2)
		            html3 = browser.response().read()
		            pattern = re.compile(r'\s+')
		            html3 = re.sub(pattern, ' ', html3)
		            for mp4 in re.findall(r'{ file: "(.*?)" , label: "SD"}', html3):
		                url3 = "http"+mp4.split('http')[-1]
		                name3 = url3.split('/')[-1]
		                print "\t\t"+name3
		                if not os.path.isfile(name3):
 				            time.sleep(1)
				            u = urllib2.urlopen(url3)
				            f = open(name3, 'wb')
				            meta = u.info()
				            file_size = int(meta.getheaders("Content-Length")[0])
				            print "\t\t\tDownloading: %s Size: %s MB" % (name3, file_size/(1024*1024))
				            print "\t\t\t",
				            file_size_dl = 0
				            block_sz = 8192
				            status=""
 				            time.sleep(1)
				            while True:
				                buffer = u.read(block_sz)
				                if not buffer:
				                    break
				                file_size_dl += len(buffer)
				                f.write(buffer)
				                if r"[%3.0f%%]" % (file_size_dl * 50. / file_size) != status:
				                    status = r"[%3.0f%%]" % (file_size_dl * 50. / file_size)
				                    print ".",
				            f.close()
				            print "\n",

while True:
	try:
	    careermatch("your username", "your password")
	except:
		pass

exit