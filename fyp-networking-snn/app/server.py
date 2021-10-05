import asyncio
import websockets
from jsonrpcserver import method, async_dispatch as dispatch

from comparator import positive_comparator, negative_comparator

@method
async def comparator(temp, fireThreshold):
    print('Comparator called')
    if positive_comparator(temp, fireThreshold, clone_to_pcm=False,tref=3):
        return 'Positive'
    elif negative_comparator(temp, fireThreshold, clone_to_pcm=False, tref=3):
        return 'Negative'
    else:
        return 'Equal'

@method
async def gradientDetector(side, prevTemp, temp):
    print('Detector called')
    if side == 'Positive':
        if temp > prevTemp + 0.01:
            return True
    elif side == 'Negative':
        if temp < prevTemp - 0.01:
            return True
    return False

async def main(websocket, path):
    while True:
        response = await dispatch(await websocket.recv())
        if response.wanted:
            await websocket.send(str(response))


start_server = websockets.serve(main, "192.168.0.103", 8080)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
