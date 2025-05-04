import discord
import re
import aiohttp
from redbot.core import commands


class EmojiStealer(commands.Cog):
    """Steal emojis from other servers by pasting them into chat."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="steal")
    @commands.guild_only()
    async def steal_emoji(self, ctx, emoji: str, name: str = None):
        """Steal a custom emoji from another server and upload it here.

        Usage: !steal <:emoji:ID> [newname]
        """
        try:
            match = re.match(r"<a?:([\w]+):(\d+)>", emoji)
            if not match:
                return await ctx.send("❌ Invalid emoji format. Please paste the emoji itself (e.g., <:name:id>).")

            emoji_name, emoji_id = match.groups()
            emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{'gif' if emoji.startswith('<a:') else 'png'}"
            emoji_name = name or emoji_name
            emoji_name = re.sub(r"[^a-zA-Z0-9_]", "", emoji_name)[:32]

            if not emoji_name:
                await ctx.send("❌ Could not determine a valid name for the emoji.")
                return

            async with aiohttp.ClientSession() as session:
                async with session.get(emoji_url) as resp:
                    if resp.status != 200:
                        await ctx.send("❌ Couldn't fetch the emoji from Discord.")
                        return
                    emoji_data = await resp.read()

            await ctx.guild.create_custom_emoji(name=emoji_name, image=emoji_data)
            await ctx.send(f"✅ Emoji `{emoji_name}` added successfully!")

        except discord.Forbidden:
            await ctx.send("❌ I need the `Manage Emojis and Stickers` permission.")
        except discord.HTTPException as e:
            await ctx.send(f"❌ Failed to add emoji: {e}")
        except Exception as e:
            await ctx.send(f"❌ Unknown error: {e}")
