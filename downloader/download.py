from youtube_dl import YoutubeDL
import requests as req
from rq import get_current_job
import threading
from selenium import webdriver
import status
from pprint import pprint

class DLLogger(object):
    def debug(self, msg):
        print("DEBUG " + msg)

    def warning(self, msg):
        print("WARN " + msg)

    def error(self, msg):
        print("ERROR " + msg)

def download_hook(d):
    if d["status"] == "downloading":
        req.post("http://127.0.0.1:4999/", data={"v": d["eta"]})
        print("Currently downloading")

def finished_hook(d):
    if d["status"] == "finished":
        req.put("http://127.0.0.1:4999/", data={})

ydl_opts = {
    "progress_hooks": [finished_hook, download_hook]
}

def rTest(v_id):
    print(v_id)

def download(v_id):
    print("Entered download")
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([v_id])

    return "video downloaded"

def download_ifunny(url):
    driver = webdriver.Chrome()
    driver.get(url)
    elems = driver.find_elements_by_css_selector(".grid__link")
    pprint(elems)