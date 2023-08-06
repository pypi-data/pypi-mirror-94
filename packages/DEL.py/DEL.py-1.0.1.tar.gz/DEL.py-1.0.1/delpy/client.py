import json
import time
import discord
from aiohttp import ClientSession
from asyncio import get_event_loop, AbstractEventLoop
from . import errors


class Client:
    """
    API wrapper for discordextremelist.xyz
    """

    def __init__(self, bot: discord.Client = None, token: str = None, *, baseurl: str = "https://api.discordextremelist.xyz/v2/", loop: AbstractEventLoop=None):
        self.bot = bot
        self.token = token
        self.baseurl = baseurl
        self.session = ClientSession(loop=loop if loop else get_event_loop())

    async def post_stats(self, guildCount: int, shardCount: int = None):
        """
        Post bot statistics to the API

        :param guildCount: Server count
        :param shardCount: Shard count (optional)
        """

        head = {"Authorization": self.token, "Content-Type": 'application/json'}
        if not self.token:
            raise errors.Unauthorized("The token is either invalid or missing.")

        to_post = json.dumps({'guildCount': guildCount, 'shardCount': shardCount})
        if not shardCount:
            to_post = json.dumps({'guildCount': guildCount})
        r = await self.session.post(self.baseurl+"bot/{0}/stats".format(self.bot.user.id), headers=head, data=to_post)
        result = json.loads(await r.text())
        
        if result['error']:
            raise errors.HTTPException(raised_error=result)
    
    async def get_website_stats(self):
        """
        Get website statistics
        
        :return WebsiteStats: Website statistics
        """

        start_time = time.time()
        r = await self.session.get(self.baseurl+"stats")
        data = json.loads(await r.text())
        if data['error']:
            raise errors.HTTPException(raised_error=data)

        data['time_taken'] = (time.time() - start_time) * 1000
        return data
    
    async def get_website_health(self):
        """
        Get website health
        
        :return WebsiteHealth: Website health
        """

        start_time = time.time()
        r = await self.session.get(self.baseurl+"health")
        data = json.loads(await r.text())
        if data['error']:
            raise errors.HTTPException(raised_error=data)

        data['time_taken'] = (time.time() - start_time) * 1000
        return data

    async def get_bot_info(self, botid: str):
        """
        Get a bot listed on discordextremelist.xyz

        :param botid: Bot to be fetched
        :return Bot: Bot that was fetched
        """

        start_time = time.time()
        r = await self.session.get(self.baseurl+"bot/{0}".format(botid))
        data = json.loads(await r.text())
        if data['error']:
            raise errors.HTTPException(raised_error=data)

        data['time_taken'] = (time.time() - start_time) * 1000
        return data
    
    async def get_server_info(self, serverid: str):
        """
        Get a server listed on discordextremelist.xyz

        :param serverid: Server to be fetched
        :return Server: Server that was fetched
        """

        start_time = time.time()
        r = await self.session.get(self.baseurl+"server/{0}".format(serverid))
        data = json.loads(await r.text())
        if data['error']:
            raise errors.HTTPException(raised_error=data)

        data['time_taken'] = (time.time() - start_time) * 1000
        return data
    
    async def get_template_info(self, templateid: str):
        """
        Get a template listed on discordextremelist.xyz

        :param templateid: Template to be fetched
        :return Template: Template that was fetched
        """

        start_time = time.time()
        r = await self.session.get(self.baseurl+"template/{0}".format(templateid))
        data = json.loads(await r.text())
        if data['error']:
            raise errors.HTTPException(raised_error=data)

        data['time_taken'] = (time.time() - start_time) * 1000
        return data
    
    async def get_user_info(self, userid: str):
        """
        Get a registered user on discordextremelist.xyz

        :param userid: User to be fetched
        :return User: User that was fetched
        """

        start_time = time.time()
        r = await self.session.get(self.baseurl+"user/{0}".format(userid))
        data = json.loads(await r.text())
        if data['error']:
            raise errors.HTTPException(raised_error=data)

        data['time_taken'] = (time.time() - start_time) * 1000
        return data
