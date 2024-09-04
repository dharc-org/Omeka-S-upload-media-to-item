#-*- coding: utf-8 -*-

# Omeka-S-upload-media-to-item.py
# v0.2

import requests
import json
import os
import sys
import urllib3

# disable error message for invalid auto generated certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# check arguments
if len(sys.argv) < 5:
    print("Include the following parameters")
    print(" 1) config .json file with credentials")
    print(" 2) an extension - i.e. .jpg")
    print(" 3) path of images files - i.e. images/data")
    print(" 4) an item ID code - i.e. 657")
    print("i.e. $ python3 Omeka-S-upload-media-to-item.py config.json .jpg /media/images_jpg/ 627")
    sys.exit()

# get var from arguments
confJson = sys.argv[1]
extImg = sys.argv[2]
pathImg = sys.argv[3]
itemID = sys.argv[4]

# set params
paramsJson = json.loads(open(confJson, 'rb').read())
apiLink = paramsJson['apiLink']
params = {
    'key_identity': paramsJson['key_identity'],
    'key_credential': paramsJson['key_credential']
}


# list all files with specific extension into "files" array
files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(pathImg):
    for file in f:
        if extImg in file:
            if not file.startswith('._'): #check for Mac OS hidden files
                files.append(os.path.join(r, file))
    break # only current directory and not subdirs
files.sort()

print("Start: upload media to item "+str(itemID)+" | Config: "+confJson+" | Folder: "+pathImg)

# loop every media and upload via post request
i=0
for fpath in files:
    fname = os.path.basename(fpath)
    dataItem = {"o:ingester": "upload", "file_index": str(i), "o:item": {"o:id": itemID}, 
    "dcterms:title":[ { "property_id":1, "property_label":"Title", "@value": fname, "type":"literal" } ] }
    mediaName = ('file['+str(i)+']', (fname, open(fpath, 'rb'), 'image/jpg'))
    mediaUpload = [ ('data', (None, json.dumps(dataItem), 'application/json')) ]
    mediaUpload.append(mediaName)
    response = requests.post(apiLink, params=params, files=mediaUpload, verify=False)
    print(str(i+1), end =". ")
    print(response, end =" -> ")
    print(fname)
    i+=1

print("Finish: uploaded "+str(i)+" media to item "+str(itemID)+" | Folder: "+pathImg+" | Config: "+confJson)
