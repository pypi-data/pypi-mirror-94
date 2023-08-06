# -*- coding: utf-8 -*-
import asyncio
import random
import re
import random
from aiohttp import web
from cbpi.api import *


@parameters([])
class CustomSensor(CBPiSensor):
    
    def __init__(self, cbpi, id, props):
        super(CustomSensor, self).__init__(cbpi, id, props)
        self.value = 0


    @action(key="Test", parameters=[])
    async def action1(self, **kwargs):
        print("ACTION!", kwargs)

    @action(key="Test1", parameters=[])
    async def action2(self, **kwargs):
        print("ACTION!", kwargs)
    
    @action(key="Test2", parameters=[])
    async def action3(self, **kwargs):
        print("ACTION!", kwargs)

    async def run(self):

        while self.running is True:
            print(self.get_config_value("TEMP_UNIT", "NONE"))
            print(self.get_static_config_value("port", "NONE"))
            await self.set_config_value("BREWERY_NAME", "WOOHOO HELLO")

            self.value = random.randint(0,50)
            self.push_update(self.value)
            await asyncio.sleep(1)
    
    def get_state(self):
        return dict(value=self.value)


def setup(cbpi):

    '''
    This method is called by the server during startup 
    Here you need to register your plugins at the server
    
    :param cbpi: the cbpi core 
    :return: 
    '''
    cbpi.plugin.register("CustomSensor", CustomSensor)
