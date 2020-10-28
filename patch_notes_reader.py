""" 

file: patch_notes_reader.py
language: python3
author: Shantanav Saurav << ss9415@g.rit.edu >>
purpose: Read patch notes from given patch

"""
import requests, re, patch_url_scraper, sys, read_file
from bs4 import BeautifulSoup


def get_notes_info(url: str) -> None:
    """
    Get info from one particular set of patch notes
    ----Pre Conditions:
    link -> str: Patch to be read
    ----Post Conditions:
    return -> None
    """
    try:
        notes = requests.get(url)
    except Exception:
        print("There was an error establishing a connection to the provided URL.")
    soup = BeautifulSoup(notes.text, 'html.parser')
    article_title = soup.find('h1', {'class' : 'article-title'}).text.strip()
    blockquote = soup.find('blockquote')
    summary = str()
    try:
        summary = blockquote.text.split("\n")
        summary = " ".join([i.strip() for i in summary])
        summary = summary.strip()
    except Exception:
        pass
    video = soup.find('iframe', allowfullscreen=True)
    if video is not None:
        video = "https://" + video['src'].split("//")[1]
    else:
        video = ''
    image = ''
    try:
        image = soup.find('div', {'class' : 'file-image'}).find('a')['href']
    except Exception:
        pass
    return url, article_title, summary, video, image


def main() -> None:
    """
    Main Function
    ----Pre/Post:
    N/A
    """
    urls = read_file.read_file("urls.txt")
    try:
        get_notes_info(urls[sys.argv[1].lower()])
    except KeyError:
        print("That patch does not exist on the na.leagueoflegends.com website.")
        most_recent = str()
        with open("urls.txt") as f:
            most_recent = f.readline().strip().split(": ")[0]
        print("The oldest patch available is Patch 3.04, and the newest patch is Patch " + most_recent)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: patch_notes_reader.py <patch number>")
    else:
        if re.search(r"^[\d]{1,2}\.[\d]{1,2}[\w]?([-][tT][fF][tT])?$", sys.argv[1]):
            main()
        else:
            print("Please enter a valid patch number.")

