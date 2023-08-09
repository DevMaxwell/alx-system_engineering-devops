#!/usr/bin/python3
""" raddit api"""

import json
import requests

def count_words(subreddit, word_list, after="", count=None):
    """Count all words in
    subreddit titles"""

    if count is None:
        count = [0] * len(word_list)

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {'after': after} if after else {}
    headers = {'user-agent': 'bhalut'}

    response = requests.get(url, params=params, allow_redirects=False, headers=headers)

    if response.status_code == 200:
        data = response.json()

        for topic in data['data']['children']:
            title_words = topic['data']['title'].split()
            for word in title_words:
                for i, target_word in enumerate(word_list):
                    if target_word.lower() == word.lower():
                        count[i] += 1

        after = data['data']['after']
        if after is None:
            count_and_sort = sorted(zip(word_list, count), key=lambda x: (-x[1], x[0].lower()))
            save_indices = set()

            for i, (word, cnt) in enumerate(count_and_sort):
                if cnt > 0 and i not in save_indices:
                    print(f"{word.lower()}: {cnt}")
                for j in range(i + 1, len(count_and_sort)):
                    if word.lower() == count_and_sort[j][0].lower():
                        save_indices.add(j)
                        count_and_sort[i] += count_and_sort[j][1]

            for i, (word, cnt) in enumerate(count_and_sort):
                word_list[i], count[i] = word, cnt
        else:
            count_words(subreddit, word_list, after, count)

# Example usage
count_words("example_subreddit", ["word1", "word2", "word3"])
