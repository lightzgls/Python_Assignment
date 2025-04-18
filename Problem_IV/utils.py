import pandas as pd
import unicodedata
from rapidfuzz import process, fuzz

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
def match_name(name, choices, threshold=75):
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

# Then merge using (for example) the original "Player" column, or merge based on best fuzzy matches.
# One way is to add a column with the best match from df1:
def get_best_match(name, choices, threshold=75):
    match, score, _ = process.extractOne(name, choices, scorer=fuzz.token_sort_ratio)
    if score >= threshold:
        return match
    return None
import unicodedata
import pandas as pd

def normalize_name(name: str) -> str:
    """
    Normalize a string by removing diacritics and converting to lower case.
    """
    if not isinstance(name, str):
        return ""
    # Normalize Unicode and remove diacritics
    normalized = unicodedata.normalize('NFKD', name)
    normalized = "".join(c for c in normalized if not unicodedata.combining(c))
    return normalized.lower().strip()


# Example usage:
# compare_player_names_in_dfs(compare_df, result_df)