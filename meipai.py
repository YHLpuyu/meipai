import requests
import re
import base64
import os
import sys


def fetch(url):
    r = requests.get(url, None, verify=False)
    return r.text


def matchVideourl(htmlcontent):
    pattern = '(?<=data-video=").*(?=")'
    # pattern='content'
    datavideoids = re.findall(pattern, htmlcontent, re.M)
    return datavideoids


def decode(encoded_string):
    # https://www.jianshu.com/p/15f5c8660f7b
    def getHex(param1):
        return {
            "str": param1[4:],
            "hex": "".join(list(param1[:4])[::-1]),
        }

    def getDec(param1):
        loc2 = str(int(param1, 16))
        return {
            "pre": list(loc2[:2]),
            "tail": list(loc2[2:]),
        }

    def substr(param1, param2):
        loc3 = param1[0 : int(param2[0])]
        loc4 = param1[int(param2[0]) : int(param2[0]) + int(param2[1])]
        return loc3 + param1[int(param2[0]) :].replace(loc4, "")

    def getPos(param1, param2):
        param2[0] = len(param1) - int(param2[0]) - int(param2[1])
        return param2

    dict2 = getHex(encoded_string)
    dict3 = getDec(dict2["hex"])
    str4 = substr(dict2["str"], dict3["pre"])
    return base64.b64decode(substr(str4, getPos(str4, dict3["tail"])))


def downmp4(url, name):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    }
    movie_url = url
    movie_name = name
    downsize = 0
    print("开始下载")
    req = requests.get(movie_url, headers=headers, stream=True, verify=False)
    with (open(movie_name + ".mp4", "wb")) as f:
        for chunk in req.iter_content(chunk_size=10000):
            if chunk:
                f.write(chunk)
                downsize += len(chunk)


def main():
    userid = sys.argv[1]
    videofolder = sys.argv[2]
    html = fetch("https://www.meipai.com/user/"+userid)
    distincturl = ""
    videoidx = 1
    for path in matchVideourl(html):
        if distincturl != path:
            videourl = decode(path)
            print(videourl)
            downmp4(videourl, videofolder + str(videoidx))
            videoidx += 1
            distincturl = path

if __name__ != main:
    main()