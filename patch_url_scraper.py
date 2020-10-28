"""

file: test.py
language: python3.7
author: Shantanav Saurav << ss9415@g.rit.edu >>
purpose: Grab patch notes links from home page 

"""
import requests, re
from bs4 import BeautifulSoup


def get_links() -> tuple:
    """
    Get patch links from Patch homepage
    ----Pre Conditions:
    N/A
    ----Post Conditions:
    return -> tuple(dict, dict): League Patches Dictionary, TFT Patches Dictionary
    """
    homepage = requests.get("https://na.leagueoflegends.com/en/news/game-updates/patch")
    soup = BeautifulSoup(homepage.text, 'html.parser')
    pagerdiv = soup.find('div', {'class': 'pager'})
    alinks = pagerdiv.find_all('a')
    maxpage = alinks[-2].text
    league_links = dict()
    tft_links = dict()
    for pagenum in range(0, int(maxpage)):
        patches = requests.get("https://na.leagueoflegends.com/en/news/game-updates/patch?page=" + str(pagenum))
        soup = BeautifulSoup(patches.text, 'html.parser')
        div = soup.find_all('div', {'class' : 'views-row'})
        h4 = [divider.find_all('h4') for divider in div]
        for h in h4:
            for header in h:
                a = header.find('a', href=True)
                try:
                    if a.text.strip().split()[0] == "Teamfight":
                        tft_links[re.findall(r"[\d]+\.[\d]+[\w]?", a.text)[0] + "-tft"] = "https://na.leagueoflegends.com" + a['href']
                    elif a.text.strip().split()[0] == "Patch" or a.text.strip().split()[0] == "Updated":
                        league_links[re.findall(r"[\d]+\.[\d]+[\w]?", a.text)[0]] = "https://na.leagueoflegends.com" + a['href']
                except Exception:
                    continue

    return league_links, tft_links


if __name__ == "__main__":
    (league_links, tft_links) = get_links()
    for dct in (league_links, tft_links):
        for key in dct:
            print(key + ": " + dct[key])
