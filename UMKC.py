# Project UMKC 2 #


# Import <
from json import load, dump
from discord import Intents
from discord.ext.commands import Bot

# >


# Declaration <
UMKC = Bot(command_prefix = '', intents = Intents.all())
admin = []
token = ''

# >


def jsonLoad(arg):
    ''' arg : str '''

    # if Exists <
    try:

        # Open JSON <
        with open(f'{arg}.json', 'r') as fileVariable:

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

    # Open JSON <
    with open(f'{args[0]}.json', 'w') as fileVariable:

        dump(args[1], fileVariable, indent = 4)

    # >


@UMKC.command(aliases = ['set', 'Set'])
async def commandSet(ctx):
    '''  '''

    key = str(ctx.channel.id)
    jsonVariable = jsonLoad('Schedule')

    # if New <
    if (key not in jsonVariable.keys()):

        value = {'Name' : 'NA',
                 'Time' : 'NA',
                 'Link' : 'NA',
                 'Day' : []}

        jsonVariable[key] = value

        jsonDump('Schedule', jsonVariable)
        await ctx.message.delete()

    # >


@UMKC.command(aliases = [])
async def setName(ctx, arg):
    ''' arg : str '''

    key = str(ctx.channel.id)
    jsonVariable = jsonLoad('Schedule')

    # if Existing <
    if (key in jsonVariable.keys()):

        jsonVariable[key]['Name'] = arg

        jsonDump('Schedule', jsonVariable)
        await ctx.message.delete()

    # >


@UMKC.command(aliases = [])
async def setTime(ctx, *args):
    ''' args[0] : str
        args[1] : str '''

    key = str(ctx.channel.id)
    jsonVariable = jsonLoad('Schedule')

    # if Existing <
    if (key in jsonVariable.keys()):

        # if 'AM' or 'PM' <
        if (args[1].upper() in ['AM', 'PM']):

            jsonVariable[key]['Time'] = f'{args[0]} {args[1].upper()}'

            jsonDump('Schedule', jsonVariable)
            await ctx.message.delete()

        # >

        else:

            pass

    # >


@UMKC.command(aliases = ['get', 'Get'])
async def commandGet(ctx):
    '''  '''

    jsonVariable = jsonLoad('Schedule')[str(ctx.channel.id)]
    strVariable = '\n'.join(f'{k}\t{v}' for k, v in jsonVariable.items())

    await ctx.channel.send(strVariable, delete_after = 60)


@UMKC.command(aliases = ['purge', 'Purge'])
async def commandPurge(ctx):
    '''  '''

    # if Admin <
    if (str(ctx.author) in admin):

        l = [int(i) for i in jsonLoad('Schedule').keys()]
        [await UMKC.get_channel(int(i)).purge() for i in l]

    # >


# Main <
if (__name__ == '__main__'):

    UMKC.run(token)

# >
