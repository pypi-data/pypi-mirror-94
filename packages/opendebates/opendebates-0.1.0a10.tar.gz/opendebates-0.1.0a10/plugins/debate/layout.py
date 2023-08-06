import asyncio

import discord
from discord import ChannelType, Colour, PermissionOverwrite, Permissions, utils
from discord.ext import commands
from discord.ext.commands import BucketType

from plugins.debate.overwrites import (
    _debate_tc_citizen_permissions,
    _debate_tc_member_permissions,
    generate_overwrite,
    lockdown_citizen_general_perms,
    lockdown_debate_member_perms,
    lockdown_permissions,
)
from plugins.debate.rooms.interface import DebateRooms


class ServerSetup(commands.Cog, name="Server Setup"):
    def __init__(self, bot):
        self.bot = bot
        self.logger = self.bot.logger
        self.db = self.bot.db

        # Roles
        self.role_warden = None
        self.role_engineering = None
        self.role_staff = None
        self.role_director = None
        self.role_moderator = None
        self.role_grandmaster = None
        self.role_legend = None
        self.role_master = None
        self.role_expert = None
        self.role_distinguished = None
        self.role_apprentice = None
        self.role_novice = None
        self.role_initiate = None
        self.role_rookie = None
        self.role_incompetent = None
        self.role_bot = None
        self.role_citizen = None
        self.role_member = None
        self.role_events = None
        self.role_logs = None
        self.role_detained = None
        self.role_muted = None
        self.role_super_muted = None
        self.role_everyone = None

        self.roles = {
            "role_warden": self.role_warden,
            "role_engineering": self.role_engineering,
            "role_staff": self.role_staff,
            "role_director": self.role_director,
            "role_moderator": self.role_moderator,
            "role_grandmaster": self.role_grandmaster,
            "role_legend": self.role_legend,
            "role_master": self.role_master,
            "role_expert": self.role_expert,
            "role_distinguished": self.role_distinguished,
            "role_apprentice": self.role_apprentice,
            "role_novice": self.role_novice,
            "role_initiate": self.role_initiate,
            "role_rookie": self.role_rookie,
            "role_incompetent": self.role_incompetent,
            "role_bot": self.role_bot,
            "role_citizen": self.role_citizen,
            "role_member": self.role_member,
            "role_events": self.role_events,
            "role_logs": self.role_logs,
            "role_detained": self.role_detained,
            "role_muted": self.role_muted,
            "role_super_muted": self.role_super_muted,
        }

        # Channels
        self.category_information = None
        self.channel_rules = None
        self.channel_about = None
        self.channel_verification = None
        self.channel_announcements = None
        self.channel_community_updates = None
        self.category_moderation = None
        self.channel_director_commands = None
        self.channel_mod_commands = None
        self.channel_isolation = None
        self.category_interface = None
        self.channel_debate_feed = None
        self.channel_commands = None
        self.category_community = None
        self.channel_general = None
        self.channel_serious = None
        self.channel_meme_dump = None
        self.category_debate = None
        self.category_logs = None
        self.channel_moderator_actions = None
        self.channel_message_deletion = None
        self.channel_message_edits = None
        self.channel_ban_unban = None
        self.channel_nicknames = None
        self.channel_join_leave = None
        self.channel_automod = None
        self.channel_channels = None
        self.channel_invites = None
        self.channel_roles = None
        self.channel_voice = None

        self.channels = {
            "category_information": self.category_information,
            "tc_rules": self.channel_rules,
            "tc_about": self.channel_about,
            "tc_verification": self.channel_verification,
            "tc_announcements": self.channel_announcements,
            "tc_community_updates": self.channel_community_updates,
            "category_moderation": self.category_moderation,
            "tc_director_commands": self.channel_director_commands,
            "tc_mod_commands": self.channel_mod_commands,
            "tc_isolation": self.channel_isolation,
            "category_interface": self.category_interface,
            "tc_debate_feed": self.channel_debate_feed,
            "tc_commands": self.channel_commands,
            "category_community": self.category_community,
            "tc_general": self.channel_general,
            "tc_serious": self.channel_serious,
            "tc_meme_dump": self.channel_meme_dump,
            "category_debate": self.category_debate,
            "category_logs": self.category_logs,
            "tc_moderator_actions": self.channel_moderator_actions,
            "tc_message_deletion": self.channel_message_deletion,
            "tc_message_edits": self.channel_message_edits,
            "tc_ban_unban": self.channel_ban_unban,
            "tc_nicknames": self.channel_nicknames,
            "tc_join_leave": self.channel_join_leave,
            "tc_automod": self.channel_automod,
            "tc_channels": self.channel_channels,
            "tc_invites": self.channel_invites,
            "tc_roles": self.channel_roles,
            "tc_voice": self.channel_voice,
        }

        # Debate
        self.debate_rooms = []
        self.debate_room_maps = []
        self.elo_role_maps = {}

    async def cog_check(self, ctx):
        """Check if user has the Engineering role."""
        engineering = utils.get(ctx.guild.roles, name="Engineering")
        return engineering in ctx.author.roles

    @commands.cooldown(1, 50000, BucketType.guild)
    @commands.command(
        name="setup-roles",
        brief="Set up roles required by the bot in the server.",
        help="This command will set up all roles and the associated "
        "permissions required by the bot in the server. This command "
        "should not be used multiple times in a period of 24 hrs as you "
        "will be rate limited.",
    )
    async def setup_roles(self, ctx):
        """Setup roles for the server."""
        guild = ctx.guild

        # Indicate command is running.
        title = f"🔍 Processing Roles"
        response = discord.Embed(color=0x696969, title=title)
        progress_message = await ctx.channel.send(embed=response)

        # Delete All Roles
        for role in guild.roles[1:]:
            if not role.managed:
                await role.delete(reason="Server Setup")
                await asyncio.sleep(5)

        # Setup Power Roles
        self.role_everyone = guild.default_role
        await self.role_everyone.edit(permissions=Permissions(permissions=0))

        self.role_warden = await guild.create_role(
            name="Warden",
            permissions=Permissions(permissions=8),
            color=Colour(value=0xEB6A5C),
            hoist=False,
        )
        await ctx.me.add_roles(self.role_warden)

        self.role_engineering = await guild.create_role(
            name="Engineering", permissions=Permissions(permissions=8), hoist=False
        )
        await guild.owner.add_roles(self.role_engineering)

        self.role_staff = await guild.create_role(
            name="Staff", permissions=Permissions(permissions=36768832), hoist=False
        )
        await guild.owner.add_roles(self.role_staff)

        self.role_director = await guild.create_role(
            name="Director",
            permissions=Permissions(permissions=1275064288),
            color=Colour(value=0xE74C3C),
            hoist=False,
        )
        await guild.owner.add_roles(self.role_director)

        self.role_moderator = await guild.create_role(
            name="Moderator",
            permissions=Permissions(permissions=267775936),
            color=Colour(value=0x2ECC71),
            hoist=False,
        )

        # Setup Rated Roles
        self.role_grandmaster = await guild.create_role(
            name="Grandmaster 👑",
            permissions=Permissions(permissions=0),
            hoist=True,
        )

        self.role_legend = await guild.create_role(
            name="Legend 🏆", permissions=Permissions(permissions=0), hoist=True
        )

        self.role_master = await guild.create_role(
            name="Master ⚖️", permissions=Permissions(permissions=0), hoist=True
        )

        self.role_expert = await guild.create_role(
            name="Expert ⚔️", permissions=Permissions(permissions=0), hoist=True
        )

        self.role_distinguished = await guild.create_role(
            name="Distinguished 💥",
            permissions=Permissions(permissions=0),
            hoist=True,
        )

        self.role_apprentice = await guild.create_role(
            name="Apprentice 💡",
            permissions=Permissions(permissions=0),
            hoist=True,
        )

        self.role_novice = await guild.create_role(
            name="Novice 🔥", permissions=Permissions(permissions=0), hoist=True
        )

        self.role_initiate = await guild.create_role(
            name="Initiate 🔰", permissions=Permissions(permissions=0), hoist=True
        )

        self.role_rookie = await guild.create_role(
            name="Rookie 🧷", permissions=Permissions(permissions=0), hoist=True
        )

        self.role_incompetent = await guild.create_role(
            name="Incompetent 💯",
            permissions=Permissions(permissions=0),
            hoist=True,
        )

        self.role_bot = await guild.create_role(
            name="Bot", permissions=Permissions(permissions=0), hoist=True
        )
        await ctx.me.add_roles(self.role_bot)

        # Setup Basic Roles
        self.role_citizen = await guild.create_role(
            name="Citizen", permissions=Permissions(permissions=104189504), hoist=False
        )

        self.role_member = await guild.create_role(
            name="Member", permissions=Permissions(permissions=36768832), hoist=False
        )

        # Setup Miscellaneous Roles
        self.role_events = await guild.create_role(
            name="Events", permissions=Permissions(permissions=0), hoist=False
        )

        self.role_logs = await guild.create_role(
            name="Logs", permissions=Permissions(permissions=0), hoist=False
        )

        # Setup Punishment Roles
        self.role_detained = await guild.create_role(
            name="Detained", permissions=Permissions(permissions=0), hoist=False
        )

        self.role_muted = await guild.create_role(
            name="Muted", permissions=Permissions(permissions=0), hoist=False
        )

        self.role_super_muted = await guild.create_role(
            name="Super Muted", permissions=Permissions(permissions=0), hoist=False
        )

        # Update Database
        await self.db.upsert(
            guild,
            role_warden=self.role_warden.id,
            role_engineering=self.role_engineering.id,
            role_staff=self.role_staff.id,
            role_director=self.role_director.id,
            role_moderator=self.role_moderator.id,
            role_grandmaster=self.role_grandmaster.id,
            role_legend=self.role_legend.id,
            role_master=self.role_master.id,
            role_expert=self.role_expert.id,
            role_distinguished=self.role_distinguished.id,
            role_apprentice=self.role_apprentice.id,
            role_novice=self.role_novice.id,
            role_initiate=self.role_initiate.id,
            role_rookie=self.role_rookie.id,
            role_incompetent=self.role_incompetent.id,
            role_bot=self.role_bot.id,
            role_citizen=self.role_citizen.id,
            role_member=self.role_member.id,
            role_events=self.role_events.id,
            role_logs=self.role_logs.id,
            role_detained=self.role_detained.id,
            role_muted=self.role_muted.id,
            role_super_muted=self.role_super_muted.id,
        )

        # Confirm database has been updated.
        response = discord.Embed(color=0x77B255, title="✅ Roles Updated")
        await progress_message.edit(embed=response, delete_after=30)

    async def check_roles(self, ctx, message):
        guild = ctx.guild
        title = f"❌ {message} ❌"
        for role in self.roles.keys():
            # Check if role exists within database.
            role_id = await self.db.get(guild, state=f"{role}")
            if role_id:
                # Check if role exists within server.
                grabbed_role = guild.get_role(role_id)
                self.roles[f"{role}"] = grabbed_role
                if grabbed_role is None:
                    embed = discord.Embed(title=title)
                    await ctx.send(embed=embed, delete_after=10)
                    return False
            else:
                embed = discord.Embed(title=title)
                await ctx.send(embed=embed, delete_after=10)
                return False
        return True

    async def check_channels(self, ctx, message):
        guild = ctx.guild
        title = f"❌ {message} ❌"
        for channel in self.channels.keys():
            # Check if channel exists within database.
            channel_id = await self.db.get(guild, state=f"{channel}")
            if channel_id:
                # Check if channel exists within server.
                grabbed_channel = guild.get_channel(channel_id)
                self.channels[f"{channel}"] = grabbed_channel
                if grabbed_channel is None:
                    embed = discord.Embed(title=title)
                    await ctx.send(embed=embed, delete_after=10)
                    return False
            else:
                embed = discord.Embed(title=title)
                await ctx.send(embed=embed, delete_after=10)
                return False

        for _channel_number in range(1, 21):
            tc_id = await self.db.get(guild, state=f"tc_debate_{_channel_number}")

            if tc_id:
                grabbed_channel = guild.get_channel(tc_id)
                if grabbed_channel is None:
                    embed = discord.Embed(title=title)
                    await ctx.send(embed=embed, delete_after=10)
                    return False
            else:
                embed = discord.Embed(title=title)
                await ctx.send(embed=embed, delete_after=10)
                return False

            vc_id = await self.db.get(guild, state=f"vc_debate_{_channel_number}")
            if vc_id:
                grabbed_channel = guild.get_channel(vc_id)
                if grabbed_channel is None:
                    embed = discord.Embed(title=title)
                    await ctx.send(embed=embed, delete_after=10)
                    return False
            else:
                embed = discord.Embed(title=title)
                await ctx.send(embed=embed, delete_after=10)
                return False
        return True

    @commands.command(
        name="setup-channels",
        brief="Set up channels required by the bot in the server.",
        help="This command will set up all channels and it's permissions "
        "required by the bot in the server.",
    )
    async def setup_channels(self, ctx):
        guild = ctx.guild
        self.role_everyone = guild.default_role

        # Indicate command is running.
        title = f"🔍 Processing Channels"
        response = discord.Embed(color=0x696969, title=title)
        progress_message = await ctx.channel.send(embed=response)

        roles_set_up = await self.check_roles(
            ctx, message="Cannot set up channels without roles set up."
        )

        # Exit early if roles not set up
        if not roles_set_up:
            return

        # Delete All Channels
        await guild.rules_channel.edit(category=None)
        await guild.public_updates_channel.edit(category=None)

        for channel in guild.channels:
            skipped_channels = [guild.rules_channel, guild.public_updates_channel]

            if channel not in skipped_channels:
                await channel.delete(reason="Server Setup")

        # Setup Information Category
        self.category_information = await guild.create_category(
            name="Information",
            overwrites=generate_overwrite(ctx, self.roles, "information"),
        )

        self.channel_rules = guild.rules_channel

        await guild.rules_channel.edit(
            name="rules", category=self.category_information, sync_permissions=True
        )

        self.channel_about = await guild.create_text_channel(
            name="about", category=self.category_information, sync_permissions=True
        )

        self.channel_verification = await guild.create_text_channel(
            name="verification",
            category=self.category_information,
            overwrites=generate_overwrite(ctx, self.roles, "verification"),
        )

        self.channel_announcements = await guild.create_text_channel(
            name="announcements",
            category=self.category_information,
            sync_permissions=True,
        )
        await self.channel_announcements.edit(type=ChannelType.news)

        self.channel_community_updates = guild.public_updates_channel
        await guild.public_updates_channel.edit(
            name="community-updates",
            category=self.category_information,
            position=8,
            overwrites=generate_overwrite(ctx, self.roles, "community_updates"),
        )

        # Setup Moderation Category
        self.category_moderation = await guild.create_category(
            name="Moderation",
            overwrites=generate_overwrite(ctx, self.roles, "moderation"),
        )

        self.channel_director_commands = await guild.create_text_channel(
            name="director-commands",
            category=self.category_moderation,
            overwrites=generate_overwrite(ctx, self.roles, "director_commands"),
        )

        self.channel_mod_commands = await guild.create_text_channel(
            name="mod-commands",
            category=self.category_moderation,
            sync_permissions=True,
        )

        self.channel_isolation = await guild.create_text_channel(
            name="isolation",
            category=self.category_moderation,
            overwrites=generate_overwrite(ctx, self.roles, "isolation"),
            slowmode_delay=15,
        )

        # Setup Interface Category
        self.category_interface = await guild.create_category(
            name="Interface",
            overwrites=generate_overwrite(ctx, self.roles, "interface"),
        )

        self.channel_debate_feed = await guild.create_text_channel(
            name="debate-feed", category=self.category_interface, sync_permissions=True
        )

        self.channel_commands = await guild.create_text_channel(
            name="commands",
            category=self.category_interface,
            overwrites=generate_overwrite(ctx, self.roles, "commands"),
            slowmode_delay=5,
        )

        # Setup Community Category
        self.category_community = await guild.create_category(
            name="Community",
            overwrites=generate_overwrite(ctx, self.roles, "community"),
        )

        self.channel_general = await guild.create_text_channel(
            name="general", category=self.category_community, sync_permissions=True
        )

        self.channel_serious = await guild.create_text_channel(
            name="serious", category=self.category_community, sync_permissions=True
        )

        self.channel_meme_dump = await guild.create_text_channel(
            name="meme-dump", category=self.category_community, sync_permissions=True
        )

        # Setup Debate Category
        self.category_debate = await guild.create_category(
            name="Debate", overwrites=generate_overwrite(ctx, self.roles, "debate")
        )

        # Setup Logs Category
        self.category_logs = await guild.create_category(
            name="Logs", overwrites=generate_overwrite(ctx, self.roles, "logs")
        )

        self.channel_moderator_actions = await guild.create_text_channel(
            name="moderator-actions", category=self.category_logs, sync_permissions=True
        )

        self.channel_message_deletion = await guild.create_text_channel(
            name="message-deletion", category=self.category_logs, sync_permissions=True
        )

        self.channel_message_edits = await guild.create_text_channel(
            name="message-edits", category=self.category_logs, sync_permissions=True
        )

        self.channel_ban_unban = await guild.create_text_channel(
            name="ban-unban", category=self.category_logs, sync_permissions=True
        )

        self.channel_nicknames = await guild.create_text_channel(
            name="nicknames", category=self.category_logs, sync_permissions=True
        )

        self.channel_join_leave = await guild.create_text_channel(
            name="join-leave", category=self.category_logs, sync_permissions=True
        )

        self.channel_automod = await guild.create_text_channel(
            name="automod", category=self.category_logs, sync_permissions=True
        )

        self.channel_channels = await guild.create_text_channel(
            name="channels", category=self.category_logs, sync_permissions=True
        )

        self.channel_invites = await guild.create_text_channel(
            name="invites", category=self.category_logs, sync_permissions=True
        )

        self.channel_roles = await guild.create_text_channel(
            name="roles", category=self.category_logs, sync_permissions=True
        )

        self.channel_voice = await guild.create_text_channel(
            name="voice", category=self.category_logs, sync_permissions=True
        )

        # Create Debate Channels
        for _channel_number in range(1, 21):
            _tc_debate = await guild.create_text_channel(
                name=f"debate-{_channel_number}",
                category=self.category_debate,
                overwrites=generate_overwrite(ctx, self.roles, "debate-#"),
            )

            _vc_debate = await guild.create_voice_channel(
                name=f"Debate {_channel_number}", category=self.category_debate
            )

            overwrite = PermissionOverwrite(view_channel=False)
            if _channel_number != 1:
                await _vc_debate.set_permissions(
                    self.roles["role_citizen"], overwrite=overwrite
                )

                await _vc_debate.set_permissions(
                    self.roles["role_member"], overwrite=overwrite
                )

            _channel_ids = {
                f"tc_debate_{_channel_number}": _tc_debate.id,
                f"vc_debate_{_channel_number}": _vc_debate.id,
            }
            await self.db.upsert(guild, **_channel_ids)

        # Update Database
        await self.db.upsert(
            guild,
            category_information=self.category_information.id,
            tc_rules=guild.rules_channel.id,
            tc_about=self.channel_about.id,
            tc_verification=self.channel_verification.id,
            tc_announcements=self.channel_announcements.id,
            tc_community_updates=guild.public_updates_channel.id,
            category_moderation=self.category_moderation.id,
            tc_director_commands=self.channel_director_commands.id,
            tc_mod_commands=self.channel_mod_commands.id,
            tc_isolation=self.channel_isolation.id,
            category_interface=self.category_interface.id,
            tc_debate_feed=self.channel_debate_feed.id,
            tc_commands=self.channel_commands.id,
            category_community=self.category_community.id,
            tc_general=self.channel_general.id,
            tc_serious=self.channel_serious.id,
            tc_meme_dump=self.channel_meme_dump.id,
            category_debate=self.category_debate.id,
            category_logs=self.category_logs.id,
            tc_moderator_actions=self.channel_moderator_actions.id,
            tc_message_deletion=self.channel_message_deletion.id,
            tc_message_edits=self.channel_message_edits.id,
            tc_ban_unban=self.channel_ban_unban.id,
            tc_nicknames=self.channel_nicknames.id,
            tc_join_leave=self.channel_join_leave.id,
            tc_automod=self.channel_automod.id,
            tc_channels=self.channel_channels.id,
            tc_invites=self.channel_invites.id,
            tc_roles=self.channel_roles.id,
            tc_voice=self.channel_voice.id,
        )

        # Confirm database has been updated.
        response = discord.Embed(color=0x77B255, title="✅ Channels Updated")
        await progress_message.edit(embed=response, delete_after=30)

    @commands.command(
        name="enable-debates",
        brief="Enable the 'Debates' cog.",
        help="This command will check if all the required channels and roles "
        "are available for the bot to use. If it is successful in "
        "confirming the same, then it will enable the 'Debates' cog.",
    )
    async def enable_debates(self, ctx):
        # Indicate command is running.
        title = f"🔍 Enabling Debates"
        response = discord.Embed(color=0x696969, title=title)
        progress_message = await ctx.channel.send(embed=response)

        if "Debate" in self.bot.cogs:
            if self.bot.cogs["Debate"].enabled:
                response = discord.Embed(title="❌ Debates Already Enabled ❌")
                await ctx.send(embed=response)
                return

        roles_set_up = await self.check_roles(
            ctx, message="Cannot enable debates without roles set up."
        )

        # Exit early if roles are not set up
        if not roles_set_up:
            await progress_message.delete()
            return

        channels_set_up = await self.check_channels(
            ctx, message="Cannot enable debates without channels set up."
        )

        if not channels_set_up:
            await progress_message.delete()
            return

        guild = ctx.guild

        for _channel_number in range(1, 21):
            _tc_debate = await self.db.get(guild, state=f"tc_debate_{_channel_number}")

            _vc_debate = await self.db.get(guild, state=f"vc_debate_{_channel_number}")

            self.debate_room_maps.append((_tc_debate, _vc_debate))

        elo_ratings = [2800, 2600, 2400, 2200, 2000, 1800, 1600, 800, 400, 100]
        role_ids = []
        for role in list(self.roles.keys())[5:15]:
            role_ids.append(self.roles[role].id)
        self.elo_role_maps = dict(zip(elo_ratings, role_ids))

        allowed_debate_channels = [i for (i, k) in self.debate_room_maps]
        allowed_misc_channels = [
            self.channel_director_commands,
            self.channel_mod_commands,
            self.channel_commands,
        ]

        self.bot.add_cog(
            DebateRooms(
                self.bot,
                guild,
                self.debate_room_maps,
                self.elo_role_maps,
                allowed_debate_channels,
                allowed_misc_channels,
            )
        )

        await self.bot.cogs["Debate"].debates_enabled()

        # Confirm Debates is Enabled
        response = discord.Embed(color=0x77B255, title="✅ Debates Enabled")
        await progress_message.edit(embed=response, delete_after=30)

    @commands.command(
        name="disable-debates",
        brief="Disable the 'Debates' cog.",
        help="This command will disable the 'Debates' cog and launch all exit "
        "mechanisms associated with the same cog.",
    )
    async def disable_debates(self, ctx):
        # Indicate command is running.
        title = f"🔍 Disabling Debates"
        response = discord.Embed(color=0x696969, title=title)
        progress_message = await ctx.channel.send(embed=response)

        if "Debate" in self.bot.cogs:
            if self.bot.cogs["Debate"].enabled:
                await self.bot.cogs["Debate"].debates_disabled()

            self.bot.remove_cog("Debate")

        # Confirm debates is enabled
        response = discord.Embed(color=0x77B255, title="✅ Debates Disabled")
        await progress_message.edit(embed=response, delete_after=30)

    @commands.has_role("Staff")
    @commands.command(
        name="lockdown",
        brief="Locks the entire server down during downtime issues.",
        help="This commands locks down the whole server from being used"
        "by all members except staff. Should only be used when all of the "
        "moderation bots go down.",
    )
    async def lockdown(self, ctx):
        await self.channels["tc_commands"].set_permissions(
            self.roles["role_member"], overwrite=lockdown_permissions
        )
        await self.channels["tc_commands"].set_permissions(
            self.roles["role_citizen"], overwrite=lockdown_permissions
        )
        await self.channels["category_community"].set_permissions(
            self.roles["role_member"], overwrite=lockdown_permissions
        )
        await self.channels["category_community"].set_permissions(
            self.roles["role_citizen"], overwrite=lockdown_permissions
        )

        await self.channels["category_debate"].set_permissions(
            self.roles["role_member"], overwrite=lockdown_debate_member_perms
        )

        await self.channels["category_debate"].set_permissions(
            self.roles["role_citizen"], overwrite=lockdown_citizen_general_perms
        )

        for _channel_num in range(1, 21):
            vc = discord.utils.get(
                ctx.guild.voice_channels, name=f"Debate {_channel_num}"
            )
            tc = discord.utils.get(
                ctx.guild.text_channels, name=f"debate-{_channel_num}"
            )
            await tc.set_permissions(
                self.roles["role_member"],
                create_instant_invite=False,
                manage_channels=False,
                add_reactions=False,
                read_messages=False,
                view_channel=False,
                send_messages=False,
                send_tts_messages=False,
                manage_messages=False,
                embed_links=False,
                attach_files=False,
                read_message_history=True,
                mention_everyone=False,
                external_emojis=False,
                manage_permissions=False,
                manage_webhooks=False,
            )
            await tc.set_permissions(
                self.roles["role_citizen"],
                create_instant_invite=False,
                manage_channels=False,
                add_reactions=False,
                read_messages=False,
                view_channel=False,
                send_messages=False,
                send_tts_messages=False,
                manage_messages=False,
                embed_links=False,
                attach_files=False,
                read_message_history=True,
                mention_everyone=False,
                external_emojis=False,
                manage_permissions=False,
                manage_webhooks=False,
            )

            if _channel_num != 1:
                await vc.set_permissions(
                    self.roles["role_member"],
                    priority_speaker=False,
                    stream=False,
                    view_channel=False,
                    connect=False,
                    speak=False,
                    mute_members=False,
                    deafen_members=False,
                    move_members=False,
                    use_voice_activation=False,
                    manage_permissions=False,
                )
                await vc.set_permissions(
                    self.roles["role_citizen"],
                    priority_speaker=False,
                    stream=False,
                    view_channel=False,
                    connect=False,
                    speak=False,
                    mute_members=False,
                    deafen_members=False,
                    move_members=False,
                    use_voice_activation=False,
                    manage_permissions=False,
                )
            else:
                await vc.set_permissions(
                    self.roles["role_member"],
                    priority_speaker=False,
                    stream=False,
                    view_channel=True,
                    connect=False,
                    speak=False,
                    mute_members=False,
                    deafen_members=False,
                    move_members=False,
                    use_voice_activation=False,
                    manage_permissions=False,
                )
                await vc.set_permissions(
                    self.roles["role_citizen"],
                    priority_speaker=False,
                    stream=False,
                    view_channel=True,
                    connect=False,
                    speak=False,
                    mute_members=False,
                    deafen_members=False,
                    move_members=False,
                    use_voice_activation=False,
                    manage_permissions=False,
                )

        await self.bot.cogs["Debate"].lockdown_cancel_all_matches()

    @commands.has_role("Director")
    @commands.command(
        name="reopen",
        brief="Unlocks the server for public use.",
        help="This commands unlocks the server for public use. It should only be used "
        "when at least one of the moderation bots are back up. Only directors can"
        "use this command.",
    )
    async def reopen(self, ctx):
        await self.channels["tc_commands"].edit(
            overwrites=generate_overwrite(ctx, self.roles, "commands")
        )
        await self.channels["category_community"].edit(
            overwrites=generate_overwrite(ctx, self.roles, "community")
        )
        await self.channels["tc_general"].edit(sync_permissions=True)
        await self.channels["tc_serious"].edit(sync_permissions=True)
        await self.channels["tc_meme_dump"].edit(sync_permissions=True)
        await self.channels["category_debate"].edit(
            overwrites=generate_overwrite(ctx, self.roles, "debate")
        )

        for _channel_num in range(1, 21):
            vc = discord.utils.get(
                ctx.guild.voice_channels, name=f"Debate {_channel_num}"
            )
            tc = discord.utils.get(
                ctx.guild.text_channels, name=f"debate-{_channel_num}"
            )
            await vc.edit(sync_permissions=True)
            overwrite = PermissionOverwrite(view_channel=False)
            if _channel_num != 1:
                await vc.set_permissions(
                    self.roles["role_citizen"], overwrite=overwrite
                )

                await vc.set_permissions(self.roles["role_member"], overwrite=overwrite)
            await tc.set_permissions(
                self.roles["role_member"], overwrite=_debate_tc_member_permissions
            )
            await tc.set_permissions(
                self.roles["role_citizen"], overwrite=_debate_tc_citizen_permissions
            )

    @commands.has_role("Engineering")
    @commands.command(
        name="quit",
        brief="Quit the bot and logout of bot account.",
        help="This command will disable all associated cogs, quit the "
        "process and log out of the bot account.",
    )
    async def quit(self, ctx):
        if "Debate" in self.bot.cogs:
            pass
        else:
            await self.bot.logout()
        if self.bot.cogs["Debate"].enabled:
            await self.bot.cogs["Debate"].debates_disabled()
        await self.bot.logout()
