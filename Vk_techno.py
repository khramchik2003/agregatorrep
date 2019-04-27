import requests, json
import psycopg2
conn = psycopg2.connect('dbname=d93m8auhdgpms4 user=ybdvnnlbssjlmh password=28593faeb443003364b372b5973a0fd4f7243d54320ccd1636320ad2cf77e004 host=ec2-54-227-245-146.compute-1.amazonaws.com')
cur=conn.cursor()
LISTOFPOSTS=[]
LISTOFIMAGEURLS=[]
url_techrocks='https://api.vk.com/method/wall.get?domain=techrocks&count=1&offset={}&access_token=873bd720873bd720873bd720b0875e60a38873b873bd720dc42fe9dfcedd6e253ff4fff&v=5.80'
url_wylsa='https://api.vk.com/method/wall.get?domain=wylsacom&count=1&offset={}&access_token=873bd720873bd720873bd720b0875e60a38873b873bd720dc42fe9dfcedd6e253ff4fff&v=5.80'

def do(url_local,com_local):
    best_postid_dict = {}
    post_text = {}
    post_imageurls = {}

    for offset in range(1, 21):
        url = url_local.format(
            offset)
        response = requests.get(url)
        answer = json.loads(response.text)

        if (answer['response']['items'][0]['marked_as_ads'] == 0) and (
                answer['response']['items'][0]['views']['count'] != 0):
            koef = answer['response']['items'][0]['likes']['count'] * (
                    answer['response']['items'][0]['comments']['count'] + answer['response']['items'][0]['reposts'][
                'count']) / answer['response']['items'][0]['views']['count']
            post_id = answer['response']['items'][0]['id']
            best_postid_dict[koef] = post_id
            post_text[post_id] = answer['response']['items'][0]['text']
            if 'attachments' in answer['response']['items'][0].keys():
                if answer['response']['items'][0]['attachments'][0]['type'] == 'photo':
                    post_imageurls[post_id]=answer['response']['items'][0]['attachments'][0]['photo']['sizes'][0]['url']
            else: post_imageurls[post_id]='OUTOFATTACHMENTS'
        else:
            continue

    postid_lst = list(best_postid_dict.keys())
    postid_lst.sort()
    best_postid_lst = []

    for i in range(5):
        best_postid_lst.append(best_postid_dict[postid_lst[i]])

    # output of the most popular posts
    for postid in post_text.keys():
        if postid in best_postid_lst and postid in post_imageurls.keys():
            LISTOFPOSTS.append(post_text[postid])
            LISTOFIMAGEURLS.append(post_imageurls[postid])
            cur.execute("INSERT INTO posts(theme, social_network, post_text, community, imageurl) VALUES (%s, %s, %s, %s, %s)",("Techno", "VK", LISTOFPOSTS[-1], com_local, LISTOFIMAGEURLS[-1]))
    conn.commit()
    return

do(url_techrocks,'TechRocks')
do(url_wylsa,'Wylsacom')