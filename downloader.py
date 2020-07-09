#import requests as req
import glob
import hashlib
import os
import json
import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()
with open('modlistdownload.json', 'r') as mlfile:
    mld = json.load(mlfile)

def download_mod(modinfo):
    print('Downloading {}'.format(modinfo['filename']))
    mod_screen = scraper.get(modinfo['link'], stream=True)

    soup = BeautifulSoup(mod_screen.text)
    haslink = soup.findAll("p", {"class": "text-sm"})[0]

    mod_download = scraper.get("https://www.curseforge.com"+haslink.findAll("a", href=True)[0].get('href'),stream=True)
    with open('mods/'+modinfo['filename'], 'wb') as mod_file:
        for chunk in mod_download.iter_content(chunk_size=1024):
            mod_file.write(chunk)
            mod_file.flush()
        mod_file.close()
    print('Finished downloading {}'.format(modinfo['filename']))

for mod in mld:
    filename = mod['filename']
    md5hash = mod['md5hash']

    if os.path.exists('mods/'+filename):
        with open('mods/'+filename, 'rb') as modfile:
            calculated_hash = hashlib.md5(modfile.read()).hexdigest()
            if calculated_hash == md5hash:
                print('{} is up to date!'.format(filename))
            else:
                modfile.close()
                os.remove('mods/'+filename)
                download_mod(mod)
    else:
        oldmodlist = glob.glob('mods/'+mod['glob'])
        if oldmodlist:
            print('Found old version of mod. Replacing {} with {}'.format(oldmodlist[0], mod['filename']))
            for oldmod in oldmodlist:
                os.remove(oldmod)
        download_mod(mod)
