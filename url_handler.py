import urllib.request
import urllib.response
import urllib.error
import urllib.robotparser
from bs4 import BeautifulSoup


def get_urls_in_request(url_list):
    """
    url로부터 response 객체를 얻는 함수
    접속 가능한 reponse 객체만 반환

    :param url_list: url의 리스트
    :return: response객체 리스트
    """
    for idx in range(0, len(url_list)):
        url = str(url_list[idx])
        if url.startswith("https://") or url.startswith("http://"):
            if url.endswith("/"):
                continue
            else:
                url_list[idx] = url_list[idx] + "/"
        else:
            if url.endswith("/"):
                url_list[idx] = "https://" + url_list[idx]
            else:
                url_list[idx] = "https://" + url_list[idx] + "/"

    res_url = list()

    for idx in range(0, len(url_list)):
        response = None
        try:
            headers = {'User-Agent': 'Chrome/66.0.3359.181'}
            # 403 에러를 피하는 용도
            request = urllib.request.Request(url_list[idx], headers=headers)
            response = urllib.request.urlopen(request)
        except urllib.error.URLError as e:
            continue
        res_url.append(response)

    return res_url


def get_urls_in_string(url_list):
    """
    url로부터 url 문자열을 얻는 함수
    접속 가능한 url 문자열만 반환

    :param url_list: url의 리스트
    :return: 문자열 리스트
    """
    for idx in range(0, len(url_list)):
        url = str(url_list[idx])
        if url.startswith("https://") or url.startswith("http://"):
            if url.endswith("/"):
                continue
            else:
                url_list[idx] = url_list[idx] + "/"
        else:
            if url.endswith("/"):
                url_list[idx] = "https://" + url_list[idx]
            else:
                url_list[idx] = "https://" + url_list[idx] + "/"

    res_url = list()

    for idx in range(0, len(url_list)):
        response = None
        try:
            headers = {'User-Agent': 'Chrome/66.0.3359.181'}
            request = urllib.request.Request(url_list[idx], headers=headers)
            response = urllib.request.urlopen(request)
        except urllib.error.URLError as e:
            continue
        res_url.append(response.url)
    return res_url


def text_extract_from_res_obj_list(response_obj_list):
    """
    response객체를 통해 웹페이지의 텍스트 추출

    :param response_obj_list: response객체 리스트
    :return: 텍스트 리스트
    """
    text_list = list()
    rp = urllib.robotparser.RobotFileParser()
    for response_obj in response_obj_list:
        robotstxt = response_obj.url
        index = robotstxt.find("/", 8)
        robotstxt = robotstxt[:index + 1]
        robotstxt += "robots.txt"
        # print(robotstxt)
        rp.set_url(robotstxt)
        rp.read()
        # robots.txt에 의거하여 텍스트 추출이 가능하다면 텍스트를 추출한다.
        # 만약 robots.txt의 방해가 싫다면 if를 지우고 들여쓰기를 고치면 된다.
        if rp.can_fetch("*", response_obj.url):
            # print("can fetch!")
            encoding = response_obj.headers.get_content_charset(failobj='utf8')
            p = response_obj.read().decode(encoding)
            soup = BeautifulSoup(p, 'html.parser')
            html_text = soup.get_text(separator=" ", strip=True)
            html_text = html_text.replace("\n", " ")
            html_text = html_text.replace(u"\xa0", u" ")
            text_list.append(html_text)
        response_obj.close()
    return text_list
