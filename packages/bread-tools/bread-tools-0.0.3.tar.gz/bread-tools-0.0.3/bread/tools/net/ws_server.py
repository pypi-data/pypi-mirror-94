import asyncio
import websockets


class WSServer(object):
    """
    Web socket server.
    Example:
        def handler(msg):
            return 'Get msg:' + msg

        server = WSServer(process_handler=handler)
        server.start()
    """

    def __init__(self, process_handler):
        assert process_handler is not None
        self.__handler = process_handler

    async def process_msg(self, w_socket):
        while True:
            received_msg = await w_socket.recv()
            response_msg = self.__handler(received_msg)
            await w_socket.send(response_msg)
            # return True

    async def main_logic(self, w_socket, path):
        await self.process_msg(w_socket)

    def start(self, ip='127.0.0.1', port=5678):
        start_server = websockets.serve(self.main_logic, ip, port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
