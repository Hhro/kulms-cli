import re
from bs4 import BeautifulSoup as bs

def parseMsg(response):
    soup = bs(response,'html.parser')
    msg = soup.find("input",{"name":"msg"})["value"]
    return str(msg)
