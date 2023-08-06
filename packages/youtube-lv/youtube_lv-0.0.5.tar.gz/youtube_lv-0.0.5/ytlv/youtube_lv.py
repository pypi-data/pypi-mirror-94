# coding=utf-8
import requests
import re

class live():
    def islive(self,chid):
        try:
            r = requests.get(f"https://www.youtube.com/channel/{chid}/live")
            if  re.search(r'"isLive":true', r.text) is None:
                return("no")
            else:
                return("yes")
        except:
            return("error")
