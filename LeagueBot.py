"""

file: LeagueBot.py
language: python3.7
author: Shantanav Saurav
purpose: Main LeagueBot implementation

"""
import discord, os, re
from read_file import read_file
from patch_notes_reader import get_notes_info
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
URLS = read_file("urls.txt")
client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord.')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("?patch "):
        text = message.content.strip()
        length = len(text.split())
        patch = text.split()[1]
        if length == 2:
            if re.search(r"^[\d]{1,2}\.[\d]{1,2}[\w]?([-][tT][fF][tT])?$", patch):
                try:
                    (info, video, image) = build_patch_embed(patch)
                    if image != '':
                        info.set_image(url=image)
                    await message.channel.send(embed=info)
                    if video != '':
                        await message.channel.send("https://www.youtube.com/watch?v=" + re.findall(r"[a-zA-Z0-9_-]{11}", video)[0])
                except KeyError:
                    most_recent = str()
                    with open("urls.txt") as f:
                        most_recent = f.readline().strip().split(": ")[0]
                    await message.channel.send("That patch does not exist on the na.leagueoflegends.com website." + \
                        " The oldest patch available is Patch 3.04, and the newest patch is Patch " + most_recent\
                        + ". \nPlease use `?patch list` to view all available patches.")
                    return
            elif patch == "last":
                most_recent = str()
                with open("urls.txt") as f:
                    most_recent = f.readline().strip().split(": ")[0]
                (info, video, image) = build_patch_embed(most_recent)
                if image != '':
                    info.set_image(url=image)
                await message.channel.send(embed=info)
                if video != '':
                    await message.channel.send("https://www.youtube.com/watch?v=" + re.findall(r"[a-zA-Z0-9_-]{11}", video)[0])
            elif patch == "list":
                info = build_patchlist()
                await message.channel.send(embed=info)
            else:
                await message.channel.send("Please enter a valid patch number. Use `?patch list` to see a list of available patches.")
                return
        elif length == 3:
            print("2nd argument detected: " + text.split()[2])
        else:
            await message.channel.send("Usage: `?patch <patchNumber> {championName}")
            return


def build_patch_embed(patch: str) -> discord.Embed:
    (url, title, summary, video, image) = get_notes_info(URLS[patch.lower()])
    if len(summary) > 1000:
        summary = summary[0:996] + "..."
    info = discord.Embed(title=title, description=summary, url=url, colour=discord.Colour.blue())
    return info, video, image


def build_patchlist() -> discord.Embed:
    """
    Helper Function to on_message:
    Build Patch Info Embed
    ----Pre Conditions:
    N/A
    ----Post Conditions:
    return -> discord.Embed: Embeddable Discord Element
    """
    patch_dct = dict()
    with open("urls.txt") as f:
        for line in f:
            line = line.strip().split(": ")[0]
            if line[-3:].lower() == "tft":
                if 'tft' in patch_dct:
                    patch_dct['tft'] += [line]
                else:
                    patch_dct['tft'] = [line]
            else:
                if "Season " + line[0] in patch_dct:
                    patch_dct["Season " + line[0]] += [line]
                else:
                    patch_dct["Season " + line[0]] = [line]
    info = discord.Embed(title="Patches", description="Here's all the patches I can see:", colour=discord.Colour.blue())
    for key in patch_dct:
        info.add_field(name=key, value="\n".join(patch_dct[key]), inline=True)
    return info


if __name__ == "__main__":
    client.run(TOKEN)
