# VocaroLyricsSearcher
보카로 가사 검색기

# usage
```python
import VocaroLyrics, requests

s = requests.Sesssion()

print(VocaroLyrics.get_lyrics(s, song="animal", artist="deco*27").lyrics)
```
## installation
```shell
pip install VocaroLyrics
```
