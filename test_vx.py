import os

import twitfix,twExtract
import cache
import msgs
from flask.testing import FlaskClient
client = FlaskClient(twitfix.app)

twitterAccountName='X' # the fact that I have to do this in the rare chance that they change their username back is stupid

testUser="https://twitter.com/jack"
testUserID = "https://twitter.com/i/user/12"
testUserWeirdURLs=["https://twitter.com/jack?lang=en","https://twitter.com/jack/with_replies","https://twitter.com/jack/media","https://twitter.com/jack/likes","https://twitter.com/jack/with_replies?lang=en","https://twitter.com/jack/media?lang=en","https://twitter.com/jack/likes?lang=en","https://twitter.com/jack/"]
testTextTweet="https://twitter.com/jack/status/20"
testVideoTweet="https://twitter.com/Twitter/status/1263145271946551300"
testMediaTweet="https://twitter.com/Twitter/status/1118295916874739714"
testMultiMediaTweet="https://twitter.com/Twitter/status/1154172324599537665"
testPollTweet="https://twitter.com/norm/status/651169346518056960"
testQRTTweet="https://twitter.com/Twitter/status/1232823570046255104"
testQrtCeptionTweet="https://twitter.com/CatherineShu/status/585253766271672320"
testQrtVideoTweet="https://twitter.com/Twitter/status/1494436688554344449"

# I literally picked a random tweet that twitter marked as 'sensitive' without it being like, actually NSFW.
# Any better suggestions for a tweet to use are welcome
testNSFWTweet="https://twitter.com/kuyacoy/status/1581185279376838657"

textVNF_compare = {'tweet': 'https://twitter.com/jack/status/20', 'url': '', 'description': 'just setting up my twttr', 'screen_name': 'jack', 'type': 'Text', 'images': ['', '', '', '', ''], 'time': 'Tue Mar 21 20:50:14 +0000 2006', 'qrtURL': None, 'nsfw': False}
videoVNF_compare={'tweet': 'https://twitter.com/Twitter/status/1263145271946551300', 'url': 'https://video.twimg.com/amplify_video/1263145212760805376/vid/1280x720/9jous8HM0_duxL0w.mp4?tag=13', 'description': 'Testing, testing...\n\nA new way to have a convo with exactly who you want. We’re starting with a small % globally, so keep your 👀 out to see it in action. https://t.co/pV53mvjAVT', 'thumbnail': 'https://pbs.twimg.com/media/EYeX7akWsAIP1_1.jpg', 'screen_name': twitterAccountName, 'type': 'Video', 'images': ['', '', '', '', ''], 'time': 'Wed May 20 16:31:15 +0000 2020', 'qrtURL': None, 'nsfw': False,'verified': True, 'size': {'width': 1920, 'height': 1080}}
testMedia_compare={'tweet': 'https://twitter.com/Twitter/status/1118295916874739714', 'url': '', 'description': 'On profile pages, we used to only show someone’s replies, not the original Tweet 🙄 Now we’re showing both so you can follow the conversation more easily! https://t.co/LSBEZYFqmY', 'thumbnail': 'https://pbs.twimg.com/media/D4TS4xeX4AA02DI.jpg', 'screen_name': twitterAccountName, 'type': 'Image', 'images': ['https://pbs.twimg.com/media/D4TS4xeX4AA02DI.jpg', '', '', '', '1'], 'time': 'Tue Apr 16 23:31:38 +0000 2019', 'qrtURL': None, 'nsfw': False, 'size': {}}
testMultiMedia_compare={'tweet': 'https://twitter.com/Twitter/status/1154172324599537665', 'url': '', 'description': '10 days. 40 cities. Virtual #Tweetups are happening around the world. Join us and follow the convo! \nhttp://sharedstudios.com/tweetups https://t.co/M436G4fVio', 'thumbnail': 'https://pbs.twimg.com/media/EARxm9FXYAA8qqz.jpg', 'screen_name': twitterAccountName, 'type': 'Image', 'images': ['https://pbs.twimg.com/media/EARxm9FXYAA8qqz.jpg', 'https://pbs.twimg.com/media/EARxm9GW4AEnQkp.jpg', 'https://pbs.twimg.com/media/EARxm9HXkAEEsM0.jpg', 'https://pbs.twimg.com/media/EARxm9QXkAAZIA4.jpg', '4'], 'qrtURL': None, 'nsfw': False, 'verified': True, 'size': {}}

