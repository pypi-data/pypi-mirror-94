from tqdm import tqdm
from sys import platform as current_platform
from bs4 import BeautifulSoup as bs
from .utils import relative_to_static, setup_browser, download_asset

class Archiver(object):
    def __init__(self,**kwargs):
        self.test_scenario = kwargs['test_scenario']
        
    def add_directory_base(self, directory_base):
        self.directory_base = directory_base
    def add_directory_image(self, directory_image):
        self.directory_image = directory_image
    def add_directory_script(self, directory_script):
        self.directory_script = directory_script
    def add_directory_style(self, directory_style):
        self.directory_style = directory_style
    def add_directory_icon(self, directory_icon):
        self.directory_icon = directory_icon
        
    def parse_asset_url(self, elem_url):
        if(not elem_url):
            # if elem does not contain src or href attribute, just skip
            return None
            
        elem_url = relative_to_static(self.archival_url, elem_url);
        if(not elem_url or elem_url in self.fetchedUris):
            return None
        self.fetchedUris.append(elem_url)
        
        return elem_url
    
    def parse_nav_url(self, elem_url):
        if(not elem_url or self.archival_url == elem_url or elem_url + "/index.html" == self.archival_url or elem_url == "/" or elem_url == "index.html"): # FIXME: not properly impl
            return None

        elem_url_static = relative_to_static(self.archival_url, elem_url);
        if(not elem_url_static):
            return None
        
        return elem_url_static

    def archive_links_process_attr(self, elem, attr):
        if(attr in elem.attrs):
            elem.attrs.pop(attr)

    def archive_links_process(self, elem):
        path_dir = self.directory_style
        if(elem.attrs.get("type") == "text/css" or (elem["rel"] and elem["rel"][0] == "stylesheet")):
            self.archive_links_process_attr(elem, "crossorigin")
            self.archive_links_process_attr(elem, "integrity")
        else:
            path_dir = self.directory_icon
            
        return path_dir

    def archive_links(self):
        self.fetchedUris = []
        for elem in tqdm(self.soup.find_all("link"), "Extracting links (css and ico)"):
            elem_url = self.parse_asset_url(elem.attrs.get("href"))
            if(not elem_url):
                continue
            
            path_dir = self.archive_links_process(elem)
            file_dl = download_asset(elem_url, self.directory_base, path_dir, self.test_scenario)
            elem.attrs["href"] = file_dl
        
        return True

    def archive_scripts(self):
        self.fetchedUris = []
        for elem in tqdm(self.soup.find_all("script"), "Extracting scripts (js)"):
            elem_url = self.parse_asset_url(elem.attrs.get("src"))
            if(not elem_url):
                continue
            
            file_dl = download_asset(elem_url, self.directory_base, self.directory_script, self.test_scenario)
            elem.attrs["src"] = file_dl
        
        return True

    def archive_images(self):
        self.fetchedUris = []
        for elem in tqdm(self.soup.find_all("img"), "Extracting images (img)"):
            elem_url = self.parse_asset_url(elem.attrs.get("src"))
            if(not elem_url):
                continue
            
            file_dl = download_asset(elem_url, self.directory_base, self.directory_image, self.test_scenario)
            elem.attrs["src"] = file_dl
        
        return True

    def archive_urls(self):
        # change all a hrefs
        for elem in tqdm(self.soup.find_all("a"), "Fixing links"):
            elem_url = elem.attrs.get("href")
            elem_url_static = self.parse_nav_url(elem_url)
            if(not elem_url_static): # FIXME: run proper regression test
                continue
            
            print("Fixing url from " + elem_url_static + " to " + elem_url)
            elem.attrs["href"] = elem_url_static
            
        return True
    
    def driver_start(self, driver_path):
        self.driver = setup_browser(driver_path)
        
    def perform(self, archival_url):
        self.archival_url = archival_url

        # start by browsing
        self.driver.get(self.archival_url)
        
        # read raw website through BeautifulSoup
        self.soup = bs(self.driver.page_source, "html.parser")

        # archive assets -- TODO: check if each dir has been added
        self.archive_links()
        self.archive_scripts()
        self.archive_images()
        self.archive_urls()
            
        if(self.test_scenario != True):
            f = None
            file_content = ""
            if(current_platform == "win32"):
                file_content = str(self.soup.prettify())
                f = open(self.directory_base + "index.html", "w", encoding='utf-8')
            else:
                file_content = self.soup.prettify()
                f = open(self.directory_base + "index.html", "w")
            print(file_content, file=f)
                
        return True