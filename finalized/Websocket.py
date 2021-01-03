import threading
import websockets
import asyncio
import json
from Game import Game

import websockets
import asyncio

class SocketManager(object):
    activeConnections = []
    activeGameConnections = []
    gameObject = None
        
    async def sender(self, websocket, path):
        if websocket in self.activeGameConnections:
            await websocket.send(json.dumps(self.gameObject.getInfo()))
            await asyncio.sleep(.05)
        else:
            await websocket.send("hello!")
            await asyncio.sleep(.5)
    
    async def receiver(self, websocket, path):
        async for message in websocket:
            print("Websocket: " + message)
            if message == "game":
                if len(self.activeGameConnections) >= 1:
                    await websocket.send("connection not allowed")
                else:
                    self.activeGameConnections.append(websocket)
                    
            if websocket in self.activeGameConnections:
                if message == "start":
                    self.gameObject.enableGun()
                    self.gameObject.reset()
                    
                elif message == "waiting for hit":
                    self.gameObject.startHit()
                    
                elif message == "clear targets":
                    self.gameObject.clearTargets()
                    
                elif "playername" in message:
                    self.gameObject.setPlayerName(message.replace("playername ", ""))
                
            if message == "__ping__":
                await websocket.send("__pong__")
                
            elif message == "hardwarestatus":
                status = self.gameObject.getHardwareStatus();
                await websocket.send(json.dumps(status))
                
            else:
                print(message)
                
    async def handle(self, websocket, path):
        self.activeConnections.append(websocket)
        print("Websocket: connection opened")
        while websocket in self.activeConnections:
            try:
                send_task = asyncio.ensure_future(
                    self.sender(websocket, path))
                receive_task = asyncio.ensure_future(
                    self.receiver(websocket, path))
                done, pending = await asyncio.wait(
                    [send_task, receive_task],
                    return_when=asyncio.FIRST_COMPLETED,
                )
                for task in done:
                    exception = task.exception()
                    if exception:
                        raise exception
                for task in pending:
                    task.cancel()
            except Exception as e:
                print("Websocket: " + str(e))
                print("Websocket: connection closed")
                self.activeConnections.remove(websocket)
                if websocket in self.activeGameConnections:
                    self.activeGameConnections.remove(websocket)
        if len(self.activeGameConnections) == 0:
            self.gameObject.disableGun()
        
    def start(self):
        print("Start websocket...")
        self.gameObject = Game()
        loop = asyncio.new_event_loop()
        server = websockets.serve(self.handle, "0.0.0.0", 5678, loop=loop)
        thread = threading.Thread(target=self.start_loop, args=(server, loop))
        thread.start()

    def start_loop(self, server, loop):
        loop.run_until_complete(server)
        loop.run_forever()
