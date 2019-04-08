import getpass
import kulms
import os

lectures={}

def listLectures(sid):
    global lectures
    print("##########[your lectures]##########")
    idxs = sorted(lectures.keys(),key=int)
    for idx in idxs:
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
    idxs = sorted(contents.keys(),key=int)
    for idx in idxs:
        title=contents[idx]["title"]
        extension=contents[idx]["location"].split('.')[-1:][0]
        print("[{idx}] {title}.{extension}".format(idx=idx,title=title,extension=extension))

def downloadMaterial(contents,sid):
    while 1:
        showMaterials(contents)
        materialNum=input(">which material?(-1 for back): ")

        if int(materialNum) >= len(contents):
            print("[x]Not available")
            break
        if materialNum == "-1":
            break
            
        location = kulms.home+contents[materialNum]["location"]
        title = contents[materialNum]["title"]
        extension = location.split('.')[-1:][0]
        os.system("wget -O '{}.{}' --no-cookies --header 'Cookie: s_session_id={}' '{}'"
        .format(title,extension,sid,location)
        )

def commLoop(uid,upw,refresh=False):
    global lectures

    if uid!='' and upw!='':
        sid = kulms.login(uid,upw)
    
    while not sid:
        print("[!]Login failed")
        uid = input("Id:")
        upw = getpass.getpass()
        sid = kulms.login(uid,upw)
    
    print("[+]Login success!")
    if not kulms.isCacheExist(uid) or refresh:
        print("[+]getting lecture info from server...")
        lectures=kulms.getLectures(sid)
        kulms.saveCache(uid,lectures)
        print("[+]Saving cache success!")
    else:
        lectures=kulms.loadCache(uid)
        print("[+]Loading cache success!")  

    while 1:
        listLectures(sid)
        lectureIdx=input(">which lecture?(-1 for quit) :")
        if int(lectureIdx) >= len(lectures):
            continue
        if lectureIdx == "-1":
            break
        lectureAction(lectures[lectureIdx],sid)