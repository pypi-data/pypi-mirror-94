from plugins.debate.layout import ServerSetup

plugin_data = {"name": "Debate Plugins", "database": True}


def setup(bot):
    bot.add_cog(ServerSetup(bot))
