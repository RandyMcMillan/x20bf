import configparser

global AT
global ATS
global CAK
global CASK

config = configparser.ConfigParser()
config.read("configs.ini")
config.sections()
config.get("DEFAULTSECT", "", fallback=False)
config.get("LOGGERDEFAULTS", "", fallback=False)
config.get("USERDEFAULTS", "", fallback=False)


if config.get("[USERDEFAULTS]", "tweet"):
    twitter_api = configparser.ConfigParser()
    twitter_api.read("twitter.ini")
    twitter_api.sections()
    twitter_api.get("TWITTERAPI", "", fallback=0)
    AT = twitter_api.get("[TWITTERAPI]", "access_token")
    ATS = twitter_api.get("[TWITTERAPI]", "access_token_secret")
    CAK = twitter_api.get("[TWITTERAPI]", "consumer_api_key")
    CASK = twitter_api.get("[TWITTERAPI]", "consumer_api_secret_key")
else:
    AT = config.get("[USERDEFAULTS]", "tweet")
    ATS = config.get("[USERDEFAULTS]", "tweet")
    CAK = config.get("[USERDEFAULTS]", "tweet")
    CASK = config.get("[USERDEFAULTS]", "tweet")
