import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.colors as allowedcolors
import json
import os
import requests
import threading
import hashlib
import datetime

filterlists = json.loads(open('filterlists.json').read())

current_date = datetime.datetime.now().strftime("%d/%m/%Y")

def dict_as_arr(dic):
    """
    Return the items in a dict as a list (called an array here, don't sue me)
    I am sure there is a better way
    """
    arr = []
    for item in dic:
        arr.append(dic[item])
    return arr

try:
    os.mkdir("stats")
except:
    pass

try:
    os.mkdir("size_stats")
except:
    pass

try:
    stats = json.loads(open('stats.json', 'r', encoding='utf-8').read())
except:
    stats = {}

try:
    change_stats = json.loads(open("change_stats.json", 'r').read())
except:
    change_stats = {
    }

try:
    size_stats = json.loads(open("size_stats.json", 'r').read())
except:
    size_stats = {
    }

running_threads = 0

def count_filters(filter, trust_line_count=False, exclude_from_line_count=0):
    global stats
    global running_threads
    global change_stats
    global size_stats
    running_threads += 1
    try:
        freq = requests.get(filterlists[filter])
        fhash = hashlib.md5(freq.content).hexdigest()
        fcontents = freq.text.replace("\r\n", "\n").split("\n")
        if filter not in stats:
            stats[filter] = {}
        if filter not in change_stats:
            change_stats[filter] = {}
        if filter not in size_stats:
            size_stats[filter] = {}
        change_stats[filter][current_date] = fhash
        size_stats[filter][current_date] = len(freq.content)
        numfilters = 0
        done = []
        if trust_line_count:
            numfilters = len(fcontents) - exclude_from_line_count
        else:
            for l in fcontents:
                if l == "" or l.startswith("#") or l.startswith("!") or l in done:
                    continue
                done.append(l)
                numfilters += 1
        stats[filter][current_date] = numfilters
    except Exception as err:
        print(err)
    running_threads -= 1
    print(f"[{datetime.datetime.now()}] {filter} complete")
"""
for these lists, the script does not go through every filter
instead, it just checks the line count and subtracts the number of comments/empty lines listed below
this is for large lists who only have comments in their header
"""

trust_lines = {
    "1Hosts Mini": 18,
    "HaGeZi's Light DNS Blocklist": 11,
    "HaGeZi's Normal DNS Blocklist": 11,
    "HaGeZi's Pro DNS Blocklist": 11,
    "HaGeZi's Pro mini DNS/Browser Blocklist": 12,
    "HaGeZi's Pro++ DNS Blocklist": 11,
    "HaGeZi's Pro++ mini DNS/Browser Blocklist": 12,
    "HaGeZi's Ultimate DNS Blocklist": 11,
    "HaGeZi's Ultimate mini DNS/Browser Blocklist": 12,
    "HaGeZi's Fake DNS Blocklist": 11,
    "HaGeZi's Pop-Up Ads DNS Blocklist": 11,
    "HaGeZi's NRD 10 DNS Blocklist": 11,
    "HaGeZi's NRD 30 DNS Blocklist": 11,
    "HaGeZi's Encrypted DNS/VPN/TOR/Proxy Bypass DNS Blocklist": 11,
    "HaGeZi's Encrypted DNS Bypass DNS Blocklist": 11,
    "HaGeZi's Threat Intelligence Feeds DNS Blocklist": 11,
    "HaGeZi's safesearch not supported DNS Blocklist": 11,
    "HaGeZi's DynDNS Blocklist": 11,
    "HaGeZi's Badware Hoster DNS Blocklist": 11,
    "HaGeZi's Anti-Piracy DNS Blocklist": 11,
    "HaGeZi's Gambling DNS Blocklist": 11,
    "HaGeZi's Amazon Tracker DNS Blocklist": 11,
    "HaGeZi's Apple Tracker DNS Blocklist": 11,
    "HaGeZi's Huawei Tracker DNS Blocklist": 11,
    "HaGeZi's Windows/Office Tracker DNS Blocklist": 11,
    "HaGeZi's TikTok Fingerprinting DNS Blocklist": 11,
    "HaGeZi's TikTok Extended Fingerprinting DNS Blocklist": 11,
    "HaGeZi's LG webOS Tracker DNS Blocklist": 11,
    "HaGeZi's Vivo Tracker DNS Blocklist": 11,
    "HaGeZi's OPPO & Realme Tracker DNS Blocklist": 11,
    "HaGeZi's Xiaomi Tracker DNS Blocklist": 11,
    "HaGeZi's Threat Intelligence Feeds - IPs": 0,
    "HaGeZi's Threat Intelligence Feeds DNS Blocklist - medium version": 11,
    "Peter Lowe's Ad and tracking server list": 14,
    "OISD Small": 12,
    "OISD Big": 12,
    "OISD NSFW": 12,
    "(Unofficial) Emerging Threats PiHole blocklist": 60,
    "(Unofficial) Emerging Threats Blocklist (jarelllama)": 62,
    "The Block List Project - Everything List": 16,
    "The Block List Project - Ads List": 15,
    "The Block List Project - Abuse List": 15,
    "The Block List Project - Crypto List": 15,
    "The Block List Project - Drugs List": 15,
    "The Block List Project - Fraud List": 19,
    "The Block List Project - Gambling List": 15,
    "The Block List Project - Malware List": 27,
    
}

for filter in filterlists:
    if filter not in trust_lines:
        trust_lines[filter] = -1
    print(f"[{datetime.datetime.now()}] Looking at {filter} (trust lines {trust_lines[filter]})")
    threading.Thread(target=count_filters, args=(filter, trust_lines[filter] != -1, trust_lines[filter])).start()

while running_threads > 0:
    pass

for filter in stats:
    filter_items = dict_as_arr(stats[filter])
    x = np.arange(1,len(filter_items) + 1)
    y = np.array(filter_items)

    filtername = filter.replace(" ","_").replace("'","").replace("+","_").replace(":", "").replace("*", "").replace("&", "_").replace("/","_")
    plt.title(f"Number of unique filters in {filter.replace('(clean version, domains only)','')}")
    plt.xlabel("Time")
    plt.ylabel("Filters")
    plt.plot(x, y, color ="green")
    plt.savefig(f"stats/{filtername}.png")
    plt.clf()

for filter in size_stats:
    filter_items = dict_as_arr(size_stats[filter])
    x = np.arange(1,len(filter_items) + 1)
    y = np.array(filter_items)

    filtername = filter.replace(" ","_").replace("'","").replace("+","_").replace(":", "").replace("*", "").replace("&", "_").replace("/","_")
    plt.title(f"Size (in bytes) of {filter}")
    plt.xlabel("Time")
    plt.ylabel("Size")
    plt.plot(x, y, color ="green")
    plt.savefig(f"size_stats/{filtername}.png")
    plt.clf()

try:
    outstats = open("stats.json", 'w')
    outstats.write(json.dumps(stats))
    outstats.close()
except Exception as err:
    print(err)

try:
    outstats = open("change_stats.json", 'w')
    outstats.write(json.dumps(change_stats))
    outstats.close()
except Exception as err:
    print(err)

try:
    outstats = open("size_stats.json", 'w')
    outstats.write(json.dumps(size_stats))
    outstats.close()
except Exception as err:
    print(err)

