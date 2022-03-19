import asyncio

import async_timeout
import wavelink
from nextcord import ClientException
from nextcord.ext import commands
from wavelink import (
    LavalinkException,
    LoadTrackError,
    SoundCloudTrack,
    YouTubeMusicTrack,
    YouTubePlaylist,
    YouTubeTrack,
)
from wavelink.ext import spotify
from wavelink.ext.spotify import SpotifyTrack

from ._classes import Provider
from .checks import voice_channel_player, voice_connected
from .errors import MustBeSameChannel
from .paginator import Paginator
from .player import DisPlayer

class music(commands.Cog, name="music"):
    """Recives Music commands"""

    COG_EMOJI = "🎵"

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot 
        
        



def setup(bot):
    bot.add_cog(music(bot))
