
# -*- coding: utf-8 -*-
import os
from aiohttp import web
import logging
from unittest.mock import MagicMock, patch
import asyncio
from telethon import *
import re
import random
import cbpi
from cbpi.api import *
from cbpi.api.config import ConfigType
from cbpi.api.base import CBPiBase
import requests
from voluptuous.schema_builder import message
from cbpi.api.dataclasses import NotificationType
from cbpi.controller.notification_controller import NotificationController
from cbpi.http_endpoints.http_notification import NotificationHttpEndpoints

logger = logging.getLogger(__name__)

class TelegramCallbacks(CBPiExtension):

    def __init__(self,cbpi):
        self.cbpi = cbpi
        self.controller : StepController = cbpi.step
        self.cbpi.register(self, "/step2")

    @events.register(events.CallbackQuery)
    async def callbackQuery(event):
        message = await event.get_message()
        if "get_target_temp" in message:
            for item in fermenter:
                if item["id"] == event.data:
                    await event.edit("Target_temp of {} is {].".format(item["name"],self.get_fermenter_target_temp(item["id"])))
            for item in kettles:
                if item["id"] == event.data:
                    await event.edit("Target_temp of {} {].".format(item["name"],self.get_kettle_target_temp(item["id"])))
        elif "set_target_temp" in message:
            for item in fermenter:
                if item["id"] == event.data:
                    await event.edit("Enter the new target temperature for {}:".format(item["name"]))
            for item in kettles:
                if item["id"] == event.data:
                    await event.edit("Enter the new target temperature for {}:".format(item["name"]))
    
    @events.register(events.NewMessage(pattern='/next'))
    async def next(event):
        await self.controller.next()
        raise events.StopPropagation
        
    @events.register(events.NewMessage(pattern='/help'))
    async def help(event):
        bot = event.client
        chat_id = event.chat_id
        tmp=""
        cmd_list = [{"command":"help","description":"get a list of all commands with description"},
                    {"command":"next","description":"Next Brew Step"},
                    {"command":"start","description":"start brewing"},
                    {"command":"stop","description":"stop brewing"},
                    {"command":"set_target","description":"set Target Temperature of the item you choose"},
                    {"command":"get_target","description":"get Target Temperature of all items"},
                    {"command":"get_timer","description":"get the actual countdown time"},
                    {"command":"get_chart","description":"send Picture of chart from the item you choose"},
                    {"command":"get_parameter","description":"get all parameters of the item you choose"}]
        for items in cmd_list:
            tmp=tmp+("/%s: %s\n" %(items["command"],items["description"]))
        title= 'List of Commands:'
        await event.respond("**{}** \n__{}__".format(title,tmp))
        raise events.StopPropagation
    
    @events.register(events.NewMessage(pattern='/start'))
    async def start(event):
        await self.controller.start()
        raise events.StopPropagation
    
    @events.register(events.NewMessage(pattern='/stop'))
    async def stop(event):
        await self.controller.stop()
        raise events.StopPropagation
    
    @events.register(events.NewMessage(pattern='/set_target'))
    async def setTarget(event):
        bot = event.client
        buttons = []
        logger.info(event)
        kettles = self.cbpi.kettle.get_state()
        logger.info(event)
        fermenter = self.cbpi.fermenter.get_state()
        for value in kettles["data"]:
            # logger.info(value["name"])
            # logger.warning(self.cbpi.sensor.get_sensor_value(value["id"])["value"])
            buttons.append(Button.inline(value["name"],value["id"]))
        for value in fermenter["data"]:
            # logger.info(value["name"])
            buttons.append(Button.inline(value["name"],value["id"]))
        await event.respond("**Choose Item for set_target_temp**",buttons=buttons)
        raise events.StopPropagation
    
    @events.register(events.NewMessage(pattern='/get_target'))
    async def getTarget(event):
        bot = event.client
        buttons = []
        logger.info(self)
        kettles = self.cbpi.kettle.get_state()
        fermenter = self.cbpi.fermenter.get_state()
        for value in kettles["data"]:
            # logger.info(value["name"])
            # logger.warning(self.cbpi.sensor.get_sensor_value(value["id"])["value"])
            buttons.append(Button.inline(value["name"],value["id"]))
        for value in fermenter["data"]:
            # logger.info(value["name"])
            buttons.append(Button.inline(value["name"],value["id"]))
        await event.respond("**Choose Item for get_target_temp**",buttons=buttons)
        raise events.StopPropagation
    
    @events.register(events.NewMessage(pattern='/get_timer'))
    async def getTimer(event):
        bot = event.client
        steps = self.cbpi.step.get_state()
        for value in steps["steps"]:
            if value["status"] == "A":
                await event.respond("timer of step '{}' is {}.".format(value["name"],value["state_text"]))
            logger.warning("{}: {}".format(value["name"],value["status"]))
        
        raise events.StopPropagation
    
    @events.register(events.NewMessage)
    async def new_message_handler(event):
        bot = event.client
        sender = await event.get_sender()
        logger.warning(sender)
        chat_id = event.chat_id
        messages = await sender.get_messages(int(chat_id),limit=2)
        for message in messages:
            if "new target temperature" in message:
                temp = '999'
                unit = "°C"
                match = re.match(r'^(?=(.|,))([+-]?([0-9]*)(\(.|,)([0-9]+))?)$', event.raw_text)
                number = match.group(1)
                if number is not None:
                    if 'F' in self.cbpi.config.get("TEMP_UNIT", "C"):
                        unit = "°F"
                        temp = round(9.0 / 5.0 * float(number) + 32, 2)
                    else:
                        temp = float(number)
                    # await self.controller.set_target_temp(id,temp)
                    for item in fermenter:
                        if item["name"] in message:
                            await self.set_fermenter_target_temp(item["id"],temp)
                            await event.respond("Set Target_temp of {} to {}{}.".format(item["name"],temp,unit))
                    for item in kettles:
                        if item["id"] in message:
                            await self.set_target_temp(item["id"],temp)
                            await event.respond("Set Target_temp of {} to {}{}.".format(item["name"],temp,unit))
                else:
                    await event.respond("**No valid Input for Set Target_temp of {} found!**".format(item["name"]))

            if "original gravity" in message:
                match = re.match(r'^(?=(.|,))([+-]?([0-9]*)(\(.|,)([0-9]+))?)$', event.raw_text)
                number = match.group(1)
                if number is not None:
                    await self.controller.next()
                else:
                    await event.respond("**No valid Input for measure of original gravity found!**")

        if r'(?i).*moin' or r'(?i).*hi' or r'(?i).*h(a|e)llo' in event.raw_text:
            sender = await event.get_sender()
            await event.respond("Hi {}, use command /help to find a list of all commands.".format(sender))
        else:
            sender = await event.get_sender()
            await event.respond("Hi {}, I could not parse your text.".format(sender))
