import requests as req
import glob
import hashlib
import os
import json
import cloudscraper
from bs4 import BeautifulSoup

class MCBulkDownloader:
    def __init__(self, mod_list_filename):
        self._scraper = cloudscraper.create_scraper()
        with open(mod_list_filename, 'r') as mlfile:
            self.mld = json.load(mlfile)

    def download_mod(self, modinfo):
        print('Downloading {}'.format(modinfo['filename']))
        if modinfo['link'].startswith('https://www.curseforge.com'):
            mod_screen = self._scraper.get(modinfo['link'], stream=True)

            soup = BeautifulSoup(mod_screen.text)
            haslink = soup.findAll("p", {"class": "text-sm"})[0]

            mod_download = self._scraper.get("https://www.curseforge.com"+haslink.findAll("a", href=True)[0].get('href'),stream=True)
        else:
            mod_download = req.get(modinfo['link'], stream=True)
        with open('mods/'+modinfo['filename'], 'wb') as mod_file:
            for chunk in mod_download.iter_content(chunk_size=1024):
                mod_file.write(chunk)
                mod_file.flush()
            mod_file.close()
        print('Finished downloading {}'.format(modinfo['filename']))

    def StartDownload(self):
        for mod in self.mld:
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
                        self.download_mod(mod)
            else:
                oldmodlist = glob.glob('mods/'+mod['glob'])
                if oldmodlist:
                    print('Found old version of mod. Replacing {} with {}'.format(oldmodlist[0], mod['filename']))
                    for oldmod in oldmodlist:
                        os.remove(oldmod)
                self.download_mod(mod)

if __name__ == '__main__':
    mcbd = MCBulkDownloader('modlistdownload.json')
    mcbd.StartDownload()