testPoll_comparePoll={"name":"poll2choice_text_only","binding_values":{"choice1_label":{"type":"STRING","string_value":"Mean one thing"},"choice2_label":{"type":"STRING","string_value":"Mean multiple things"},"end_datetime_utc":{"type":"STRING","string_value":"2015-10-06T22:57:24Z"},"counts_are_final":{"type":"BOOLEAN","boolean_value":True},"choice2_count":{"type":"STRING","string_value":"33554"},"choice1_count":{"type":"STRING","string_value":"124875"},"last_updated_datetime_utc":{"type":"STRING","string_value":"2015-10-06T22:57:31Z"},"duration_minutes":{"type":"STRING","string_value":"1440"}}}
testPoll_comparePollVNF={'total_votes': 158429, 'choices': [{'text': 'Mean one thing', 'votes': 124875, 'percent': 78.8}, {'text': 'Mean multiple things', 'votes': 33554, 'percent': 21.2}]}

tokens=os.getenv("VXX_WORKAROUND_TOKENS",None).split(',')

def compareDict(original,compare):
    for key in original:
        assert key in compare
        if type(compare[key]) is not dict:
            if (key == 'verified' or key== 'time') and compare[key]!=original[key]:
                continue # does not match as test data was from before verification changes
            assert compare[key]==original[key]
        else:
            compareDict(original[key],compare[key])

## Specific API tests ##
def test_syndicationAPI():
    tweet = twExtract.extractStatus_syndication(testMediaTweet,workaroundTokens=tokens)
    assert tweet["full_text"]==testMedia_compare['description']

def test_v2API():
    tweet = twExtract.extractStatusV2Legacy(testMediaTweet,workaroundTokens=tokens)
    assert tweet["full_text"]==testMedia_compare['description']

## Tweet retrieve tests ##
def test_textTweetExtract():
    tweet = twExtract.extractStatus(testTextTweet,workaroundTokens=tokens)
    assert tweet["full_text"]==textVNF_compare['description']
    assert tweet["user"]["screen_name"]=="jack"
    assert 'extended_entities' not in tweet
    
def test_extractV2(): # remove this when v2 is default
    tweet = twExtract.extractStatusV2(testTextTweet,workaroundTokens=tokens)

def test_UserExtract():
    user = twExtract.extractUser(testUser,workaroundTokens=tokens)
    assert user["screen_name"]=="jack"
    assert user["id"]==12
    assert user["created_at"] == "Tue Mar 21 20:50:14 +0000 2006"

def test_UserExtractID():
    user = twExtract.extractUser(testUserID,workaroundTokens=tokens)
    assert user["screen_name"]=="jack"
    assert user["id"]==12
    assert user["created_at"] == "Tue Mar 21 20:50:14 +0000 2006"

def test_UserExtractWeirdURLs():
    for url in testUserWeirdURLs:
        user = twExtract.extractUser(url,workaroundTokens=tokens)
        assert user["screen_name"]=="jack"
        assert user["id"]==12
        assert user["created_at"] == "Tue Mar 21 20:50:14 +0000 2006"

def test_videoTweetExtract():
    tweet = twExtract.extractStatus(testVideoTweet,workaroundTokens=tokens)
    assert tweet["full_text"]==videoVNF_compare['description']
    assert tweet["user"]["screen_name"]==twitterAccountName
    assert 'extended_entities' in tweet
    assert len(tweet['extended_entities']["media"])==1
    video = tweet['extended_entities']["media"][0]
    assert video["media_url_https"]=="https://pbs.twimg.com/media/EYeX7akWsAIP1_1.jpg"
    assert video["type"]=="video"
    

def test_mediaTweetExtract():
    tweet = twExtract.extractStatus(testMediaTweet,workaroundTokens=tokens)
    assert tweet["full_text"]==testMedia_compare['description']
    assert tweet["user"]["screen_name"]==twitterAccountName
    assert 'extended_entities' in tweet
    assert len(tweet['extended_entities']["media"])==1
    video = tweet['extended_entities']["media"][0]
    assert video["media_url_https"]=="https://pbs.twimg.com/media/D4TS4xeX4AA02DI.jpg"
    assert video["type"]=="photo"
    

