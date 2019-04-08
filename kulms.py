import requests
import parser
import getpass
import json
import sys
import os

home = "https://kulms.korea.ac.kr"
cacheDir='/tmp/kulms_cache'

def login(uid,upw):
    global home
    response = requests.get(home)
    cookies = dict(response.cookies)

    #login first step
    try:
        url = "https://auth.korea.ac.kr/directLoginNew.jsp"
        loginData = {"id":uid, "pw":upw,"returnURL":"kulms.korea.ac.kr"}
        response = requests.post(url,loginData)
        #print response.headers, response.text

        #login second step
        url = home
        msg = parser.parseMsg(response.text)
        data = {"sYN":"Y","sWHY":"","msg":msg}
        response = requests.post(url,data)
        sid = response.cookies['s_session_id']
    except:
        return False

    return sid

def getLectures(sid):
    cookies = {'s_session_id':sid}
    response = requests.get(home,cookies=cookies)

    url = home+"/webapps/portal/execute/tabs/tabAction"
    data = {"action":"refreshAjaxModule","modId":"_22_1","tabId":"_2_1","tab_tab_group_id":"_2_1"}
    response2 = requests.post(url,data=data,cookies=cookies)
    lectures = parser.parseLecture(response.text,response2.text)
    
    for i in range(len(lectures)):
        url = home+("/webapps/blackboard/execute/announcement?"
            "method=search&context=course_entry&course_id={}"
            "&handle=announcements_entry&mode=view"
        ).format(lectures[str(i)]["courseId"])
        response3 = requests.get(url,cookies=cookies)
        if "강의자료" in response3.text:
            lectures[str(i)].update(parser.addContentId(response3.text,lectures[str(i)]))
    
    for i in range(len(lectures)):
        lecture = lectures[str(i)]
        if "contentId" not in lecture.keys():
            continue
        url = home+("/webapps/blackboard/content/listContent.jsp?"
            "course_id={}&content_id={}&mode=reset"
        ).format(lecture["courseId"],lecture["contentId"])
        response4 = requests.get(url,cookies=cookies)

        hrefs,titles=parser.parseHrefandTitles(response4.text)
        contents={}
        for idx,href,title in zip([_ for _ in range(len(hrefs))],hrefs,titles):
            url = home+href
            try:
                response5 = requests.head(url,cookies=cookies,allow_redirects=False)
            except:
                continue
            location = response5.headers["location"]
            content = {str(idx):{"title":title,"location":location}}
            contents.update(content)
        
        lectures[str(i)].update({"contents":contents})

    return lectures 

def isCacheExist(uid):
    global cacheDir
    return os.path.isfile(cacheDir+'/'+uid+'.cache')

def saveCache(uid,lectures):
    global cacheDir
    cacheDir='/tmp/kulms_cache'
    if not os.path.isdir(cacheDir):
        os.mkdir(cacheDir)
    path = os.path.join(cacheDir,uid+'.cache')
    with open(path,'w') as cacheOut:
        json.dump(lectures,cacheOut)

def loadCache(uid):
    global cacheDir
    path = os.path.join(cacheDir,uid+'.cache')
    with open(path,'r') as cacheIn:
        return json.load(cacheIn)