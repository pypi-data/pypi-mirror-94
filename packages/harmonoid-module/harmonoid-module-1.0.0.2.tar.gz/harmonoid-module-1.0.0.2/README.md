# harmonoid-module
A Python wrapper around harmonoid-service server code published to PyPI

Install it from PyPI using `pip install harmonoid-module`

It is perfect for usage in ASGI (asynchronous) applications & is fully asynchronous

## Download song
```
import harmonoidmodule as hm
import asyncio

async def trackDownload(trackName):
    return await hm.trackDownload(trackName=trackName)

loop = asyncio.get_event_loop()
loop.run_until_complete(trackDownload("save your tears"))
loop.close()
```
