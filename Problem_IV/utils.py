
import unicodedata
from rapidfuzz import process, fuzz
import re
import requests

# Example canonical name function (you can adjust as needed)
def canonical_name(name):
    # Normalize Unicode and remove diacritics
    name = unicodedata.normalize('NFKD', name)
    name = "".join([c for c in name if not unicodedata.combining(c)])
    # Lower-case and strip extra spaces
    tokens = name.lower().strip().split()
    if len(tokens) >= 2:
        # Option 1: first and last token, e.g. "manuel urgate ribeiro" -> "manuel ribeiro"
        option1 = tokens[0] + " " + tokens[-1]
        # Option 2: first and second token, e.g. "manuel urgate ribeiro" -> "manuel urgate"
        option2 = tokens[0] + " " + tokens[1]
        # For example, return the one with fewer characters (or choose your preferred rule)
        return option1 if len(option1) <= len(option2) else option2
    return name.lower().strip()



# Define a function to match names using fuzzy matching
def match_name(name, choices, threshold=90):
    # Returns the best match if score is above threshold, else returns None
    match, score, _ = process.extractOne(name, choices, scorer=fuzz.token_sort_ratio)
    if score >= threshold:
        return match
    return None

# Apply fuzzy matching when filtering:
def fuzzy_filter(row, valid_names):
    # Try to match the canonical name from df against the list from df1
    matched = match_name(row["Canonical_Player"], valid_names)
    return matched is not None


def get_best_match(name, choices, threshold=90):
    match, score, _ = process.extractOne(name, choices, scorer=fuzz.token_sort_ratio)
    if score >= threshold:
        return match
    return None


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
    price = response.json()
    data = response.json()
    if data.get("found", 0) > 0 and data.get("hits"):
        # Assumes that the transfer value is in the first hit's document field as "transfer_value"
        transfer_value = data["hits"][0]["document"].get("transfer_value")
        return transfer_value
    return None