def test_multimediaTweetExtract():
    tweet = twExtract.extractStatus(testMultiMediaTweet,workaroundTokens=tokens)
    assert tweet["full_text"][:94]==testMultiMedia_compare['description'][:94]
    assert tweet["user"]["screen_name"]==twitterAccountName
    assert 'extended_entities' in tweet
    assert len(tweet['extended_entities']["media"])==4
    video = tweet['extended_entities']["media"][0]
    assert video["media_url_https"]=="https://pbs.twimg.com/media/EARxm9FXYAA8qqz.jpg"
    assert video["type"]=="photo"
    video = tweet['extended_entities']["media"][1]
    assert video["media_url_https"]=="https://pbs.twimg.com/media/EARxm9GW4AEnQkp.jpg"
    assert video["type"]=="photo"

def test_pollTweetExtract():
    tweet = twExtract.extractStatus("https://twitter.com/norm/status/651169346518056960",workaroundTokens=tokens)
    assert 'card' in tweet
    compareDict(testPoll_comparePoll,tweet['card'])

def test_NSFW_TweetExtract():
    tweet = twExtract.extractStatus(testNSFWTweet,workaroundTokens=tokens) # For now just test that there's no error

## VNF conversion test ##
def test_textTweetVNF():
    vnf = twitfix.link_to_vnf_from_unofficial_api(testTextTweet)
    compareDict(textVNF_compare,vnf)

def test_videoTweetVNF():
    vnf = twitfix.link_to_vnf_from_unofficial_api(testVideoTweet)
    
    compareDict(videoVNF_compare,vnf)

def test_mediaTweetVNF():
    vnf = twitfix.link_to_vnf_from_unofficial_api(testMediaTweet)
    compareDict(testMedia_compare,vnf)

def test_multimediaTweetVNF():
    vnf = twitfix.link_to_vnf_from_unofficial_api(testMultiMediaTweet)
    compareDict(testMultiMedia_compare,vnf)

def test_pollTweetVNF():
    vnf = twitfix.link_to_vnf_from_unofficial_api(testPollTweet)
    compareDict(testPoll_comparePollVNF,vnf['poll'])

def test_qrtTweet():
    cache.clearCache()
    # this is an incredibly lazy test, todo: improve it in the future
    resp = client.get(testQRTTweet.replace("https://twitter.com",""),headers={"User-Agent":"test"})
    assert resp.status_code==200
    assert "Twitter says I have 382 followers" in str(resp.data)
    # test qrt-ception
    resp = client.get(testQrtCeptionTweet.replace("https://twitter.com",""),headers={"User-Agent":"test"}) # get top level tweet
    assert resp.status_code==200
    assert "Please retweet this to spread awareness for retweets" in str(resp.data)
    qtd_tweet=cache.getVnfFromLinkCache("https://twitter.com/EliLanger/status/585253161260216320") # check that the quoted tweet for the top level tweet is cached
    assert qtd_tweet is not None
    assert qtd_tweet["qrtURL"] is not None # check that the quoted tweet for the top level tweet has a qrtURL
    assert cache.getVnfFromLinkCache("https://twitter.com/EliLanger/status/313143446842007553") is None # check that the bottom level tweet has NOT been cached
    resp = client.get("/EliLanger/status/585253161260216320",headers={"User-Agent":"test"}) # get mid level tweet
    assert resp.status_code==200
    assert cache.getVnfFromLinkCache("https://twitter.com/EliLanger/status/313143446842007553") is not None # check that the bottom level tweet has been cached now

def test_qrtVideoTweet():
    cache.clearCache()
    # this is an incredibly lazy test, todo: improve it in the future
    resp = client.get(testQrtVideoTweet.replace("https://twitter.com",""),headers={"User-Agent":"test"})
    assert resp.status_code==200
    assert "twitter:player:stream\" content=\"https://video.twimg.com/tweet_video/FL0gdK8WUAIHHKa.mp4" in str(resp.data)

## Test adding to cache ; cache should be empty ##
def test_addToCache():
    cache.clearCache()
    twitfix.vnfFromCacheOrDL(testTextTweet)
    twitfix.vnfFromCacheOrDL(testVideoTweet)
    twitfix.vnfFromCacheOrDL(testMediaTweet)
    twitfix.vnfFromCacheOrDL(testMultiMediaTweet)
    #retrieve
    compareDict(textVNF_compare,cache.getVnfFromLinkCache(testTextTweet))
    compareDict(videoVNF_compare,cache.getVnfFromLinkCache(testVideoTweet))
    compareDict(testMedia_compare,cache.getVnfFromLinkCache(testMediaTweet))
    compareDict(testMultiMedia_compare,cache.getVnfFromLinkCache(testMultiMediaTweet))
    cache.clearCache()

