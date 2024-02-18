from random import randint
from robotBody import RobotBody
from robotMiddle import RobotMiddleLayer
from robotTop import RobotTopLayer
from environment import Environment
from threading import Thread, Lock
from collections import deque


update_queue = deque()
lock = Lock()


def init():
    """
    Returns the update_queue and lock.
    """
    return update_queue, lock


class Agent:
    def __init__(self, env):
        self.__env = env
        self.__body = RobotBody(self.__env)
        self.__middle = RobotMiddleLayer(self.__body)
        self.__top = RobotTopLayer(self.__middle, timeout=30)

        lock.acquire()
        update_queue.append({
            "type": "sprite-init",
            "info": {
                "ID": self.__body.get_ID(),
                "name": "agent",
                "coordinates": self.__body.get_coordinates()
            }
        })
        lock.release()

    def get_env_info(self):
        return self.__env.info()

    def register_update_queue(self, queue, lock):
        self.__body.register_update_queue(queue, lock)

    def do(self):
        """
        Completes a pre-defined task of visiting a bunch of locations.
        """
        self.__top.do({'visit': [(randint(1, 500), randint(1, 500)) for i in range(100)]})


class AgentThread(Thread):
    def __init__(self, name):
        super().__init__(name=name)
        self.__agent = Agent(Environment(width=500, length=500))

    def get_env_info(self):
        return self.__agent.get_env_info()

    def run(self):
        print("Executing `AgentThread`")
        self.__agent.register_update_queue(update_queue, lock)
        self.__agent.do()

        from time import sleep

        sleep(5)
        print("Finished `AgentThread`")
