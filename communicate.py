import getpass
import kulms
import os

lectures={}

def listLectures(sid):
    global lectures
    print("##########[your lectures]##########")
    if not lectures:
        lectures = kulms.getLectures(sid)
    
    for idx in range(len(lectures)):
        print("[{idx}] {lectureTitle}".format(idx=idx,lectureTitle=lectures[idx]["title"]))

def lectureAction(lecture,sid):
    global lectures
    while 1:
        print("##########[Actions]##########")
        print("1. Download Material")
        print("2. Return")
        action=int(input(">which action?: "))

        if action == 1:
            if "contents" not in lecture.keys():
                print("[x]No contents in this course.")
                break
            downloadMaterial(lecture["contents"],sid)
        elif action == 2:
            break
        else:
            print("[x]Not available")
            break

def showMaterials(contents):
    print("##########[course materials]##########")
    for idx in range(len(contents)):
        print("[{idx}] {materialTitle}".format(idx=idx,materialTitle=contents[idx]["title"]))

def downloadMaterial(contents,sid):
    showMaterials(contents)
    materialNum=int(input(">which material?: "))

    if materialNum >= len(contents):
        print("[x]Not available")
        return -1

    href = kulms.home+contents[materialNum]["href"]
    title = contents[materialNum]["title"]
    print("wget -O '{}' --no-cookies --header 'Cookie: s_session_id={}' '{}'".format(title,sid,href))
    os.system("wget -O '{}' --no-cookies --header 'Cookie: s_session_id={}' '{}'"
    .format(title,sid,href)
    )

def commLoop(uid,upw):
    if uid!='' and upw!='':
        try:
            sid = kulms.login(uid,upw)
        except:
            pass
    
    while not sid:
        uid = input("Id:")
        upw = getpass.getpass()
        sid = kulms.login(uid,upw)
    
    print("[+]Login success!")
    while 1:
        listLectures(sid)
        lectureIdx=int(input(">which lecture?(idx) :"))
        if lectureIdx >= len(lectures):
            continue
        lectureAction(lectures[lectureIdx],sid)