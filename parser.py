import re
from bs4 import BeautifulSoup as bs

def parseMsg(response):
    soup = bs(response,'html.parser')
    msg = soup.find("input",{"name":"msg"})["value"]
    return str(msg)

def parseLecture(response,response2):
    soup = bs(response,'html.parser')
    _divLectureWrapperTable = soup.find("div",{'id':'module:_243_1'})
    _divLectureTable = _divLectureWrapperTable.find_all("div")[1]
    _tableLecture = _divLectureTable.find("table")
    _lectures = _tableLecture.find_all("td")[5:]
    _titles = _lectures[::5]
    _lectureIds = _lectures[1::5]
    
    titles=[]
    Ids=[]
    for _title in _titles:
        if _title.string not in titles:
            titles.append(_title.string)
    
    for _lectureId in _lectureIds:
        if _lectureId.string not in Ids:
            Ids.append(_lectureId.string)

    lectures = {str(idx):{"id":Id,"title":title} for idx,Id,title in zip([i for i in range(len(Ids))],Ids,titles)}

    soup = bs(response2,'lxml')
    _lectureAnchors = soup.find_all('a',attrs={"target":"_top"})
    _lectureHrefs = []
    
    for _anchor in _lectureAnchors:
        for title in titles:
            if _anchor.string == "[학부]"+title:
                _lectureHrefs.append(title)
                _lectureHrefs.append(_anchor["href"])

    for i in range(1,len(_lectureHrefs),2):
        cId=re.search("id=([_\d]*)&",_lectureHrefs[i]).group(1)
        for lectureIdx in lectures.keys():
            if lectures[lectureIdx]["title"]==_lectureHrefs[i-1]:
                lectures[lectureIdx].update({"courseId":cId})

    return lectures
    
def addContentId(response,lecture):
    soup = bs(response,'html.parser')
    href = soup.find("span",{"title":"강의자료"}).parent["href"]
    contentId =  re.search("content_id=([_\d]*)&",href).group(1)
    
    lecture.update({"contentId":contentId})

    return lecture

def parseHrefandTitles(response):
    try:
        soup = bs(response,'html.parser')
        _materialDiv = soup.find("div",{"id":"containerdiv"})
        __anchors = _materialDiv.find_all("a")
        _anchors=[]
        for _anchor in __anchors:
            if _anchor.has_attr("id"):
                continue
            if _anchor.has_attr("class"):
                continue
            _anchors.append(_anchor)

        hrefs=[]
        titles=[]
        for idx,_anchor in enumerate(_anchors):
            href=_anchor["href"]    
            title=_anchor.find("span")
            if not title:
                title = _anchor.find("img")
            if(len(title.string.split('.'))==1):
                title=title.string
            else:
                title=''.join(title.string.split('.')[:-1])
            hrefs.append(href)
            titles.append(title)

        return hrefs,titles
    except:
        return hrefs,titles