
import re
import requests

def external_lookup(player_name, team_name):
    url_api = "https://www.footballtransfers.com/us/search/actions/search"
    suffix = str(player_name) + " " + str(team_name)
    resuffix = re.sub(r'\s', '%20', suffix)
    headers = {
        "referer" : f"https://www.footballtransfers.com/us/search?search_value={resuffix}",
        "x-requested-with" : "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "content-type":"application/x-www-form-urlencoded; charset=UTF-8"
    }
    payload ={
        "search_page" : "1",
        "search_value" : suffix,
        "players" : 1,
        "teams" : 1
    }
    response = requests.post(url=url_api,headers=headers,data=payload)
    data = response.json()
    if data.get("found", 0) > 0 and data.get("hits"):
        # Assumes that the transfer value is in the first hit's document field as "transfer_value"
        transfer_value = data["hits"][0]["document"].get("transfer_value")
        return transfer_value
    return None
