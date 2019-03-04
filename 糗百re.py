import urllib.request
import re


def spider(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req).read().decode("utf-8")
    return html


def re_htm(html):
    pattern = r'<h2>(.*?)</h2>.*?<span>(.*?)</span>'
    re_html = re.compile(pattern, re.S)
    content = re_html.findall(html)
    print(content)
    return content


def save(content):
    with open("baikeDuanZi.txt", "a", encoding='utf8') as f:
        for i in content:
            duan = str(i[1]).strip()
            duan1 = duan.replace("<br/>", "").replace(" ", "")
            duanZi = str(i[0]).strip() + ":\n" + duan1 + '\n\n'
            f.write(duanZi)


def main():
    for i in range(1, 11):
        url = "https://www.qiushibaike.com/text/page/" + str(i) + "/"
        html = spider(url)
        content = re_htm(html)
        save(content)


main()
