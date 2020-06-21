import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('./serviceAccount.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()



def getNews(limit, offset):
    news_ref = db.collection("News")
    news = news_ref.order_by('published_at', direction=firestore.Query.DESCENDING).limit(limit).offset(offset).stream()
    news = [n.to_dict() for n in news]
    return news

def getNewsByCategory(limit, offset, category):
    news_ref = db.collection("News")
    news = news_ref.where('category', '==', category).order_by('published_at',
     direction=firestore.Query.DESCENDING).limit(limit).offset(offset).stream()
    news = [n.to_dict() for n in news]
    return news

def getNewsByCategoryAndField(limit, offset, category, field):
    news_ref = db.collection("News")
    if category == "Sport":
        news = news_ref.where('category', '==', 'Sport').where('sport', '==', field).order_by('published_at',
         direction=firestore.Query.DESCENDING).limit(limit).offset(offset).stream()
    else:
        news = news_ref.where('category', '==', category).where('field', '==', field).order_by('published_at',
         direction=firestore.Query.DESCENDING).limit(limit).offset(offset).stream()     
    news = [n.to_dict() for n in news]
    return news
def getNewsBySportAndLeague(limit, offset, sport, league):
    news_ref = db.collection("News")
    news = news_ref.where('sport', '==', sport).where('category', '==', 'Sport').where('league', '==', league).order_by('published_at',
     direction=firestore.Query.DESCENDING).limit(limit).offset(offset).stream()
    news = [n.to_dict() for n in news]
    print (news)
    return news
def incrementAction(_hash,action):
    news_ref=db.collection("News")
    news = news_ref.where('hash', '==', _hash).stream()
    news = [n.to_dict() for n in news]
    print (news)
    data = {action: news[0][action] + 1}
    news_ref.document(_hash).set(data, merge=True)
    return news
    
# incrementLike("f7410bc4cb602bd9883a80b1d4f5a9c17dbd205b05bc79237f299b11", "views")
# getNewsBySportAndLeague(10,1,"FOOTBALL","LIGUE1")