import asyncio

import lastfmpy


async def main():
    lastfm = await lastfmpy.LastFM("4ad3e555ae85bc63dc2551656a21766c")
    artist = await lastfm.artist.get_info(artist="BLACKPINK", username="myerfire")
    print(artist.stats.userplaycount)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
