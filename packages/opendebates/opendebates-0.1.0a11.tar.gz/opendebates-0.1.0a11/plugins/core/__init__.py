from plugins.core.error import CommandError
from plugins.core.navigation import HelpMenu
from plugins.core.startup import Login

plugin_data = {"name": "Core Plugins", "database": False}


def setup(bot):
    bot.add_cog(CommandError(bot))
    bot.add_cog(HelpMenu(bot))
    bot.add_cog(Login(bot))
