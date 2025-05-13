from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient 

app = Flask(__name__)

client = MongoClient('localhost',27017)
db=client.please2

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/memo',methods=['POST'])
def post_article():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    
    data = requests.get(url_receive,headers=headers)
    soup = BeautifulSoup(data.text,'html.parser')

    og_image=soup.select_one('meta[property="og:image"]')
    og_title=soup.select_one('meta[property="og:title"]')
    og_description=soup.select_one('meta[property="og:description"]')

    url_image = og_image['content']
    url_title = og_title['content']
    url_description = og_description['content']

    article = {'url': url_receive, 'title': url_title, 'desc': url_description, 'image': url_image,
               'comment': comment_receive}
    db.articles2.insert_one(article)
    
    return jsonify({'result':'success'})

@app.route('/memo',methods=['GET'])
def read_article():
    result = list(db.articles2.find({},{'_id':0}))
    return jsonify({'result':'success', 'articles_list':result})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)

