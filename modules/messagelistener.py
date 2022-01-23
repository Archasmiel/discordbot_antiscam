from discord.ext import commands


class MessageListener(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, ctx):
        guild = ctx.message.guild
        print(guild.categories)

        for category in guild.categories:
            for channel in category.text_channels:
                print(channel)

    @commands.command()
    async def removescam(self, ctx, text):
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
