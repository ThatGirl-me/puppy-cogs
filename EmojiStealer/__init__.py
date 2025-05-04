# /home/pb/puppy-cogs/EmojiStealer/__init__.py
from .emoji_stealer import EmojiStealer

async def setup(bot):
    await bot.add_cog(EmojiStealer(bot))
