import tweepy

class Twitter:
    cfg = { 
        "consumer_key"        : "SIaSk1mapfSoiih9rTpj3leVw",
        "consumer_secret"     : "aN5r0pU7UGlkIyb9IDkpS3Gggvp7sllXO8VDtOCGZCrfcOEGAf",
        "access_token"        : "602970493-r4zEQYzhshRhuQ9qzjJ7FULOi12NEb0CkDxBnqhS",
        "access_token_secret" : "2Sm4xBD8zRp2K3RnnNdZBInLnQeJ43PUX9iWEZVNxQUMz" 
    }

    def get_api(self, cfg):
        auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
        auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
        return tweepy.API(auth)

    def enviar_tweet(self, texto):
        api = self.get_api(Twitter.cfg)
        api.update_status(status=texto) 
