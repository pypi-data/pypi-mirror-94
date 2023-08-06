:github_url:

========
Commands
========

All commands are documented in this page. You can do ``$help [command]`` to view help
for a command.

Layout Manager and Server Setup
===============================

+------------------+----------------------------------------------------------------------------+
| $setup-roles     | This command will set up all roles and the associated permissions required |
|                  | by the bot in the server. This command should not be used multiple times   |
|                  | in a period of 24 hrs as you will be rate limited.                         |
+------------------+----------------------------------------------------------------------------+
| $setup-channels  | This command will set up all channels and it's permission required by the  |
|                  | bot in the server.                                                         |
+------------------+----------------------------------------------------------------------------+
| $enable-debates  | This command will check if all the required channels and roles are         |
|                  | available for the bot to use. If it is successful in confirming the same,  |
|                  | then it will enable the 'Debates' cog.                                     |
+------------------+----------------------------------------------------------------------------+
| $disable-debates | This command will disable the 'Debates' cog and launch all exit mechanisms |
|                  | associated with the same cog.                                              |
+------------------+----------------------------------------------------------------------------+
| $lockdown        | This command locks down the whole server from being use by all members     |
|                  | except staff. Should only be used when all of the moderation bots go down. |
+------------------+----------------------------------------------------------------------------+
| $reopen          | This command unlocks the server for public use. It should only be used     |
|                  | when at least one of the moderation bots are back up. Only directors can   |
|                  | use this command.                                                          |
+------------------+----------------------------------------------------------------------------+
| $quit            | This command will disable all associated cogs, quit the process and log    |
|                  | out of the bot account.                                                    |
+------------------+----------------------------------------------------------------------------+


Debate Commands
===============

+---------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Command**               | **Alias** | **Description**                                                                                                                                                                                                                                  |
+---------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| $topic <member> [message] | N/A       | Set a topic in an empty debate room if you're the first setter. If you're not the first to set the topic, then vote on any user's topic or propose your own. A successful topic change will cause the ELO ratings to be calculated for debaters. |
+---------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| $for                      | N/A       | This command will allow you to vote on a debate. You are 'For' the topic.                                                                                                                                                                        |
+---------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| $against                  | N/A       | This command will allow you to vote on a debate. You are 'Against' the topic.                                                                                                                                                                    |
+---------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| $debate                   | N/A       | This command will allow you to start or join an existing debate. You must have already selected a position on a topic for this command to have any effect.                                                                                       |
+---------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| $debate-for               | $df       | This command has the same affect as taking the 'For' position on a topic and then starting or joining a debate.                                                                                                                                  |
+---------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| $debate-against           | $da       | This command has the same affect as taking the 'Against' position on a topic and then starting or joining a debate.                                                                                                                              |
+---------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| $vote <member>            | N/A       | This command will cast a vote for a debater in an active debate. You can switch votes before the end of a debate.                                                                                                                                |
+---------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| $elo [member]             | N/A       | This command will display the current ELO score of a user.                                                                                                                                                                                       |
+---------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| $conclude                 | N/A       | This command will end an active debate in a debate room. It will also cause the calculation of ELO ratings and remove the topic from the room.                                                                                                   |
+---------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| $setup-elo                | N/A       | This command will give the default ELO rating to users and setup default initialization procedures for ELO ratings. Only Engineers can use this command.                                                                                         |
+---------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| $repair-elo               | N/A       | This command will check all users to see if they have missing ELO ratings, fix their roles and update the database.                                                                                                                              |
+---------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| $hard-reset-elo-ratings   | N/A       | This command will purge the database of all ELO ratings and give them a default rating of 1500. Only Engineers can use this command.                                                                                                             |
+---------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| $remove-topic             | N/A       | This command will remove the topic a user has proposed. If an active topic is removed then ELO ratings for that debate will be calculated. Only Staff, Director and Moderator can use this command.                                              |
+---------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
