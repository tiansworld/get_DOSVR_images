import sys
import json
import urllib.request
import urllib.parse
import os

'''Use urllib to retrieve available dates page'''
'''Available dates page is read and loaded by json.loads to variable date.'''
tempdate, headers = urllib.request.urlretrieve\
       ('http://epic.gsfc.nasa.gov/api/images.php?available_dates')
html = open(tempdate,encoding="utf-8")
date = json.loads(html.read())
html.close()

'''Variable already is a file list of current directory. It is used to check
whether a image has been downloaded. Default place is the directory at which
this script locates.'''
already = os.listdir("./")

'''To save running time of the script, first to compare the available dates'''
'''with the local date file.'''
if 'datefile' in already:
    date_old = open("./datefile",mode='r',encoding='utf-8')
    datefile = date_old.read()
    date_old.close()
    if len(datefile) < len(date):
        date = date[len(datefile):]
        date_old = open("./datefile",mode="a",encoding='utf-8')
        date_old.write(str(date))
        date_old.close()
        
'''If the 'datefile' doesn't exist, then it means you haven't download any'''
'''images, it will begin to download all the images. So don't delete '''
'''datefile, otherwise, the script will try to check every dates available on'''
'''the nasa server, and compare the image names within each day with your local'''
'''image names, this will spend a lot time even no image is need to download.'''
else:
    datefile = open("./datefile",mode="w",encoding='utf-8')
    datefile.write(str(date))
    datefile.close()
    
'''From here, the script will try to download the images that taken by each
dates'''    
for i in date:
    url = 'http://epic.gsfc.nasa.gov/api/images.php?date='+i
    temp_data, headers = urllib.request.urlretrieve(url)
    data = open(temp_data)
    data = json.loads(data.read())
    for f in data:
        if str(f['image']+'.jpg') not in already:
            urllib.request.urlretrieve(\
                "http://epic.gsfc.nasa.gov/epic-archive/jpg/"\
                    +f['image']+'.jpg',str(f['image']+'.jpg'))
            
print("All downloaded. Enjoy!")