def test_embedFromScratch():
    cache.clearCache()
    client.get(testTextTweet.replace("https://twitter.com",""),headers={"User-Agent":"test"})
    client.get(testVideoTweet.replace("https://twitter.com",""),headers={"User-Agent":"test"})
    client.get(testMediaTweet.replace("https://twitter.com",""),headers={"User-Agent":"test"})
    client.get(testMultiMediaTweet.replace("https://twitter.com",""),headers={"User-Agent":"test"})

def test_embedFromCache():
    cache.clearCache()
    twitfix.vnfFromCacheOrDL(testTextTweet)
    twitfix.vnfFromCacheOrDL(testVideoTweet)
    twitfix.vnfFromCacheOrDL(testMediaTweet)
    twitfix.vnfFromCacheOrDL(testMultiMediaTweet)
    #embed time
    resp = client.get(testTextTweet.replace("https://twitter.com",""),headers={"User-Agent":"test"})
    assert resp.status_code==200
    resp = client.get(testVideoTweet.replace("https://twitter.com",""),headers={"User-Agent":"test"})
    assert resp.status_code==200
    resp = client.get(testMediaTweet.replace("https://twitter.com",""),headers={"User-Agent":"test"})
    assert resp.status_code==200
    resp = client.get(testMultiMediaTweet.replace("https://twitter.com",""),headers={"User-Agent":"test"})
    assert resp.status_code==200

def test_embedSuggestive():
    resp = client.get(testNSFWTweet.replace("https://twitter.com",""),headers={"User-Agent":"test"})
    assert resp.status_code==200
    assert "so i had a bot generate it for me" in str(resp.data)
    assert "FfF_gKwXgAIpnpD" in str(resp.data)

def test_veryLongEmbed():
    cache.clearCache()
    cache.setCache({'https://twitter.com/TEST/status/1234':
                    {"description":"A"*1024,"hits":0,"images":["","","","",""],"likes":1234,"nsfw":False,"pfp":"","qrt":{},"rts":1234,"screen_name":"TEST","thumbnail":"","time":"","tweet":"https://twitter.com/TEST/status/1234","type":"Text","uploader":"Test","url":""}
                    })
    resp = client.get('https://twitter.com/TEST/status/1234'.replace("https://twitter.com",""),headers={"User-Agent":"test"})
    assert resp.status_code==200

