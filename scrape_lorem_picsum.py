# ==============================================================================
# About: scrape_lorem_picsum.py
# ==============================================================================
# scrape_lorem_picsum.py is responsible for:
#   - scrapes the picsum.com API for a list of their available photos

# Imports ----------------------------------------------------------------------

import sys
import json
import time
import requests

# Main -------------------------------------------------------------------------

def scrape():
    results = []
    page = 1
    while(True):
        print(f"{page}: {len(results)} results so far")
        old_length = len(results)
        time.sleep(0.25)
        r = requests.get(f"https://picsum.photos/v2/list?page={page}&limit=100")
        if (r.status_code == 200):
            for img in r.json():
                results.append(img)
        else:
            break

        if (len(results) == old_length):
            break
        page += 1

    with open('./input/lorem_picsum.json', 'w') as f:
        json.dump(results, f)
    print('done!')

# Run --------------------------------------------------------------------------

if (__name__ == '__main__'):
    scrape()
