# Project UMKC 2 by Alex Arbuckle #


# Import <
from json import load, dump
from discord import Intents
from datetime import datetime as dt
from discord.ext.commands import Bot

# >


# Declaration <
UMKC = Bot(command_prefix = '', intents = Intents.all())

# >


def jsonLoad():
    '''  '''

    with open('UMKC.json', 'r') as fileVariable:

        return load(fileVariable)


def jsonDump(arg):
    '''  '''

    with open('UMKC.json', 'w') as fileVariable:

        dump(arg, fileVariable, indent = 4)


@UMKC.event
async def on_ready():
    '''  '''

    # Algorithm <
    #while (True):

        #dictVariable, day = jsonLoad()['Schedule'], dt.today().weekday()
        #hour, minute = dt.today().strftime('%H'), dt.today().strftime('%M')
        #current = f'{int(hour)}{minute} ' + '{}'.format(dt.today().strftime('%p'))
        #for key in dictVariable.keys():

            #if (key['Time'] == )



    # >





@UMKC.command(aliases = ['set', 'Set'])
async def commandSet(ctx, *args):
    ''' args[0] : str
        args[1] : str '''

    dictVariable = jsonLoad()
    channelId = str(ctx.channel.id)
    bootSchedule = {'Name' : 'NA',
                    'Time' : 'NA',
                    'Link' : 'NA',
                    'Day' : []}

    # if New <
    if (channelId not in dictVariable['Schedule'].keys()):

        dictVariable['Schedule'][channelId] = bootSchedule

    # >

    # if Key <
    if (args[0].title() in bootSchedule.keys()):

        strVariable = f'{args[0].title()} : {args[1]}'
        dictVariable['Schedule'][channelId][args[0].title()] = args[1]

        await ctx.channel.send(strVariable, delete_after = 30)
        await ctx.message.delete()
        jsonDump(dictVariable)

    # >


@UMKC.command(aliases = ['get', 'Get'])
async def commandGet(ctx):
    '''  '''

    dictVariable, channel = jsonLoad()['Schedule'], str(ctx.channel.id)
    strVariable = ''.join(f'{k}\t{v}\n' for k, v in dictVariable[channel].items())

    await ctx.channel.send(f'```{strVariable}```', delete_after = 30)
    await ctx.message.delete()


@UMKC.command(aliases = ['purge', 'Purge'])
async def commandPurge(ctx):
    '''  '''

    # if Admin <
    if (str(ctx.author) in jsonLoad()['Admin']):

        # Purge Channels <
        [await UMKC.get_channel(int(k)).purge() for k in jsonLoad().keys()]

        # >

    # >

# Main <
UMKC.run(jsonLoad()['token'])

# >
