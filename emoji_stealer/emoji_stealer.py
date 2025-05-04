"""
Emoji Stealer Cog
~~~~~~~~~~~~~~~~~
Steal emojis from other servers by pasting them into chat.

Author: Puppy
"""

__author__ = "Puppy"
__version__ = "1.0.0"

import discord
from redbot.core import commands
import re
import aiohttp
=======
from redbot.core import commands
import discord
import re

__red_end_user_data_statement__ = "This cog does not store any user data."
>>>>>>> 61402e4 (Initial commit: Add emoji_stealer cog)

class EmojiStealer(commands.Cog):
    """Steal custom emojis from other servers."""

    def __init__(self, bot):
        self.bot = bot

<<<<<<< HEAD
    @commands.command()
    async def steal(self, ctx, emoji: str, name: str = None):
        """
        Steal a custom emoji from another server.

        Paste an emoji like <:name:id> or <a:name:id>
        Optionally provide a new name.
        """
        match = re.match(r"<(a?):(\w+):(\d+)>", emoji)
        if not match:
            await ctx.send("❌ Please paste a valid custom emoji like `<:emoji:123456789>`.")
            return

        is_animated, emoji_name, emoji_id = match.groups()
        filetype = "gif" if is_animated else "png"
        emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{filetype}"

        # Use provided name or fallback to original
        emoji_name = name or emoji_name
        emoji_name = re.sub(r"[^a-zA-Z0-9_]", "", emoji_name)[:32]

        if not emoji_name:
            await ctx.send("❌ Could not determine a valid name for the emoji.")
            return

        try:
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
=======
    @commands.command(name="steal")
    @commands.guild_only()
    async def steal_emoji(self, ctx, emoji: str, name: str = None):
        """Steal a custom emoji from another server and upload it here.

        Usage: !steal <:emoji:ID> [newname]
        """
        try:
            match = re.match(r"<a?:(\\w+):(\\d+)>", emoji)
            if not match:
                return await ctx.send("❌ Invalid emoji format.")

            emoji_name, emoji_id = match.groups()
            emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{'gif' if emoji.startswith('<a:') else 'png'}"
            emoji_name = name or emoji_name

            image_bytes = await self.bot.session.get(emoji_url)
            if image_bytes.status != 200:
                return await ctx.send("❌ Could not fetch emoji.")

            data = await image_bytes.read()
            await ctx.guild.create_custom_emoji(name=emoji_name, image=data)
            await ctx.send(f"✅ Emoji `{emoji_name}` added!")

        except discord.Forbidden:
            await ctx.send("❌ I do not have permission to add emojis.")
        except discord.HTTPException as e:
            await ctx.send(f"❌ Discord error: {e}")
        except Exception as e:
            await ctx.send(f"❌ Unknown error: {e}")

