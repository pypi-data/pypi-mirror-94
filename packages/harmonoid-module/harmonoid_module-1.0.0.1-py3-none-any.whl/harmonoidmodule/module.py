from .harmonoidservice import HarmonoidService
import json
import time

harmonoidService = HarmonoidService()

async def fetchJS():
    await harmonoidService.ytMusic.youtube.getJS()


def returnResponse(response):
    if type(response) is dict:
        return json.dumps(response, indent=4)
    return response


async def searchYoutube(keyword, mode="album"):
    result = await harmonoidService.searchYoutube(keyword, mode)
    return returnResponse(result)


async def albumInfo(albumId):
    result = await harmonoidService.albumInfo(albumId)
    return returnResponse(result)


async def trackInfo(trackId, albumId=None):
    result = await harmonoidService.trackInfo(trackId, albumId)
    return returnResponse(result)


async def artistInfo(artistId):
    result = await harmonoidService.artistInfo(artistId)
    return returnResponse(result)


async def artistTracks(artistId):
    result = await harmonoidService.artistTracks(artistId)
    return returnResponse(result)

async def getLyrics(trackId=None, trackName=None):
    if not any((trackId, trackName)):
        raise Exception("Neither trackId nor trackName is specified")
    if trackId and trackName:
        raise Exception("Both trackId and trackName is specified")
    result = await harmonoidService.getLyrics(trackId, trackName)
    return returnResponse(result)

async def trackDownload(trackId=None, albumId=None, trackName=None):
    if not any((trackId, trackName)):
        raise Exception("Neither trackId nor trackName is specified")
    if trackId and trackName:
        raise Exception("Both trackId and trackName is specified")
    return await harmonoidService.trackDownload(trackId, albumId, trackName)

async def test(trackName="NoCopyrightedSounds", albumName="NoCopyrightedSounds", artistName="NoCopyrightedSounds", trackDownloadName="NoCopyrightedSounds", lyricsTrackId="Kx7B-XvmFtE"):
    startTime = time.time()
    startLt = time.ctime(startTime)
    print("[test] Testing /search&mode=track")
    try:
        response = await searchYoutube(trackName, "track")
        tracks = json.loads(response["body"])["result"]
        if len(tracks) != 0 and tracks[0]["trackId"]:
            trackSearchTest = True
        else:
            trackSearchTest = False
    except Exception as e:
        trackSearchTest = False
        print(f"[test] Exception: {e}")

    print("[test] Testing /trackInfo")
    try:
        response = await trackInfo(tracks[0]["trackId"])
        tracks = json.loads(response["body"])
        if len(tracks) != 0 and tracks["trackId"]:
            trackInfoTest = True
        else:
            trackInfoTest = False
    except Exception as e:
        trackInfoTest = False
        print(f"[test] Exception: {e}")

    print("[test] Testing /search&mode=album")
    try:
        response = await searchYoutube(albumName, "album")
        albums = json.loads(response["body"])["result"]
        if len(albums) != 0 and albums[0]["albumId"]:
            albumSearchTest = True
        else:
            albumSearchTest = False
    except Exception as e:
        albumSearchTest = False
        print(f"[test] Exception: {e}")

    print("[test] Testing /albumInfo")
    try:
        response = await albumInfo(albums[0]["albumId"])
        albums = json.loads(response["body"])
        if len(albums) != 0 and (albums["tracks"][0]["trackId"]):
            albumInfoTest = True
        else:
            albumInfoTest = False
    except Exception as e:
        albumInfoTest = False
        print(f"[test] Exception: {e}")
    
    print("[test] Testing /search&mode=artist")
    try:
        response = await searchYoutube(artistName, "artist")
        artists = json.loads(response["body"])["result"]
        if len(artists) != 0 and artists[0]["artistId"]:
            artistSearchTest = True
        else:
            artistSearchTest = False
    except Exception as e:
        artistSearchTest = False
        print(f"[test] Exception: {e}")

    print("[test] Testing /artistInfo")
    try:
        response = await artistInfo(artists[0]["artistId"])
        artists = json.loads(response["body"])
        if len(artists) != 0 and artists["description"]:
            artistInfoTest = True
        else:
            artistInfoTest = False
    except Exception as e:
        artistInfoTest = False
        print(f"[test] Exception: {e}")
        
    print("[test] Testing /lyrics")
    try:
        response = await getLyrics(lyricsTrackId, None)
        lyrics = json.loads(response["body"])
        if len(lyrics) != 0 and lyrics["lyrics"]:
            lyricsTest = True
        else:
            lyricsTest = False
    except Exception as e:
        lyricsTest = False
        print(f"[test] Exception: {e}")
    
    print("[test] Testing /trackDownload")
    try:
        response = await harmonoidService.trackDownload(None, None, trackDownloadName)
        statusCode = response.status_code
    except Exception as e:
        statusCode = 500
        print(f"[test] Exception: {e}")
    print(f"[test] Status code: {statusCode}")
    if statusCode != 200:
        trackDownloadTest = False
    else:
        trackDownloadTest = True
    
    if all([trackSearchTest, trackInfoTest, albumSearchTest, albumInfoTest, artistSearchTest, artistInfoTest, lyricsTest, trackDownloadTest]):
        testSuccess = True
    else:
        testSuccess = False
    endTime = time.time()
    endLt = time.ctime(endTime)
    totalTime = endTime - startTime
    response = {
        "endTime": endLt,
        "startTime": startLt,
        "time": totalTime,
        "success": testSuccess,
        "trackSearch": trackSearchTest,
        "trackInfo": trackInfoTest,
        "albumSearch": albumSearchTest,
        "alubmInfo": albumInfoTest,
        "artistSearch": artistSearchTest,
        "artistInfo": artistInfoTest,
        "lyrics": lyricsTest,
        "trackDownload": trackDownloadTest,
    }
    return returnResponse(response)
