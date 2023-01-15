from flask import request, jsonify
from flask_cors import cross_origin
from . import api
import pickle
import os
import time
import random

def prefix_contains(prefix_str, word_dictionary):
    for word in word_dictionary:
        loc = word.index(prefix_str) if prefix_str in word else -1
        if loc == 0:
            return True
    return False
    
    

def find_words(word, word_dictionary, letters, gold_letter, result_list, start_time):
    # base case 1: we find a word in the dictionary that contains the gold letter
    # we've already pruned words < length of 4 so don't have to check word length
    if time.time() - start_time >= 10:
        return
    
    if word in word_dictionary and gold_letter in word:
        result_list.append(word)
    
    if prefix_contains(word, word_dictionary):
        for letter in letters:
            find_words(word + letter, word_dictionary, letters, gold_letter, result_list, start_time)
        
    else:
        return

@api.route('/solve', methods=['POST', 'OPTIONS'])
@cross_origin()
def solve():
    start_time = time.time()
    req_body = request.json
    
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    
    pkl_url = os.path.join(SITE_ROOT, 'static', 'dictionary.pkl')
    
    with open(pkl_url, "rb") as dict_file:
        word_dictionary = pickle.load(dict_file)
            
    letters = list(req_body['letters'])
    gold_letter = req_body['gold_letter']
    
    words = []
    
    random.shuffle(letters)
    
    find_words("", word_dictionary, letters, gold_letter, result_list=words, start_time=start_time)
    
    return jsonify(words)