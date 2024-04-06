import requests


def tts_request(msg, eid, lid, vid, fx=None, fx_level=None):
    headers = {
        'authority': 'cache-a.oddcast.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'range': 'bytes=0-',
        'referer': 'https://l-www.vocalware.com/',
        'sec-ch-ua': '"Not?A_Brand";v="99", "Opera GX";v="97", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'audio',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 OPR/97.0.0.0',
    }
    params = {
        'EID': eid,
        'LID': lid,
        'VID': vid,
        'TXT': msg,
        'IS_UTF8': '1',
        'FX_TYPE': fx,
        'FX_LEVEL': fx_level,
        'ACC': '3314795',
        'API': '2292376',
        'CB': 'vw_mc.vwCallback',
        'HTTP_ERR': '1',
        'vwApiVersion': '2',
        'd': '39e416bbed6bbed265c918e13a215cbb1fafc39e41',
    }

    response = requests.get('https://cache-a.oddcast.com/tts/gen.php', params=params, headers=headers)
    with open("./tts/message.mp3", "wb") as f:
        f.write(response.content)
