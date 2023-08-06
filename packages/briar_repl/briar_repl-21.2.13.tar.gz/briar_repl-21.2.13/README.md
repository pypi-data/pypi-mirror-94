# briar_repl

python repl cli chat client, to be used with briar-headless:

https://code.briarproject.org/briar/briar/tree/master/briar-headless

### currently it features:
* contact listing
* contact adding
* contact removing
* contact renaming
* contacts pending list
* contacts display online status
* contacts display unread message count (currently per session only)
* direct chat with contacts
* briar link display
* command help

### two modes:
* command mode (blue bottom bar)
* chat mode    (green bottom bar)

commands in chat mode are called by pre-pending `/` so a `/back` or `/exit_chat` brings you back to command mode

commands are auto completed thanks to the amazing prompt_toolkit package

https://github.com/prompt-toolkit/python-prompt-toolkit
