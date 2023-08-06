:github_url:

===========
Quickstart
===========

Follow the `instructions here <https://erin.readthedocs.io/en/latest/manual/usage.html>`_ to setup Erin and the config file for the bot. The config file will look similar to this:

.. code-block:: ini

    [bot]
    token = "jdgkJKkhghgkgskjKJKJ.6-Jq0Hjhskjhsjkh875sbanchaajalfMWg"
    debug = false
    project = "opendebates"
    plugins_folder = "plugins"
    log_type = "Timed"
    log_level = "INFO"


    [database]

    enabled = true
    driver= "mongo"

    uri = "mongodb+srv://argus:abcdefghi1234@cluster0.abcded.mongodb.net/opendebates"
    database = "opendebates"

    [global]

    name = "Argus"
    prefixes = ["$"]
    description = ""

    [help]

    color = 0xEB6A5C
    support_text = """
    Need further help? Send a message to out support bot!
    """

Then start the bot with:

::

   erin start --config config.toml

Next setup an empty server where Community is enabled and a public rules channel is
visible. Run :code:`$setup-roles` in the rules channel the first time you setup the
server. Make sure to not run that command more than once every 24 hours or the bot
will get rate limited for a long time. Once the roles have been set up, run
:code:`$setup-channels` to create the channels for the server. Follow up with
:code:`$enable-debates` to enable debates plugin of the bot.
