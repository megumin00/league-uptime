# League-Uptime
a funny little project to track how long someone has been playing league of legends for discord.
Now includes/is planning to add functions to track user activity in general and aims to track sleep schedules, spotify activity and more.

## Dependencies

-   `discord.py`  -- library to interact with the discord API
-   `json`        -- to read json files (config & secret)
-   `asyncio`     -- to run code asynchronously 
-   `datetime`    -- time related items

## TODOs
1. fix bug with custom status and logging
2. add discord status tracking functions (online, dnd, idle, offline)
3. base sleep tracker on discord status tracking
4. upload logged statistics to a server, whether that is to a google spreadsheet or to a personal server via ssh & scp
5. clean up code (rewrite main and commands.cog), clean up events

## License
GPL 3.0

## Contributors
suwa
