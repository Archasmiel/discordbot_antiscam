import discord
from discord.ext import commands

intents = discord.Intents(messages=True, members=True)


def filter_by_role(members, role_name):
    lst = []

    for i in members:
        if len(i[1]) > 0:
            if role_name in i[1]:
                lst.append(i[1][0])

    for i in sorted(lst):
        print(i)


async def create_roles(guild):
    with open('files/create_roles.txt', 'r', encoding='utf-8') as f:
        lst = [i.strip() for i in f.readlines()]
    for i in lst:
        await guild.create_role(name=i, colour=discord.Colour(0xF1C40F))


async def delete_roles(guild):
    with open('files/delete_roles.txt', 'r', encoding='utf-8') as f:
        lst = [i.strip() for i in f.readlines()]
    for i in lst:
        for role in guild.roles:
            if role.name == i:
                await role.delete()
                break


async def reposition_roles(guild):
    with open('files/position_of_roles.txt', 'r', encoding='utf-8') as f:
        lst = [i.strip() for i in f.readlines()]
    for pos, current in enumerate(lst):
        for role in guild.roles:
            if role.name == current and role.name != 'СОЗНАНИЕ' and role.name != 'Психиатр':
                try:
                    print(f'{role.position} {len(guild.roles) - pos - 6}: {role}')
                    await role.edit(position=len(guild.roles) - pos - 6)
                    break
                except:
                    pass


def write_roles(guild):
    res = []
    with open(f'files/roles/{guild}.txt', 'w', encoding='utf-8') as f:
        print()
        for role in reversed(guild.roles):
            # if role.name in downwards:
            #     print(f'{role.position} {len(guild.roles) - counter - 1}: {role}')
            #     await role.edit(position=len(guild.roles) - counter - 1)
            res.append(role)
            f.write(f'{role.position}: {role}\n')
    return res


def write_members(guild):
    result = []
    with open(f'files/members/{guild}.txt', 'w', encoding='utf-8') as f:
        for member in guild.members:
            result.append([member.name, [role.name for role in member.roles if role.name != "@everyone"]])
            f.write(f'{member.name}\n'
                    f'{[role.name for role in member.roles if role.name != "@everyone"]}\n\n')
    return result


class MessageListener(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, ctx):
        guild = ctx.message.guild

        current_members = write_members(guild)
        current_roles = write_roles(guild)

        # print(current_members)
        # filter_by_role(current_members, 'ДП-91')

    @commands.command()
    async def crole(self, ctx, name, surname):
        guild = ctx.message.guild
        channel = ctx.channel
        role = await guild.create_role(name=f'{name} {surname}')
        await channel.send(f'Created role [{name} {surname}] successfully!')

    @commands.command()
    async def antiscam(self, ctx, text):
        counter = 0
        current_date = ctx.message.created_at
        guild = ctx.message.guild

        for channel in guild.text_channels:
            messages = await channel.history().flatten()
            for item in messages:
                message = await channel.fetch_message(item.id)
                if (current_date - message.created_at).days > 0:
                    break
                print(f'Message in {channel}')
                if text in message.content:
                    await message.delete()
                    print(f'Del message in {channel}')
                    counter += 1

        for category in guild.categories:
            text_channels = category.text_channels
            for channel in text_channels:
                messages = await channel.history().flatten()
                for item in messages:
                    message = await channel.fetch_message(item.id)
                    if (current_date - message.created_at).days > 0:
                        break
                    print(f'Message in {channel}')
                    if text in message.content:
                        await message.delete()
                        print(f'Del message in {channel}')
                        counter += 1
        await ctx.channel.send(f'Deleted {counter} scam messages')
