import asyncio
import datetime
from queue import PriorityQueue
from typing import Optional, Union

import discord
from discord import Member, PermissionOverwrite
from discord.ext import commands
from discord.ext.commands import BucketType

from plugins.debate.rooms.data import DebateRoom, Participant, Topic


def only_debate_channels():
    def predicate(ctx):
        return ctx.channel.id in ctx.cog.allowed_debate_channels

    return commands.check(predicate)


def only_command_channel():
    def predicate(ctx):
        return ctx.channel.id == ctx.cog.channels["tc_debate_feed"].id

    return commands.check(predicate)


def only_command_and_debate_channels():
    def predicate(ctx):
        channels = list(ctx.cog.allowed_debate_channels)
        channels.append(ctx.cog.channels["tc_debate_feed"].id)
        return ctx.channel.id in channels

    return commands.check(predicate)


def only_misc_channels():
    def predicate(ctx):
        return ctx.channel.id in ctx.cog.allowed_misc_channels

    return commands.check(predicate)


def only_misc_and_debate_channels():
    def predicate(ctx):
        return (
            ctx.channel.id
            in ctx.cog.allowed_misc_channels + ctx.cog.allowed_debate_channels
        )

    return commands.check(predicate)


def only_misc_debate_command_channels():
    def predicate(ctx):
        channels = list(ctx.cog.allowed_debate_channels)
        channels.append(ctx.cog.channels["tc_commands"].id)
        return ctx.channel.id in (ctx.cog.allowed_misc_channels + channels)

    return commands.check(predicate)


def disabled_while_concluding():
    def predicate(ctx):
        room_number = ctx.cog.get_room_number(ctx.channel)
        room = ctx.cog.get_room(room_number)

        if room is None:
            return True

        if room.match is None:
            return True

        if room.match.concluding:
            return False
        else:
            return True

    return commands.check(predicate)


