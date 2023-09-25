import json
import os

if ('RUNNING_SERVERLESS' in os.environ and os.environ['RUNNING_SERVERLESS'] == '1'): # pragma: no cover
    config = {
            "config":{
                "link_cache":os.getenv("VXX_LINK_CACHE","none"),
                "database":os.getenv("VXX_DATABASE",""),
                "table":os.getenv("VXX_CACHE_TABLE",""),
                "color":os.getenv("VXX_COLOR",""), 
                "appname": os.getenv("VXX_APP_NAME","vxX"), 
                "repo": os.getenv("VXX_REPO","https://github.com/arzolath/BetterXFix"), 
                "url": os.getenv("VXX_URL","https://vxx.com"),
                "combination_method": os.getenv("VXX_COMBINATION_METHOD","local"), # can either be 'local' or a URL to a server handling requests in the same format
                "gifConvertAPI":os.getenv("VXX_GIF_CONVERT_API",""),
                "workaroundTokens":os.getenv("VXX_WORKAROUND_TOKENS",None)
            }
        }
else:
    # Read config from config.json. If it does not exist, create new.
    if not os.path.exists("config.json"):
        with open("config.json", "w") as outfile:
            default_config = {
                "config":{
                    "link_cache":"json",
                    "database":"[url to mongo database goes here]",
                    "table":"TwiFix",
                    "color":"#43B581", 
                    "appname": "vxX", 
                    "repo": "https://github.com/arzolath/BetterXFix", 
                    "url": "https://vxx.com",
                    "combination_method": "local", # can either be 'local' or a URL to a server handling requests in the same format
                    "gifConvertAPI":"",
                    "workaroundTokens":None
                }
            }

            json.dump(default_config, outfile, indent=4, sort_keys=True)

        config = default_config
    else:
        f = open("config.json")
        config = json.load(f)
        f.close()
