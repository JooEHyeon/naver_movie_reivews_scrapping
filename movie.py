import requests
from bs4 import BeautifulSoup
import csv

# soup_objects = []

# search_input = input()

URL = 'https://movie.naver.com/movie/running/current.nhn'

response = requests.get(URL)
soup = BeautifulSoup(response.text,'html.parser')
movie_section = soup.select('div[id = container] > div[id = content] > div.article > div.obj_section > div.lst_wrap > ul.lst_detail_t1 >li')

headers = {
    'authority': 'movie.naver.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'iframe',
    'referer': 'https://movie.naver.com/movie/bi/mi/point.nhn?code=189069',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=NDDNIVLZXIBF6; NRTK=ag#all_gr#1_ma#-2_si#0_en#0_sp#0; nid_inf=-1542357834; NID_AUT=yf2GXLdXl6kA7ukklVOPJGEu8taQXmHOhMo2d+eO8p9Gg1ORkEXMiq7FskSCxiUI; NID_JKL=g24PjSo1omxIKP72bZgvrh9BEwD340TQdA3EWpcqsGo=; nx_ssl=2; _ga_7VKFYR6RV1=GS1.1.1594812240.1.1.1594814446.60; MM_NEW=1; NFS=2; MM_NOW_COACH=1; _fbp=fb.1.1594954434454.1127767840; _ga=GA1.1.466947612.1594738208; _ga_4BKHBFKFK0=GS1.1.1594954433.1.0.1594954442.51; NDARK=Y; recent=%uB124%uC774%uBC84%20%uC601%uD654; NID_SES=AAABqOk9RrFcwKfVvNcUGG2ZxbO4NfsKWfdIhh2M66oyUvbGGL/QOUFpcobnDVUhvPsNfbb+ozoCp7NZNULjmfhlXoANyDLOiAxG56sP7do2dSpXvmDJUxCCJWPauXOI2gk3HLKGz3pdMgpUj3WNxMPch1SkavD7OiSWD1VL7VRNtja4cQNIEtZn9S71Xrlq1cfF7ovPVafUCnh1c1LH4nd8IsyCiLCNN5VPPbAm7tvMZaT30Pn/wI1dWfHqCDix1oingbr95N3nNTIQ+vafzEg0ir3E/KCI8mMOAgw/7jUycs0gB9UZlyARaeePNNlu2iATV50vuXd30SYjslXzld+mrjHJLE1TtxSGx4BrvCr+QE9CZzJWsi74oOd1LTSEOosYo5jwd34F4KPlz/P01CA4jEaosbZsxZviTtO/C3/RDMqpNJ0FYfsx1leV5+snNeGfgEy6quaUqWMwQmvp9mfruhYpJHutp79TmzfVfiHm0njGyGQbHSZ9Lyd0JwXRICQLXCieRJYDYvl5R6Oudb5Xx6cX1++oBiX+PURpuHBql5ffxt8d6rZcK3SuCmQIXmJmDA==; REFERER_DOMAIN="d3d3Lmdvb2dsZS5jb20="; csrf_token=ee355adb-3d7c-4ba9-aac8-605cb109d4ee',
}

final_movie_data = []


for movie in movie_section:
    a_tag = movie.select_one('dl.lst_dsc > dt > a')
    movie_name = a_tag.text
    movie_code = a_tag['href'].split('=')[-1]
    # print(movie_name, movie_code)
    movie_data = {'name' : movie_name, 'code' : movie_code}
    final_movie_data.append(movie_data)

# print(final_movie_data[0]['code'])
# print(f"{final_movie_data[0]['code']}asdf")


for movie in final_movie_data:
    movie_score_review = []
    num = 0

    params = (
    ('code', f"{movie['code']}"),
    ('type', 'after'),
    ('isActualPointWriteExecute', 'false'),
    ('isMileageSubscriptionAlready', 'false'),
    ('isMileageSubscriptionReject', 'false'),
    )

    response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', headers=headers, params=params)

    soup = BeautifulSoup(response.text,'html.parser')
    ripple_list = soup.select('body > div > div > div.score_result > ul > li')
    for ripple in ripple_list:
        if ripple.select_one(f'#_filtered_ment_{num} > #_unfold_ment{num}'):
            ripples = ripple.select_one(f'#_filtered_ment_{num} > span > a')
            ripples = ripples['data-src']
            scores = ripple.select_one('div.star_score>em')
            movie_data = {'score' : scores.text, 'review' : ripples}
        else:
            ripples = ripple.select_one(f'#_filtered_ment_{num}')
            scores = ripple.select_one('div.star_score>em')
            movie_data = {'score' : scores.text, 'review' : ripples.text.strip()}
        
        # print(ripples.text.strip())
        # print(scores.text)
        num+=1
        
        # print(movie_data)
        movie_score_review.append(movie_data)
        

    print(movie_score_review)
   


    # with open('movie_rank.csv','a',newline='',encoding='utf-8-sig') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames = ['name', 'code'])
    #     writer.writerow(movie_data)

    #          # print(news_link)
    #          # print(news_title,'\n')



