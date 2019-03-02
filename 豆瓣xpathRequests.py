import requests, json
from lxml import etree


def get_response(url, headers):
    response = requests.get(url, headers=headers)
    return response.content.decode()


def parse_response(response):
    html = etree.HTML(response)
    lis = html.xpath("//div[@id='nowplaying']//ul[@class='lists']/li")
    movie_dict = {}
    for li in lis:
        movie_name = li.xpath("./@data-title")[0]
        score = li.xpath("./@data-score")[0]
        country = li.xpath("./@data-region")[0]
        img = li.xpath(".//img/@src")[0]
        movie_dict[movie_name] = {
            'score': score,
            'country': country,
            'img_url': img
        }
    return movie_dict


def save(movie_dict):
    with open('movie.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(movie_dict, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Referer': 'https://movie.douban.com/'
    }
    url = 'https://movie.douban.com/cinema/nowplaying/beijing/'
    response = get_response(url, headers)
    movie_dict = parse_response(response)
    save(movie_dict)
