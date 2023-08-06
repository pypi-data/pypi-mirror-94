#!/usr/bin/env python

# TODO: https://www.thepythoncode.com/article/using-threads-in-python
# TODO: look into using CSS selectors which is, generally, a more concise way to locate the elements. For example, you can replace table = soup.find('table', {'class': 'tablesorter'}) with table = soup.select_one('table.tablesorter'). Or, you can replace:
#links = []
#for anchor in soup.findAll('a', href=True):
#    if 'imported' in anchor['href']:
#        links.append('link' + anchor['href'])
# CHANGE WITH:
#links = ['link' + anchor['href'] for anchor in soup.select("a[href*=imported]")]
#src: https://codereview.stackexchange.com/questions/89956/using-beautifulsoup-to-scrape-various-tables-and-combine-in-a-csv-file
#src: https://www.scrapingbee.com/blog/python-web-scraping-beautiful-soup/
# TODO: StudlyCaps for classes, camelCase only to conform to pre-existing conventions
# https://en.wikipedia.org/wiki/Comment_(computer_programming)#Tags
# https://www.reddit.com/r/Python/comments/mkes7/how_do_you_keep_track_of_todos/
# TODO: HACK: startswith for http:// url refix / or alternatively, use CSS slc
# TODO: identify *nix and propose Chromium/Chrome/Firefox default driver dir (or accept runtime variable)
# TODO: urllib.request AND requests ???
# TODO: ad-revenue and re-visits help some sites. consider header() javascript if there is internet aval
# XXX: can mass CSS @ https://stackoverflow.com/questions/32962474/how-can-i-create-a-stylesheet-external-link-using-beautifulsoup

# notes:
## options:
### deduplicating script cont
### external script as means of memory storage (elastic mapping)
### inline styles

import sys
import os

from .utils import generate_directories
from .archiver import Archiver

def crawl_finalize(archival_url, driver_path, directory_base, test_scenario):
    #Also the script that check if the directory exists, if it don't exist create it.
    directory_image = 'images/'
    directory_script = 'scripts/'
    directory_style = 'styles/'
    directory_icon = 'icons/'
    
    # TODO: test_scenario as global const // or static var // or env var // or make config helper // anyway idk
    
    # TODO: can remove old ones? or confirm from user input
    generate_directories(directory_base, [directory_image, directory_script, directory_style, directory_icon], test_scenario)
    
    # TODO: phase perform_archival to `setup`, `add_directory`, `perform` lifecycle
    archiver = Archiver(test_scenario=test_scenario)
    archiver.add_directory_base(directory_base)
    archiver.add_directory_image(directory_image)
    archiver.add_directory_script(directory_script)
    archiver.add_directory_style(directory_style)
    archiver.add_directory_icon(directory_icon)
    archiver.driver_start(driver_path)
    archiver.perform(archival_url)
    
    return True

def crawl(archival_url, *positional_parameters, **keyword_parameters):
    #Parse the html in the 'page' variable, and store it in Beautiful Soup format
    driver_path = None
    if('driver' in keyword_parameters):
        driver_path = keyword_parameters['driver']
    else:
        try:
            driver_path = os.environ["CHROME_DRIVER_PATH"] # base port was /usr/lib/chromium/chromedriver
        except KeyError as e:
            print("Expect `CHROME_DRIVER_PATH` as environment variable or as 'driver' parameter, will try to use PATH")
            #raise KeyError("Expect CHROME_DRIVER_PATH as environment variable")

    directory_base = ''
    if('directory_base' in keyword_parameters):
        directory_base = keyword_parameters['output_dir']
    else:
        directory_base = "output/"
    
    test_scenario = None
    if('test_scenario' in keyword_parameters):
        test_scenario = keyword_parameters['test_scenario']
        
    return crawl_finalize(archival_url, driver_path, directory_base, test_scenario)