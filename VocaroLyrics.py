import requests, regex, html

from typing import Optional, Union
from collections import namedtuple

Lyrics = namedtuple("Lyrics", "lyrics original_url vocaloid")

def search(*song: Union[str, bytes], artist: Optional[str] = ""):
    response = requests.get("https://www.google.com/search?q={}+site%3Avocaro.wikidot.com".format(str(*song) + artist))
    s = regex.findall(r"http://vocaro.wikidot.com/.*", html.unescape(response.text))
    try:
        d = s[0][0:s[0].index("&")]
    except:
        raise TypeError

    if all([k == "http://vocaro.wikidot.com" or k == "http://vocaro.wikidot.com/" for k in s]):
        raise TypeError

    return d

def get_lyrics(*song: Union[str, bytes], indents: Optional[int] = 1, artist: Optional[str] = ""):
    song_url = search(*song, artist=artist)

    lyrics = requests.get(song_url).text
    lyrics = html.unescape(lyrics)

    html_replacements = ("<span style=\"white-space: pre-wrap;\">---", "<span class=\"ruby\">", "---<span>")

    d = regex.findall(r"<td>.*", lyrics)
    s = str("\n"*indents).join(d)
    s = regex.sub(r"(<td>)|(</td>)", "", s)
    s = s.replace("<span class=\"rt\">", "(")
    s = s.replace("</span></span>", ")")
    for r in html_replacements:
        s = s.replace(r, "")
    s = regex.sub(r"(<a class.*)|(<a href.*)", "", s)
    
    return Lyrics(
        s.lstrip().rstrip(),
        regex.sub(r"(target.*)", "", d[0].split("href=")[1].replace("\"", "")), 
        regex.sub(r"(<a href=\".*\">)|(</a>)|(<td>)|(</td>)", "", d[3])
    )   