class DebateRooms(commands.Cog, name="Debate"):
    def __init__(
        self,
        bot,
        guild,
        debate_room_maps: list,
        elo_role_maps: dict,
        allowed_debate_channels: list,
        allowed_misc_channels: list,
    ):
        self.bot = bot
        self.logger = self.bot.logger
        self.db = self.bot.db

        self.interface_messages = []
        self.exiting = False

        # Data
        self.guild = guild
        self.roles = self.bot.cogs["Server Setup"].roles
        self.debate_rooms = []
        self.debate_room_maps = debate_room_maps
        self.channels = self.bot.cogs["Server Setup"].channels
        self.elo_role_maps = elo_role_maps
        self.allowed_debate_channels = allowed_debate_channels
        self.allowed_misc_channels = allowed_misc_channels
        self.enabled = False

        # Implementation Junk
        self.debate_room_tcs = []

        # Room Visibility
        self.empty_rooms = PriorityQueue(maxsize=0)
        self.non_empty_rooms = PriorityQueue(maxsize=0)
        self.invisible_rooms = PriorityQueue(maxsize=0)
        self.visible_rooms = PriorityQueue(maxsize=0)
        self.empty_invisible_rooms = PriorityQueue(maxsize=0)
        self.empty_visible_rooms = PriorityQueue(maxsize=0)
        self.non_empty_invisible_rooms = PriorityQueue(maxsize=0)
        self.non_empty_visible_rooms = PriorityQueue(maxsize=0)

        # Tasks
        self.vc_visibility_task = self.bot.loop.create_task(self.voice_channel_update())

    @commands.Cog.listener()
    async def on_ready(self):
        await self.debates_enabled()

    async def debates_enabled(self):
        for mapping in self.debate_room_maps:
            tc = self.bot.get_channel(mapping[0])
            vc = self.bot.get_channel(mapping[1])
            self.debate_rooms.append(
                DebateRoom(
                    self.debate_room_maps.index(mapping) + 1,
                    tc,  # Text Channel
                    vc,  # Voice Channel
                )
            )

        self.debate_room_tcs = [room.tc for room in self.debate_rooms]
        await self.delete_recent_messages()
        for room in self.debate_rooms:
            message = await self.send_embed_message(room.number)
            self.interface_messages.append(message)

        self.enabled = True

    # Convenience Methods
    def get_room_number(
        self, channel: Union[discord.TextChannel, discord.VoiceChannel]
    ):
        """Get a room number from a TextChannel or VoiceChannel ID."""
        try:
            number = list(
                filter(lambda x: x.number_from_channel(channel), self.debate_rooms)
            )[0].number
            return number
        except IndexError as e_info:
            return None

    def get_room(self, room_num: int):
        """Get a room from a room number."""
        try:
            room = list(filter(lambda x: x.number == room_num, self.debate_rooms))[0]
            return room
        except IndexError as e_info:
            return None

    def get_vc_from_tc(self, tc: discord.TextChannel) -> discord.VoiceChannel:
        """Get a VoiceChannel from a TextChannel."""
        vc = list(filter(lambda x: x.tc == tc, self.debate_rooms))[0].vc
        return vc

    def get_tc_from_vc(self, vc: discord.VoiceChannel) -> discord.TextChannel:
        """Get a TextChannel from a Voice Channel."""
        tc = list(filter(lambda x: x.vc == vc, self.debate_rooms))[0].tc
        return tc

    def check_debate_vc(self, vc: discord.VoiceChannel) -> bool:
        """Ensure VoiceChannel is a debate room."""
        return vc in [room.vc for room in self.debate_rooms]

    # End of Convenience Methods

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            # Do nothing if the message is persistent embed
            if len(message.embeds) > 0:
                if message.embeds[0].title.startswith("Debate Room"):
                    return

        if message.channel in self.debate_room_tcs:
            # Get number
            room_num = self.get_room_number(message.channel)

            # Delete interface message
            index = room_num - 1
            im_del = self.interface_messages[index]
            try:
                await im_del.delete()
            except discord.errors.NotFound as e_info:
                return

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.channel in self.debate_room_tcs:
            # Add interface message when embed is deleted
            if message.id in [i.id for i in self.interface_messages]:
                index = self.get_room_number(message.channel) - 1
                if not self.exiting:
                    im = await self.add_interface_message(index)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        for message in messages:
            if message.channel in self.debate_room_tcs:
                # Add interface message when embed is deleted
                if message.id in [i.id for i in self.interface_messages]:
                    index = self.get_room_number(message.channel) - 1
                    if not self.exiting:
                        im = await self.add_interface_message(index)

    async def delete_recent_messages(self):
        """Delete most recent messages sent by the bot account."""
        for room in self.debate_rooms:
            tc = room.tc
            async for message in tc.history(limit=100):
                if message.author == self.bot.user:
                    await message.delete()

    def get_embed_message(self, room_num):
        response = discord.Embed(
            color=0xEB6A5C,
            title=f"Debate Room {room_num}",
            description="Set channel topics democratically and vote for "
            "the best debater. Start a debate to unmute yourself.",
        )
        return response

    async def send_embed_message(self, room_num):
        embed = self.get_embed_message(room_num)

        topic_updated = self.get_room(room_num).set_current_topic()
        current_topic = self.get_room(room_num).current_topic
        if current_topic:
            embed.add_field(name="**Topic**: ", value=f"{current_topic}")
        text_channel = self.bot.get_channel(list(self.debate_room_tcs)[room_num - 1].id)
        message = await text_channel.send(embed=embed)
        return message

    async def add_interface_message(self, index):
        room_num = index + 1
        im_add = await self.send_embed_message(room_num)
        self.interface_messages[index] = im_add
        return self.interface_messages

    async def update_im(self, room_num):
        index = room_num - 1
        im = self.interface_messages[index]
        embed = self.get_embed_message(room_num)
        topic = self.get_room(room_num).current_topic
        if topic:
            embed.add_field(
                name="**Topic**: ", value=f"{self.get_room(room_num).current_topic}"
            )
        try:
            await im.edit(embed=embed)
        except discord.errors.NotFound as e_info:
            return

    def check_in_debate(self, ctx):
        """Check if someone is in the corresponding TextChannel or
        VoiceChannel to allow a command.
        """
        tc = ctx.message.channel
        if not (tc in [room.tc for room in self.debate_rooms]):
            return False
        vc = self.get_vc_from_tc(tc)
        if ctx.message.author.voice:
            author_vc = ctx.message.author.voice.channel
        else:
            return False
        return vc == author_vc

    async def conclude_debate(self, room, debaters):
        for debater in debaters:
            # Mute
            if debater.member in room.vc.members:
                await debater.member.edit(mute=True)

        for debater in debaters:
            await room.vc.set_permissions(debater.member, overwrite=None)

        embed = discord.Embed(
            title="⏸ Debate concluding..",
            description="ELO ratings are being updated. "
            "Debate specific commands will not run.",
        )

        check_voters = room.match.check_voters()
        if not check_voters:
            debaters = []

        if debaters:
            await room.tc.send(embed=embed, delete_after=60)

        for debater in debaters:
            await self.db.upsert(debater.member, elo=debater.elo_post)

            debate_feed = self.channels["tc_debate_feed"]
            embed = discord.Embed(
                title="ELO Rating Change",
            )
            embed.set_footer(
                text=debater.member.display_name,
                icon_url=debater.member.avatar_url,
            )
            embed.add_field(name="Before: ", value=f"{debater.elo_pre}")
            embed.add_field(name="After: ", value=f"{debater.elo_post}")
            await debate_feed.send(embed=embed)

            for key, val in self.elo_role_maps.items():
                guild = room.vc.guild
                if guild.get_member(debater):
                    await debater.member.remove_roles(
                        debater.member.guild.get_role(self.elo_role_maps[key]),
                        reason="Automatically removed at end of match.",
                    )

            for key, val in self.elo_role_maps.items():
                if key < debater.elo_post:
                    guild = room.vc.guild
                    if guild.get_member(debater):
                        await debater.member.add_roles(
                            debater.member.guild.get_role(self.elo_role_maps[key]),
                            reason="Automatically added at the end of a match.",
                        )
                    break

        embed = discord.Embed(
            title="✅ Debate concluded.",
            description="ELO ratings have been updated.",
        )
        if not check_voters:
            embed.description = (
                "ELO ratings have not been updated due to lack of voters."
            )
        room.match = None  # Clear match
        if debaters:
            await room.tc.send(embed=embed)

    async def update_topic(self, room):
        """Update topic of room from current topic."""
        if len(room.vc.members) == 0:
            current_topic = None
            topic_updated = False
        else:
            topic_updated = room.set_current_topic()
            current_topic = room.current_topic

        match = room.match

        self.logger.debug(f"Topics: {room.topics}")
        if current_topic is not None:
            if not match:
                topic_updated = room.set_current_topic()
                current_topic = room.current_topic
                room.start_match(current_topic)
                await self.update_im(room.number)
            else:
                for member in room.vc.members:
                    await room.vc.set_permissions(member, overwrite=None)

                if not room.match:
                    return

                # Do nothing if there are no voters
                if not room.match.check_voters():
                    debaters = room.match.get_debaters()

                    if not topic_updated:
                        return

                    # Mute debaters early
                    for debater in debaters:
                        # Remove overwrite from VC and mute
                        await room.vc.set_permissions(debater.member, overwrite=None)
                        if debater.member in room.vc.members:
                            await debater.member.edit(mute=True)
                    return

                debaters = []
                if match.concluding is False and match.concluded is False:
                    if topic_updated:

                        debaters = room.stop_match()

                        # Mute debaters early
                        for debater in debaters:
                            # Remove overwrite from VC and mute
                            await room.vc.set_permissions(
                                debater.member, overwrite=None
                            )
                            if debater.member in room.vc.members:
                                await debater.member.edit(mute=True)

                        match.concluding = True
                        await self.conclude_debate(room, debaters)
                        match.concluding = False
                        match.concluded = True

                        topic_updated = room.set_current_topic()
                        current_topic = room.current_topic
                        room.start_match(current_topic)
                        await self.update_im(room.number)
                        for member in room.vc.members:
                            await member.edit(mute=True)
                elif match.concluding is False and match.concluded is True:
                    topic_updated = room.set_current_topic()
                    current_topic = room.current_topic
                    await self.update_im(room.number)
                    return
                elif match.concluding is True and match.concluded is False:
                    topic_updated = room.set_current_topic()
                    current_topic = room.current_topic
                    await self.update_im(room.number)
                    return

        topic_updated = room.set_current_topic()
        current_topic = room.current_topic
        await self.update_im(room.number)

    @only_debate_channels()
    @disabled_while_concluding()
    @commands.command(
        name="topic",
        brief="Set or vote for a topic in a debate room.",
        help="Set a topic in an empty debate room if you're the first setter. "
        "If you're not the first to set the topic, then vote on any "
        "user's topic or propose your own. A successful topic change "
        "will cause the ELO ratings to be calculated for debaters.",
    )
    async def topic(
        self, ctx, member: Union[Member, str], *, message: commands.clean_content = ""
    ):
        room = self.get_room(self.get_room_number(ctx.channel))

        # Exit if not in a debate room
        if not self.check_in_debate(ctx):
            return

        if isinstance(member, Member):

            if self.check_debate_vc(self.get_vc_from_tc(ctx.channel)):
                topic = room.vote_topic(voter=ctx.author, candidate=member)
        else:
            if len(str(message)) > 1024:
                embed = discord.Embed(title="❌ Topic is longer than 1024 characters! ❌")
                await ctx.channel.send(embed=embed, delete_after=20)
                return
            else:
                topic_updated = room.add_topic(
                    Topic(
                        member=ctx.author,
                        message=f"{member} {str(message)}",  # Look carefully
                    )
                )
                if topic_updated:
                    embed = discord.Embed(
                        title="⚠️ Votes on your topic have been reset "
                        "because you updated it! ⚠️"
                    )
                    await ctx.channel.send(embed=embed, delete_after=10)
        await self.update_topic(room)

    async def make_vc_visible(self, vc):
        await vc.edit(sync_permissions=True)

    async def make_vc_invisible(self, vc):
        overwrite = PermissionOverwrite(view_channel=False)
        await vc.set_permissions(self.roles["role_citizen"], overwrite=overwrite)
        await vc.set_permissions(self.roles["role_member"], overwrite=overwrite)

    def vc_is_visible(self, vc):
        return vc.permissions_synced

    def vc_is_empty(self, vc):
        return len(vc.members) == 0

    async def voice_channel_update(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.empty_rooms = PriorityQueue(maxsize=0)
            self.non_empty_rooms = PriorityQueue(maxsize=0)
            self.invisible_rooms = PriorityQueue(maxsize=0)
            self.visible_rooms = PriorityQueue(maxsize=0)
            self.empty_invisible_rooms = PriorityQueue(maxsize=0)
            self.empty_visible_rooms = PriorityQueue(maxsize=0)
            self.non_empty_invisible_rooms = PriorityQueue(maxsize=0)
            self.non_empty_visible_rooms = PriorityQueue(maxsize=0)

            for room in self.debate_rooms:
                if self.vc_is_empty(room.vc):
                    self.empty_rooms.put(room)
                    if not self.vc_is_visible(room.vc):
                        self.empty_invisible_rooms.put(room)
                    else:
                        self.empty_visible_rooms.put(room)
                else:
                    self.non_empty_rooms.put(room)
                    if not self.vc_is_visible(room.vc):
                        self.non_empty_invisible_rooms.put(room)
                    else:
                        self.non_empty_visible_rooms.put(room)

                if not self.vc_is_visible(room.vc):
                    self.invisible_rooms.put(room)
                else:
                    self.visible_rooms.put(room)

            if self.empty_visible_rooms.empty():
                empty_invisible_room = self.empty_invisible_rooms.get()
                await self.make_vc_visible(empty_invisible_room.vc)
                self.visible_rooms.put(empty_invisible_room)
            else:
                if self.empty_visible_rooms.qsize() > 1:
                    for room in self.empty_visible_rooms.queue[1:]:
                        await self.make_vc_invisible(room.vc)

            await asyncio.sleep(1)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        # Variables
        dr_vcs = [dr.vc for dr in self.debate_rooms]

        # Do nothing if mute event
        if before.mute and not after.mute:
            return
        if not before.mute and after.mute:
            return

        if before.deaf and not after.deaf:
            return
        if not before.deaf and after.deaf:
            return

        if before.self_mute and not after.self_mute:
            return
        if not before.self_mute and after.self_mute:
            return

        if before.self_deaf and not after.self_deaf:
            return
        if not before.self_deaf and after.self_deaf:
            return

        async def join_room():
            self.logger.debug(f"{member} joined: {after.channel}")
            room_after = self.get_room(self.get_room_number(after.channel))
            room_after.add_topic_voter(member)
            room_after.reset_topic_creation(member)

            if room_after.match:
                participant = room_after.match.get_participant(member)
                if participant:
                    participant.session_start = datetime.datetime.utcnow()

            # Make linked text chat visible
            tc_after = self.get_tc_from_vc(after.channel)
            overwrite = PermissionOverwrite(read_messages=True)
            await tc_after.set_permissions(member, overwrite=overwrite)

            await member.edit(mute=True)

        async def leave_room():
            self.logger.debug(f"{member} left: {before.channel}")
            room_before = self.get_room(self.get_room_number(before.channel))
            room_before.remove_topic_voter(member)
            room_before.remove_priority_from_topic(member)
            room_before.remove_obsolete_topic(member)

            active_debaters = []
            if room_before.match:
                participant = room_before.match.get_participant(member)
                if participant:
                    participant.session_end = datetime.datetime.utcnow()
                    participant.update_duration()

                debaters = [d.member for d in room_before.match.get_debaters()]
                for voice_member in before.channel.members:
                    if voice_member in debaters:
                        active_debaters.append(voice_member)

                self.logger.debug(
                    f"Active Debaters (On Leave Room):"
                    f" {[a.name for a in active_debaters]}"
                )
                self.logger.debug(
                    f"# of Active Debaters (On Leave Room): {len(active_debaters)}"
                )

                if len(active_debaters) <= 1:
                    if room_before.match.concluding or room_before.match.concluded:
                        pass
                    else:
                        room_before.match.concluding = True
                        await self.conclude_debate(
                            room_before, debaters=room_before.stop_match()
                        )

            # Remove overwrite from VC
            await room_before.vc.set_permissions(member, overwrite=None)

            # Make linked text chat invisible
            tc_before = self.get_tc_from_vc(before.channel)
            await tc_before.set_permissions(member, overwrite=None)

            # Delete if not working
            await self.update_topic(room_before)

        async def switch_room():
            # Join Room
            self.logger.debug(f"{member} joined: {after.channel}")
            room_after = self.get_room(self.get_room_number(after.channel))
            room_after.add_topic_voter(member)
            room_after.reset_topic_creation(member)

            # Make linked text chat visible
            tc_after = self.get_tc_from_vc(after.channel)
            overwrite = PermissionOverwrite(read_messages=True)
            await tc_after.set_permissions(member, overwrite=overwrite)

            # Leave Room
            self.logger.debug(f"{member} left: {before.channel}")
            room_before = self.get_room(self.get_room_number(before.channel))
            room_before.remove_topic_voter(member)
            room_before.remove_priority_from_topic(member)
            room_before.remove_obsolete_topic(member)

            active_debaters = []
            if room_before.match:
                participant = room_before.match.get_participant(member)
                if participant:
                    participant.session_end = datetime.datetime.utcnow()
                    participant.update_duration()

                debaters = [d.member for d in room_before.match.get_debaters()]
                for voice_member in before.channel.members:
                    if voice_member in debaters:
                        active_debaters.append(voice_member)

                self.logger.debug(
                    f"Active Debaters (On Switch Out): "
                    f"{[a.name for a in active_debaters]}"
                )
                self.logger.debug(
                    f"# of Active Debaters (On Switch Out): {len(active_debaters)}"
                )

                if len(active_debaters) <= 1:
                    if room_before.match.concluding or room_before.match.concluded:
                        pass
                    else:
                        room_before.match.concluding = True
                        await self.conclude_debate(
                            room_before, debaters=room_before.stop_match()
                        )

            # Remove overwrite from VC
            await room_before.vc.set_permissions(member, overwrite=None)

            # Make linked text chat invisible
            tc_before = self.get_tc_from_vc(before.channel)
            await tc_before.set_permissions(member, overwrite=None)

            # Mute User
            await member.edit(mute=True)

            # Delete if not working
            await self.update_topic(room_before)

        # If member joins a debate room
        if before.channel is None and after.channel in dr_vcs:
            await join_room()
            return
        # If member leaves a debate room
        if before.channel in dr_vcs and after.channel is None:
            await leave_room()
            return

        if after.channel:
            after_list = list(dr_vcs)
            after_list.remove(after.channel)
        else:
            return

        if before.channel:
            before_list = list(dr_vcs)
            before_list.remove(before.channel)
        else:
            return

        if before.channel in after_list and after.channel in before_list:
            await switch_room()
            return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
        await self.db.upsert(member, elo=1500)
        await member.add_roles(
            member.guild.get_role(self.elo_role_maps[800]),
            reason="Automatically added since a new user.",
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        document = await self.db[self.db.database].MemberStates.find_one(
            {"member_id": member.id}
        )
        if document:
            await self.db[self.db.database].MemberStates.delete_one(
                {"member_id": member.id}
            )

    @only_debate_channels()
    @disabled_while_concluding()
    @commands.has_any_role("Staff", "Director", "Moderator")
    @commands.command(
        name="remove-topic",
        brief="Remove a topic from a debate room.",
        help="This command will remove the topic a user has proposed. If an "
        "active topic is removed then ELO ratings for that debate will be "
        "calculated.",
    )
    async def remove_topic(self, ctx, member: Optional[Member]):
        room_num = self.get_room_number(ctx.channel)
        room = None
        if room_num:
            room = self.get_room(room_num)
        if room:
            if member:
                topic = room.topic_from_member(member)
            else:
                topic = room.current_topic
            if room.match:
                if topic == room.match.topic:
                    for current_member in room.vc.members:
                        await current_member.edit(mute=True)
            if member:
                room.remove_topic(member)
            else:
                room.remove_topic(room.current_topic.author)
            room.match = None  # Clear match
            await self.update_topic(room)

    @commands.has_role("Engineering")
    @commands.command(
        name="hard-reset-elo-ratings",
        brief="Permanently reset the ELO ratings of users.",
        help="This command will purge the database of all ELO ratings and "
        "give them a default rating of 1500.",
    )
    async def reset_scores(self, ctx):
        guild = ctx.guild

        # Count humans
        count = 0
        for member in guild.members:
            if member.bot:
                continue

            count += 1

        response = discord.Embed(color=0x696969, title=f"🔍 Processing {count} members.")
        message = await ctx.send(embed=response)

        count = 0
        for member in guild.members:
            if member.bot:
                continue

            await self.db.upsert(member, elo=1500)
            count += 1

            for key, val in self.elo_role_maps.items():
                await member.remove_roles(
                    member.guild.get_role(self.elo_role_maps[key]),
                    reason="Automatically removed during reset.",
                )

            title = f"🔍 Processed {count} members."
            if count % 5 == 0:
                response = discord.Embed(color=0x696969, title=title)
                await message.edit(embed=response)

        response = discord.Embed(
            color=0x77B255, title="✅ All ELO scores have been reset."
        )
        await message.edit(embed=response, delete_after=10)

    @commands.has_role("Engineering")
    @commands.command(
        name="setup-elo",
        brief="Initialize ELO ratings in a new server.",
        help="This command will give the default ELO rating to users and "
        "setup default initialization procedures for ELO ratings.",
    )
    async def setup_elo(self, ctx):
        guild = ctx.guild

        # Count humans
        count = 0
        for member in guild.members:
            if member.bot:
                continue

            count += 1

        response = discord.Embed(color=0x696969, title=f"🔍 Processing {count} members.")
        message = await ctx.send(embed=response)
        count = 0
        for member in guild.members:
            if member.bot:
                continue
            await self.db.upsert(member, elo=1500)
            count += 1

            for key, val in self.elo_role_maps.items():
                await member.remove_roles(
                    member.guild.get_role(self.elo_role_maps[key]),
                    reason="Automatically removed during setup.",
                )

            await member.add_roles(
                member.guild.get_role(self.elo_role_maps[800]),
                reason="Automatically added during setup.",
            )

            title = f"🔍 Processed {count} members."
            if count % 5 == 0:
                response = discord.Embed(color=0x696969, title=title)
                await message.edit(embed=response)

        response = discord.Embed(
            color=0x77B255,
            title="✅ ELO ratings have been setup and roles have been assigned.",
        )
        await message.edit(embed=response, delete_after=10)

    @commands.has_role("Engineering")
    @commands.command(
        name="repair-elo",
        brief="Repairs the ELO ratings of buggy users.",
        help="This command will check all users to see if they have missing "
        "ELO ratings, fix their roles and update the database.",
    )
    async def repair_elo(self, ctx):
        guild = ctx.guild

        # Count humans
        count = 0
        for member in guild.members:
            if member.bot:
                continue

            count += 1

        response = discord.Embed(color=0x696969, title=f"🔍 Processing {count} members.")
        message = await ctx.send(embed=response)
        count = 0
        for member in guild.members:
            if member.bot:
                continue
            count += 1
            elo = await self.db.get(member, state="elo")
            if elo:
                for key, val in self.elo_role_maps.items():
                    await member.remove_roles(
                        member.guild.get_role(self.elo_role_maps[key]),
                        reason="Automatically removed during setup.",
                    )

                for key, val in self.elo_role_maps.items():
                    if key < elo:
                        await member.add_roles(
                            member.guild.get_role(self.elo_role_maps[key]),
                            reason="Automatically added during setup.",
                        )
                        break
            else:
                await self.db.upsert(member, elo=1500)
                for key, val in self.elo_role_maps.items():
                    await member.remove_roles(
                        member.guild.get_role(self.elo_role_maps[key]),
                        reason="Automatically removed during setup.",
                    )

                await member.add_roles(
                    member.guild.get_role(self.elo_role_maps[800]),
                    reason="Automatically added during setup.",
                )

            title = f"🔍 Processed {count} members."
            if count % 5 == 0:
                response = discord.Embed(color=0x696969, title=title)
                await message.edit(embed=response)

        response = discord.Embed(
            color=0x77B255,
            title="✅ Missing ELO ratings and roles " "have been assigned.",
        )
        await message.edit(embed=response, delete_after=30)

    @only_misc_debate_command_channels()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.command(
        name="elo",
        brief="Display ELO rating of a user.",
        help="This command will display the current ELO score of a user.",
    )
    async def elo(self, ctx, member: Optional[discord.Member]):
        if member:
            if member.bot:
                return
        if member:
            elo = await self.db.get(member, state="elo")
        else:
            elo = await self.db.get(ctx.author, state="elo")
        if not elo:
            return
        embed = discord.Embed(
            title="Debate ELO Rating",
            description=f"`{str(elo)}`",
        )
        if member:
            embed.set_footer(text=member.display_name, icon_url=member.avatar_url)
        else:
            embed.set_footer(
                text=ctx.author.display_name, icon_url=ctx.author.avatar_url
            )
        await ctx.send(embed=embed)

    @only_debate_channels()
    @disabled_while_concluding()
    @commands.command(
        name="for",
        brief="Set the 'For' position on a topic in a debate room.",
        help="This command will allow you to vote on a debate. You are 'For' "
        "the topic.",
    )
    async def command_for(self, ctx):
        room = self.get_room(self.get_room_number(ctx.channel))

        # Exit if not in a debate room
        if not self.check_in_debate(ctx):
            return

        if not room.check_match():
            embed = discord.Embed(title="❌ No debate running right now. ❌")
            await ctx.send(embed=embed, delete_after=10)
            return

        elo = await self.db.get(ctx.author, state="elo")

        room.match.add_for(
            Participant(
                member=ctx.author, elo=elo, session_start=datetime.datetime.utcnow()
            )
        )

        embed = discord.Embed(title="✅ You are now for the position.")
        await ctx.send(embed=embed, delete_after=10)

    @only_debate_channels()
    @disabled_while_concluding()
    @commands.command(
        name="against",
        brief="Set the 'Against' position on a topic in a debate room.",
        help="This command will allow you to vote on a debate. You are 'Against' "
        "the topic.",
    )
    async def against(self, ctx):
        room = self.get_room(self.get_room_number(ctx.channel))

        # Exit if not in a debate room
        if not self.check_in_debate(ctx):
            return

        if not room.check_match():
            embed = discord.Embed(title="❌ No debate match in progress. ❌")
            await ctx.send(embed=embed, delete_after=10)
            return

        elo = await self.db.get(ctx.author, state="elo")

        room.match.add_against(
            Participant(
                member=ctx.author, elo=elo, session_start=datetime.datetime.utcnow()
            )
        )

        embed = discord.Embed(title="✅ You are now against the position.")
        await ctx.send(embed=embed, delete_after=10)

    @only_debate_channels()
    @disabled_while_concluding()
    @commands.command(
        name="debate",
        brief="Start or join a debate.",
        help="This command will allow you to start or join an existing "
        "debate. You must have already selected a position on a topic "
        "for this command to have any effect.",
    )
    async def debate(self, ctx):
        room = self.get_room(self.get_room_number(ctx.channel))

        # Exit if not in a debate room
        if not self.check_in_debate(ctx):
            return

        if not room.check_match():
            embed = discord.Embed(title="❌ No debate match in progress. ❌")
            await ctx.send(embed=embed, delete_after=10)
            return

        if not room.match.check_participant(ctx.author):
            embed = discord.Embed(
                title="You must choose a position on the topic before "
                "you can debate.",
                description="`$for` - For the topic.\n\n"
                "`$against` - Against the topic.",
            )
            await ctx.send(embed=embed, delete_after=60)
            return

        current_session_start = datetime.datetime.utcnow()
        for participant in room.match.participants:
            participant.session_start = current_session_start

        room.match.add_debater(ctx.author)

        embed = discord.Embed(
            title="✅ You are now a debater on the topic.",
            description="Your ELO rating is at risk. " "Be mindful of what you say.",
        )
        await ctx.send(embed=embed, delete_after=20)
        if self.roles["role_muted"] in ctx.author.roles:
            await ctx.author.edit(mute=True)
        else:
            await ctx.author.edit(mute=False)

    @only_debate_channels()
    @disabled_while_concluding()
    @commands.command(
        name="debate-for",
        aliases=["df"],
        brief="Shortcut to debate for the topic.",
        help="This command has the same affect as taking the 'For' position on a "
        "topic and then starting or joining a debate.",
    )
    async def debate_for(self, ctx):
        room = self.get_room(self.get_room_number(ctx.channel))

        # Exit if not in a debate room
        if not self.check_in_debate(ctx):
            return

        if not room.check_match():
            embed = discord.Embed(title="❌ No debate running right now. ❌")
            await ctx.send(embed=embed, delete_after=10)
            return

        elo = await self.db.get(ctx.author, state="elo")

        room.match.add_for(
            Participant(
                member=ctx.author, elo=elo, session_start=datetime.datetime.utcnow()
            )
        )

        if not room.check_match():
            embed = discord.Embed(title="❌ No debate match in progress. ❌")
            await ctx.send(embed=embed, delete_after=10)
            return

        current_session_start = datetime.datetime.utcnow()
        for participant in room.match.participants:
            participant.session_start = current_session_start

        room.match.add_debater(ctx.author)

        embed = discord.Embed(
            title="✅ You are now a debater for the topic.",
            description="Your ELO rating is at risk. Be mindful of what you say.",
        )
        await ctx.send(embed=embed, delete_after=20)
        if self.roles["role_muted"] in ctx.author.roles:
            await ctx.author.edit(mute=True)
        else:
            await ctx.author.edit(mute=False)

    @only_debate_channels()
    @disabled_while_concluding()
    @commands.command(
        name="debate-against",
        aliases=["da"],
        brief="Shortcut to debate against the topic.",
        help="This command has the same affect as taking the 'Against' position "
        "on a "
        "topic and then starting or joining a debate.",
    )
    async def debate_against(self, ctx):
        room = self.get_room(self.get_room_number(ctx.channel))

        # Exit if not in a debate room
        if not self.check_in_debate(ctx):
            return

        if not room.check_match():
            embed = discord.Embed(title="❌ No debate match in progress. ❌")
            await ctx.send(embed=embed, delete_after=10)
            return

        elo = await self.db.get(ctx.author, state="elo")

        room.match.add_against(
            Participant(
                member=ctx.author, elo=elo, session_start=datetime.datetime.utcnow()
            )
        )

        if not room.check_match():
            embed = discord.Embed(title="❌ No debate match in progress. ❌")
            await ctx.send(embed=embed, delete_after=10)
            return

        current_session_start = datetime.datetime.utcnow()
        for participant in room.match.participants:
            participant.session_start = current_session_start

        room.match.add_debater(ctx.author)

        embed = discord.Embed(
            title="✅ You are now a debater against the topic.",
            description="Your ELO rating is at risk. " "Be mindful of what you say.",
        )
        await ctx.send(embed=embed, delete_after=20)
        if self.roles["role_muted"] in ctx.author.roles:
            await ctx.author.edit(mute=True)
        else:
            await ctx.author.edit(mute=False)

    @only_debate_channels()
    @disabled_while_concluding()
    @commands.command(
        name="vote",
        brief="Vote for who you think won the debate.",
        help="This command will cast a vote for a debater in an active "
        "debate. You can switch votes before the end of a debate.",
    )
    async def vote(self, ctx, member: discord.Member):
        room = self.get_room(self.get_room_number(ctx.channel))

        # Exit if not in a debate room
        if not self.check_in_debate(ctx):
            return

        if not room.check_match():
            embed = discord.Embed(title="❌ No debate match in progress. ❌")
            await ctx.send(embed=embed, delete_after=10)
            return

        if member == ctx.author:
            embed = discord.Embed(title="❌ You cannot vote for yourself dummy. ❌")
            await ctx.send(embed=embed, delete_after=10)
            return

        result = room.match.vote(voter=ctx.author, candidate=member)
        if result is None:
            embed = discord.Embed(
                title="❌ You can only vote for debaters if you take a position. ❌"
            )
            await ctx.send(embed=embed, delete_after=10)
            return
        if result is False:
            embed = discord.Embed(title="❌ You can only vote for debaters. ❌")
            await ctx.send(embed=embed, delete_after=10)
            return
        embed = discord.Embed(title="✅ Your vote has been cast.")
        await ctx.send(embed=embed, delete_after=20)

    @only_debate_channels()
    @disabled_while_concluding()
    @commands.command(
        name="conclude",
        brief="Conclude an active debate.",
        help="This command will end an active debate in a debate room. It "
        "will also cause the calculation of ELO ratings and remove the "
        "topic from the room.",
    )
    async def conclude(self, ctx):
        room = self.get_room(self.get_room_number(ctx.channel))
        match = room.match

        # Exit if not in a debate room
        if not self.check_in_debate(ctx):
            return

        if not room.check_match():
            embed = discord.Embed(title="❌ No debate match in progress. ❌")
            await ctx.send(embed=embed, delete_after=10)
            return

        debaters, concluded, voters = room.vote_conclude(voter=ctx.author)
        self.logger.debug(f"Debaters (On Conclude): {debaters}")
        self.logger.debug(f"Concluded (On Conclude): {concluded}")

        # Do nothing if another conclude command already run
        if concluded is None:
            return
        else:
            embed = discord.Embed(title="✅ Vote to conclude debate cast.")
            await ctx.send(embed=embed, delete_after=10)

        if concluded:
            match.concluding = True
            embed = discord.Embed(
                title="⏸ Debate concluding..",
                description="ELO ratings are being updated.",
            )
            await ctx.send(embed=embed, delete_after=60)
            for debater in debaters:
                # Mute
                if debater.member in room.vc.members:
                    await debater.member.edit(mute=True)

            for debater in debaters:
                await room.vc.set_permissions(debater.member, overwrite=None)

            if voters:
                for debater in debaters:
                    # Update database
                    await self.db.upsert(debater.member, elo=debater.elo_post)

                    debate_feed = self.channels["tc_debate_feed"]
                    embed = discord.Embed(
                        title="ELO Rating Change",
                    )
                    embed.set_footer(
                        text=debater.member.display_name,
                        icon_url=debater.member.avatar_url,
                    )
                    embed.add_field(name="Before: ", value=f"{debater.elo_pre}")
                    embed.add_field(name="After: ", value=f"{debater.elo_post}")
                    await debate_feed.send(embed=embed)

                    # Remove ELO roles
                    for key, val in self.elo_role_maps.items():
                        guild = room.vc.guild
                        if guild.get_member(debater):
                            await debater.member.remove_roles(
                                debater.member.guild.get_role(self.elo_role_maps[key]),
                                reason="Automatically removed at end of match.",
                            )

                    # Add ELO roles
                    for key, val in self.elo_role_maps.items():
                        if key < debater.elo_post:
                            guild = room.vc.guild
                            if guild.get_member(debater):
                                await debater.member.add_roles(
                                    debater.member.guild.get_role(
                                        self.elo_role_maps[key]
                                    ),
                                    reason="Automatically added at the "
                                    "end of a match.",
                                )
                            break

            # Update topic
            current_topic = room.current_topic
            if current_topic:
                await self.update_im(self.get_room_number(room.tc))
                room.remove_topic(current_topic.author)
                room.vote_topic(current_topic.author, current_topic.author)
            else:
                await self.update_im(self.get_room_number(room.tc))

            # Remove voters from data set
            room.remove_conclude_voters()
            room.match = None  # Clear match

            await self.update_topic(room)

            # Send conclude message
            embed = discord.Embed(
                title="✅ Debate concluded.",
                description="ELO ratings have been updated.",
            )
            await ctx.send(embed=embed)
            match.concluding = False
            match.concluded = True

        else:
            if debaters:
                if len(debaters) == 0:
                    embed = discord.Embed(
                        title="❌ Debate not concluded. ❌",
                        description="You cannot conclude a debate with 0 "
                        "participants.",
                    )
                    await ctx.send(embed=embed)

    async def lockdown_cancel_all_matches(self):
        for room in self.debate_rooms:
            if room.match:
                room.match = None
            room.purge_topics()
            index = room.number - 1
            await self.interface_messages[index].edit(
                embed=self.get_embed_message(room_num=room.number)
            )

            for member in room.vc.members:
                await member.move_to(None)
                await room.vc.set_permissions(member, overwrite=None)

                # Make linked text chat invisible
                await room.tc.set_permissions(member, overwrite=None)

            overwrite = PermissionOverwrite(view_channel=False)
            if room.number >= 2:
                await room.vc.set_permissions(
                    self.roles["role_member"], overwrite=overwrite
                )
                await room.vc.set_permissions(
                    self.roles["role_citizen"], overwrite=overwrite
                )

    async def debates_disabled(self):
        self.exiting = True
        for message in self.interface_messages:
            try:
                await message.delete()
            except discord.errors.NotFound as e_info:
                self.bot.logger.debug(
                    f"Interface message during exit process could not be deleted."
                )
        self.enabled = False
