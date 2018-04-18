import requests
import json

def getSubmissions(sub_red):
    base_path = 'https://api.pushshift.io/reddit'
    submissions_path = '/search/submission/?'

    after = 0
    prev_after = None
    sub_dict = {}

    while True:
        params = ('size=500&sort=acs&after=' + str(after)
                 + '&subreddit=' +  sub_red)

        print('Searching for posts after', after)
        sub_data = getData(base_path + submissions_path + params)

        if len(sub_data['data']) == 0:
            break

        for post in sub_data['data']:
            if 'selftext' in post.keys():
                if post['selftext'] != '':
                    sub_dict[post['id']] = [post['created_utc'], post['author'],
                                            post['title'], post['selftext'],
                                            post['url']]
                else:
                    sub_dict[post['id']] = [post['created_utc'], post['author'],
                                            post['title'], None, post['url']]
            else:
                sub_dict[post['id']] = [post['created_utc'], post['author'],
                                        post['title'], None, post['url']]

        after = sub_data['data'][-1]['created_utc']

    return sub_dict

def addComments(sub_dict):
    base_path = 'https://api.pushshift.io/reddit'
    comment_id_path = '/reddit/submission/comment_ids/'
    comments_path = '/search/comment/?'

    for sub_id in sub_dict.keys():
        id_data = getData(base_path + comment_id_path + sub_id)
        comment_ids = [id_data['data']]

        # TODO fetch all comments and add them to sub_dict/make new data
        # structure to encompass comments

def getData(path):
    batch = requests.get(path)
    decoder = json.JSONDecoder()
    return decoder.decode(batch.text)
