import requests
import parser

home = "https://kulms.korea.ac.kr"

def login(uid,upw):
    global home
    response = requests.get(home)
    cookies = dict(response.cookies)
    
    #login first step
    url = "https://auth.korea.ac.kr/directLoginNew.jsp"
    loginData = {"id":uid, "pw":upw,"returnURL":"kulms.korea.ac.kr"}
    response = requests.post(url,loginData)
    #print response.headers, response.text

    #login second step
    url = "https://kulms.korea.ac.kr"
    msg = parser.parseMsg(response.text)
    data = {"sYN":"Y","sWHY":"","msg":msg}
    response = requests.post(url,data)
    sid = response.cookies['s_session_id']

    return sid
    
