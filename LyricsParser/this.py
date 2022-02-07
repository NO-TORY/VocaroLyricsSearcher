import requests, re, html

from typing import Optional, Any

def search(*song: Any, artist: Optional[str] = ""):
    response = requests.get("https://www.google.com/search?q={}+site%3Avocaro.wikidot.com".format(str(*song) + artist))
    s = re.findall(r"http://vocaro.wikidot.com/.*", html.unescape(response.text))
    return s[0][0:s[0].index("&")]

def get_lyrics(*song: Any, indents: Optional[int] = 1, artist: Optional[str] = ""):
    song_url = search(*song, artist=artist)

    lyrics = requests.get(song_url).text
    lyrics = html.unescape(lyrics)

    d = re.findall(r"<td>.*", lyrics)
    s = ("\n"*indents).join(d)
    s = re.sub(r"(<td>)|(</td>)", "", s)
    s = s.replace("<span class=\"rt\">", "(")
    s = s.replace("</span></span>", ")")
    s = s.replace("<span class=\"ruby\">", "")
    s = re.sub(r"(<a class.*)|(<a href.*)", "", s)
    return {
        "vocaloid": re.sub(r"(<a href=\".*\">)|(</a>)|(<td>)|(</td>)", "", d[3]),
        "original_url": re.sub(r"(target.*)", "", d[0].split("href=")[1].replace("\"", "")),
        "lyrics": s.lstrip().rstrip()
    }
