import tweepy
import json
import csv
import sys


def fetch_tweets(consumer_key=None, consumer_secret=None, access_key=None, access_secret=None, twitter_handle=None):
    '''
    INSERT DOCSTRING HERE
    '''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    all_tweets = []
    new_tweets = api.user_timeline(screen_name=twitter_handle, count=200, tweet_mode='extended')
    print("###### Starting to scrape tweets: ######")
    while(len(new_tweets) > 0):
        all_tweets.extend(new_tweets)
        last_id = all_tweets[-1].id - 1
        new_tweets = api.user_timeline(screen_name=twitter_handle, count=200, max_id=last_id, tweet_mode='extended')
        print("######## %d tweets downloaded ########" % len(all_tweets))
    print("## Maximum possible tweets downloaded ##")
    tweet_data = [[  tweet.id_str, str(tweet.created_at).split(' ')[0], tweet.full_text, tweet.retweet_count, 
                    tweet.lang, tweet.user.id_str, tweet.user.name, tweet.user.screen_name, 
                    tweet.user.followers_count, tweet.user.friends_count, tweet.user.location, 
                    tweet.user.verified ] for tweet in all_tweets]
    return tweet_data


def write_file(tweet_data=None, twitter_handle=None):
    '''
    INSERT DOCSTRING HERE
    '''    
    try:
        print("######## Writing data to file: #########")
        with open(twitter_handle + '_tweets.csv', 'w', encoding='utf8') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(['Tweet ID', 'Date Created', 'Tweet', 'Retweets', 'Language', 'User ID', 
                            'User Name', 'User Twitter Handle', 'Follower Count', 'Friend Count',
                            'Location', 'Verified'])
            writer.writerows(tweet_data)
        print('### ' + twitter_handle + '_tweets.csv created ###')
        return True
    except:
        return False


if __name__ == '__main__':
    with open('twiiter_credentials.json') as cred_data:
        login_info = json.load(cred_data)
    consumer_key = login_info['CONSUMER_KEY']
    consumer_secret = login_info['CONSUMER_SECRET']
    access_key = login_info['ACCESS_KEY']
    access_secret = login_info['ACCESS_SECRET']
    twitter_handle = str(sys.argv[1])

    tweet_data = fetch_tweets(consumer_key=consumer_key, consumer_secret=consumer_secret, access_key=access_key, access_secret=access_secret, twitter_handle=twitter_handle)
    if(write_file(tweet_data=tweet_data, twitter_handle=twitter_handle)):
        with open('twitter_handles.txt', 'a') as f:
            f.writelines(twitter_handle + '\n')
    else:
        print("Something went wrong in getting tweets from " + twitter_handle)