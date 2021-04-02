import asyncio
import random
from socket import socket

import websockets

#from ActionSpace import ActionSpace
import logging
import json


class Gym:
    host = None
    port = None
    player = None
    families = None
    types = None
    protocols = None
    logger = None
    # Create a TCP/IP socket
    sock = None
    last_recieved_JSON = None
    loop = None
    maxaction = 5

    def __init__(self, host= 'localhost', port = 9080, player = 'player1'):
        self.host = host
        self.port = port
        self.player = player
        #self.loop = loop
        random.seed()

        # self.families = self.get_constants('AF_')
        # self.types = self.get_constants('SOCK_')
        # self.protocols = self.get_constants('IPPROTO_')

        self.logger = logging.getLogger('websockets')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        print('New gym instance IP:', host, 'Port:', port, 'Playername:', player)

    # Call reset function of environment and returns observation
    #send data
    
    async def step(self, action, delta):
        global maxaction
        test_message = []
        if action.find("accelerate") !=-1:
            test_message.append("accelerate")
        elif action.find("steer_left") !=-1:
            test_message.append("steer_left")
        elif action.find("steer_right") !=-1:
            test_message.append("steer_right")
        elif action.find("steer_center") !=-1:
            test_message.append("steer_center")
        elif action.find("brake") !=-1:
            test_message.append("brake")
        elif action.find("reverse") !=-1:
            test_message.append("reverse")
        elif action.find("reset1") !=-1:
            test_message.append("reset1")
        elif action.find("reset2") !=-1:
            test_message.append("reset2")
        else:
            print("Action is not a valid Step!")

        print(test_message)
        
        message = json.dumps([test_message, delta], sort_keys = True, indent = 4)
        data = []
        
        await self.send_websocket(message, data)
        test = json.loads(data[0])
        reward = test[4]
        observation= test[0:4]
        done = test[5]
        parkpos = test[6]
        rotation = test[7]
        return observation, reward, done, parkpos, rotation


    # TPC - creates env
    def open(self, server_ip=None, port=None):
        if server_ip is not None:
            self.host = server_ip
        if port is not None:
            self.port = port
        # connect to server
        self.create_socket(self.host, self.port)

    # TCP - closes the env
    def close(self):
        # send close to server
        # close socket
        self.close_socket("Closing environment")
        pass

    # send action to env returns observation, reward, done, info
    # creates JSON object
    # async def step(self, action):
    #     if isinstance(action, ActionSpace):
    #         # action is part of ActionSpace
    #         print("go step")
    #         data = await self.send_action(action)
    #         print('step done', data)
    #         return data
    #     else:
    #         print("Action is not a valid Step")

    """ Returns a random action of action space
    """
    def get_sample_action(self):
        global maxaction
        action = random.randrange(0, maxaction)
        return action

    # socket_echo_client_easy.py

    def get_constants(self, prefix):
        """Create a dictionary mapping socket module
        constants to their names.
        """
        return {
            getattr(socket, n): n
            for n in dir(socket)
            if n.startswith(prefix)
        }

    def create_socket(self, server_ip=None, port=None):
        if server_ip is not None:
            self.host = server_ip
        if port is not None:
            self.port = port

        # Create a TCP/IP socket
        self.sock = socket.create_connection(self.host, self.port)

        print('Family  :', self.families[self.sock.family])
        print('Type    :', self.types[self.sock.type])
        print('Protocol:', self.protocols[self.sock.proto])

    # async def send_action(self, next_action):
    #     message = '["' + next_action.name + '"]'
    #     data = []
    #     print('send_action:',message)
    #     await self.send_websocket(message, data)
    #     print("awaited send_action")
    #     print(data)
    #     return data

    async def send_websocket(self, message, data):
        uri = "ws://127.0.0.1:9080"
        async with websockets.connect(uri) as websocket:

            await websocket.send(message)
            # print(f"> {name}")
            data.append(await websocket.recv())

    def send_tcp(self, message):
        try:
            # Send data
            # test message
            # message = b'This is the message.  It will be repeated.'
            print('sending {!r}'.format(message))
            self.sock.sendall(message)

            amount_received = 0
            amount_expected = len(message)
            data = None
            while amount_received < amount_expected:
                data = self.sock.recv(16)
                amount_received += len(data)
            return data

        except Exception as e:
            self.close_socket("closing socket because of exception {}".format(e.args[-1]))

    # TCP - Closing the socket
    def close_socket(self, message):
        print("Closing Socket")
        print("Msg: " + message)
        self.sock.close()
