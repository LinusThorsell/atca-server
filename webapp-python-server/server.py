#!/usr/bin/env python

import asyncio
from websockets import serve
import time
import datetime
import serial

def timestamp():
	timestamp = time.time()
	date_time = datetime.datetime.fromtimestamp(timestamp)
	str_date_time = date_time.strftime("%d/%m %H:%M:%S")
	return str_date_time

CLIENTS = []

async def send(websocket, message):
    try:
        await websocket.send(message)
    except websockets.ConnectionClosed:
        pass

print("Starting server...")

ser = serial.Serial ("/dev/ttyUSB0", 9600)
def sendToAVR(message):
    message_type = message.split(':')[0]
    #print("Message Type: " + message_type)
    
    if (message_type == 'keyspressed'):
        #print("Got 'keyspressed' command, sending to Control Unit")
        ser.write(message.encode());
    
async def sendAll(websocket):
	#print(websocket)
	
	async for message in websocket:
		print(timestamp() + " " + message)
		sendToAVR(message)
		if websocket not in CLIENTS:
			if "[webapp]" in message:
				CLIENTS.append(websocket)
		
		for socket in CLIENTS:
			await send(socket, message)

async def main():
    async with serve(sendAll, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
