from flask import Flask, escape, request, render_template, redirect, url_for
from pymongo import MongoClient
from hashids import Hashids
import os

SALT = "INSERT SECURE RANDOM SALT HERE"

shortener = Hashids(salt=SALT)

MONGODB_HOST = os.environ['OPENSHIFT_MONGODB_DB_HOST']
MONGODB_PORT = os.environ['OPENSHIFT_MONGODB_DB_PORT']
client = MongoClient('mongodb://username:password@%s:%s'%(MONGODB_HOST,MONGODB_PORT))
db = client.shurl
collection = db.val2url

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/short',methods=['POST'])
def short_url():
    url = escape(request.form['url'])
    result = collection.find_one({'count': {'$exists': 'true'}})
    count = result['count'] + 1
    short_url = shortener.encode(count)
    document = { 'url' : url, 'value' : count , 'shorturl' : short_url}
    collection.insert_one(document)
    collection.update({'count': {'$exists': 'true'}},{'$inc':{'count':1}})
    return redirect(short_url+'/info')   

@app.route('/<shorturl>/info')
def short_url_info(shorturl):
    result = collection.find_one({'shorturl': shorturl})
    url = result['url']
    return render_template('info.html',surl=url_for('short_url_redir', shorturl=shorturl,_external=True),url=url)

@app.route('/<shorturl>')
def short_url_redir(shorturl):
    result = collection.find_one({'shorturl': shorturl})
    url = result['url']
    return redirect(url)

if __name__ == '__main__':
    app.run()
