import interactions
from LyricsParser import *

app = interactions.Client("토큰")

@app.command(name="검색", description="음악을 검색합니다.")
async def search_music(ctx: interactions.CommandContext, music, artist = ""):
    try:
        d = search(music, artist=artist)
    except Exception as e:
        return await ctx.send(
            embeds=[interactions.Embed(title="오류가 발생했습니다.", description=f"{e}")],
            ephemeral=True
        )

    return await ctx.send(d, ephemeral=True)

@app.command(name="가사", description="가사를 검색합니다.")
async def search_lyrics(ctx: interactions.CommandContext, music, artist = ""):
    try:
        d = get_lyrics(music, artist=artist)
    except Exception as e:
        return await ctx.send(
            embeds=[interactions.Embed(title="오류가 발생했습니다.", description=f"{e}")],
            ephemeral=True
        )
    return await ctx.send(
        embeds=[interactions.Embed(title="검색 성공", description=f"```\n{d['lyrics']}\n```")]
    )

app.start()
