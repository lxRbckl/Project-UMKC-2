# Project UMKC 2


# Import <
from os import path
from time import strftime
from asyncio import sleep
from json import load, dump
from discord import Intents
from discord.ext.commands import Bot

# >


# Declaration <
path = path.realpath(__file__)[:-8]
UMKC = Bot(command_prefix = '', intents = Intents.all())
token = ''

# >


def jsonLoad(arg):
    ''' arg : str '''

    # if Exists <
    try:

        # Read JSON <
        with open(f'{path}/{arg}.json', 'r') as fileVariable:

            return load(fileVariable)

        # >

    # >

    except:

        # Create JSON <
        jsonDump(arg, {})
        return jsonLoad(arg)

        # >


def jsonDump(*args):
    ''' args[0] : str
        args[1] : dict '''

    # Write JSON <
    with open(f'{path}/{args[0]}.json', 'w') as fileVariable:

        dump(args[1], fileVariable, indent = 4)

    # >


@UMKC.command(aliases = ['purge', 'Purge'])
async def commandPurge(ctx):
    '''  '''

    # if Admin <
    if (str(ctx.author) in jsonLoad('Setting')['adminRole']):

        l = [int(k) for k in jsonLoad('Schedule').keys()]
        [await UMKC.get_channel(k).purge() for k in l]

    # >


async def setName(k, schedule, arg):
    ''' k : str
        schedule : dict
        arg : str '''

    schedule[k]['Name'] = arg
    return schedule


async def setTime(k, schedule, arg):
    ''' k : str
        schedule : dict
        arg : str '''

    # if AM or PM <
    if (arg[1].upper() in ['AM', 'PM']):

        strVariable = f'{arg[0]} {arg[1].upper()}'
        schedule[k]['Time'] = strVariable

    # >

    return schedule


async def setLink(k, schedule, arg):
    ''' k : str
        schedule : dict
        arg : str '''

    schedule[k]['Link'] = arg
    return schedule


async def setDay(k, schedule, arg):
    ''' k : str
        schedule : dict
        arg : tuple '''

    check, l = jsonLoad('Setting')['checkChannel'], []
    for i in arg:

        [l.append(i) for v in check.values() if (i.title() in v)]

    schedule[k]['Day'] = l
    return schedule


async def setStatus(k, schedule, arg):
    ''' k : str
        schedule : dict
        arg : str'''

    # if On or Off <
    if (arg.title() in ['On', 'Off']):

        schedule[k]['Status'] = arg.title()

    # >

    return schedule


@UMKC.command(aliases = ['set', 'Set'])
async def commandSet(ctx, *args):
    ''' args[0] : str
        args[n] : str '''

    k = str(ctx.channel.id)
    schedule = jsonLoad('Schedule')

    # if New Channel <
    if (k not in schedule.keys()):

        schedule[k] = jsonLoad('Setting')['bootChannel']

    # >

    # if args <
    if (len(args) != 0):

        funcDict = {'Day' : setDay(k, schedule, args[1:]),
                    'Name' : setName(k, schedule, args[1]),
                    'Link' : setLink(k, schedule, args[1]),
                    'Time' : setTime(k, schedule, args[1:]),
                    'Status' : setStatus(k, schedule, args[1])}

        schedule = await funcDict[args[0].title()]

    # >

    jsonDump('Schedule', schedule)
    await ctx.message.delete()


@UMKC.command(aliases = ['get', 'Get'])
async def commandGet(ctx):
    '''  '''

    schedule = jsonLoad('Schedule')[str(ctx.channel.id)]
    out = '\n'.join(f'{k}\t{v}' for k, v in schedule.items())

    await ctx.channel.send(out, delete_after = 60)
    await ctx.message.delete()


@UMKC.event
async def on_ready():
    '''  '''

    # while Online <
    while (True):

        await sleep(0.2)

        # if New Minute <
        if ((int(strftime('%S')) % 60) == 0):

            schedule = jsonLoad('Schedule')
            for k, v in schedule.items():

                # if Class is On <
                if (v['Status'] == 'On'):

                    d = strftime('%A')
                    check = jsonLoad('Setting')['checkChannel']
                    for i in check[d]:

                        h, m, f = strftime('%I %M %p').split()
                        time = (f'{int(h)}{m} {f}' == v['Time'])
                        day = (i in [j.title() for j in v['Day']])

                        # if Day and Time <
                        if (day and time):

                            out = ':alarm_clock: {} :alarm_clock:'.format(v['Link'])

                            await UMKC.get_channel(int(k)).send(out, delete_after = 540)
                            await sleep(0.2)

                        # >

                # >

            await sleep(58)

        # >

    # >


# Main <
if (__name__ == '__main__'):

    UMKC.run(token)

# >