def test_embedFromOutdatedCache(): # presets a cache that has VNF's with missing fields; there's probably a better way to do this
    cache.setCache({"https://twitter.com/Twitter/status/1118295916874739714":{"description":"On profile pages, we used to only show someone’s replies, not the original Tweet 🙄 Now we’re showing both so you can follow the conversation more easily! https://t.co/LSBEZYFqmY","hits":0,"images":["https://pbs.twimg.com/media/D4TS4xeX4AA02DI.jpg","","","","1"],"likes":5033,"nsfw":False,"pfp":"https://pbs.twimg.com/profile_images/1488548719062654976/u6qfBBkF_normal.jpg","qrt":{},"rts":754,"screen_name":twitterAccountName,"thumbnail":"https://pbs.twimg.com/media/D4TS4xeX4AA02DI.jpg","time":"Tue Apr 16 23:31:38 +0000 2019","tweet":"https://twitter.com/Twitter/status/1118295916874739714","type":"Image","uploader":twitterAccountName,"url":""},
            "https://twitter.com/Twitter/status/1263145271946551300":{"description":"Testing, testing...\n\nA new way to have a convo with exactly who you want. We’re starting with a small % globally, so keep your 👀 out to see it in action. https://t.co/pV53mvjAVT","hits":0,"images":["","","","",""],"likes":61584,"nsfw":False,"pfp":"https://pbs.twimg.com/profile_images/1488548719062654976/u6qfBBkF_normal.jpg","qrt":{},"rts":17138,"screen_name":twitterAccountName,"thumbnail":"https://pbs.twimg.com/media/EYeX7akWsAIP1_1.jpg","time":"Wed May 20 16:31:15 +0000 2020","tweet":"https://twitter.com/Twitter/status/1263145271946551300","type":"Video","uploader":twitterAccountName,"url":"https://video.twimg.com/amplify_video/1263145212760805376/vid/1280x720/9jous8HM0_duxL0w.mp4?tag=13"},
            #"https://twitter.com/Twitter/status/1293239745695211520":{"description":"We tested, you Tweeted, and now we’re rolling it out to everyone! https://t.co/w6Q3Q6DiKz","hits":0,"images":["https://pbs.twimg.com/media/EfJ-C-JU0AAQL_C.jpg","https://pbs.twimg.com/media/EfJ-aHlU0AAU1kq.jpg","","","2"],"likes":5707,"nsfw":False,"pfp":"https://pbs.twimg.com/profile_images/1488548719062654976/u6qfBBkF_normal.jpg","qrt":{},"rts":1416,"screen_name":"Twitter","thumbnail":"https://pbs.twimg.com/media/EfJ-C-JU0AAQL_C.jpg","time":"Tue Aug 11 17:35:57 +0000 2020","tweet":"https://twitter.com/Twitter/status/1293239745695211520","type":"Image","uploader":"Twitter","url":""},
            "https://twitter.com/jack/status/20":{"description":"just setting up my twttr","hits":0,"images":["","","","",""],"likes":179863,"nsfw":False,"pfp":"https://pbs.twimg.com/profile_images/1115644092329758721/AFjOr-K8_normal.jpg","qrt":{},"rts":122021,"screen_name":"jack","thumbnail":"","time":"Tue Mar 21 20:50:14 +0000 2006","tweet":"https://twitter.com/jack/status/20","type":"Text","uploader":"jack","url":""},
            testQrtVideoTweet:{'tweet': 'https://twitter.com/Twitter/status/1494436688554344449', 'url': '', 'description': 'https://twitter.com/TwitterSupport/status/1494386367467593737', 'thumbnail': '', 'uploader': twitterAccountName, 'screen_name': twitterAccountName, 'pfp': 'https://pbs.twimg.com/profile_images/1488548719062654976/u6qfBBkF_normal.jpg', 'type': 'Text', 'images': ['', '', '', '', ''], 'likes': 5186, 'rts': 703, 'time': 'Thu Feb 17 22:20:46 +0000 2022', 'qrt': {'desc': 'Keep your fave DM convos easily accessible by pinning them! You can now pin up to six conversations that will stay at the top of your DM inbox.\n\nAvailable on Android, iOS, and web. https://t.co/kIjlzf9XLJ', 'handle': 'Twitter Support', 'screen_name': 'TwitterSupport', 'verified': True, 'id': '1494386367467593737'}, 'nsfw': False, 'verified': True, 'size': {}}
            })
    #embed time
    resp = client.get(testTextTweet.replace("https://twitter.com",""),headers={"User-Agent":"test"})
    assert resp.status_code==200
    resp = client.get(testVideoTweet.replace("https://twitter.com",""),headers={"User-Agent":"test"})
    assert resp.status_code==200
    resp = client.get(testMediaTweet.replace("https://twitter.com",""),headers={"User-Agent":"test"})
    assert resp.status_code==200
    resp = client.get(testMultiMediaTweet.replace("https://twitter.com",""),headers={"User-Agent":"test"})
    assert resp.status_code==200
    # qrt
    resp = client.get(testQrtVideoTweet.replace("https://twitter.com",""),headers={"User-Agent":"test"})
    assert resp.status_code==200
    assert "twitter:player:stream\" content=\"https://video.twimg.com/tweet_video/FL0gdK8WUAIHHKa.mp4" in str(resp.data)


def test_directEmbed():
    resp = client.get(testVideoTweet.replace("https://twitter.com","")+".mp4",headers={"User-Agent":"test"})
    assert resp.status_code==200
    assert videoVNF_compare["url"] in str(resp.data)

def test_message404():
    resp = client.get("https://twitter.com/jack/status/12345",headers={"User-Agent":"test"})
    assert resp.status_code==200
    assert "Failed to scan your link!" in str(resp.data)

def test_combine():
    twt,e = twitfix.vnfFromCacheOrDL(testMultiMediaTweet)
    img1 = twt["images"][0]
    img2 = twt["images"][1]
    resp = client.get(f"/rendercombined.jpg?imgs={img1},{img2}",headers={"User-Agent":"test"})
    assert resp.status_code==200
    assert resp.headers["Content-Type"]=="image/jpeg"
    assert len(resp.data)>1000

def test_calcSyndicationToken():
    assert twExtract.calcSyndicationToken("1691389765483200513") == "43lnobuxzql"