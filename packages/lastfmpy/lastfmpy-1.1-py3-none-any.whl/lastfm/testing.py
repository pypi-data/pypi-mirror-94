import asyncio

import client


async def main():
    lastfm = await client.LastFM("4ad3e555ae85bc63dc2551656a21766c")
    tracks = await lastfm.artist.get_top_tracks(artist="blackpink")
    for track in tracks:
        print(track.name)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
