import discord, db_user_interface
from discord.ext import commands, tasks
from utility import Timer, make_simple_embed, PARSE_CLASS_VAR
from copy import copy

import customs.cog

class Compensation(customs.cog.Cog):
    amount = 0
    reason = None
    # a
    _users_compensated = list()

    @commands.command()
    @commands.is_owner()
    async def compensate(self, ctx, frogs: int, reason: str):
        '''
        Gives users the option to obtain frogs after a
        server wipe
        '''
        Compensation.amount = frogs
        Compensation.reason = reason
        Compensation._users_compensated.clear()
        await ctx.send(f'Users can now claim `{frogs}` free frogs for reason: `{reason}`')


    @commands.group()
    async def claim(self, ctx):
        if ctx.message.author in Compensation._users_compensated:
            await ctx.send("You already recieved your compensation")
            return
        
        Compensation._users_compensated.append(ctx.message.author)
        db_user_interface.modify_frog(self.bot.db_user, ctx.author.id, Compensation.amount)
        await ctx.send(f'You have recieved `{Compensation.amount}` frogs because `{Compensation.reason}`')


def setup(bot):
    bot.add_cog(Compensation(bot))