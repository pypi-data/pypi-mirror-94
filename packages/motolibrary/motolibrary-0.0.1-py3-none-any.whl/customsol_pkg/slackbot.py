# slack_funcs.py

from slack import WebClient
from slack.errors import SlackApiError
import sys

SLACK_BOT_TOKEN = 'xoxb-4950217216-1580739024241-KE4CsYwOouHLxmpuEmk8BYJ4'
client = WebClient(token=SLACK_BOT_TOKEN)
def slack_send_message(channels, messages):
    """
    -------------------------------------------------------
    Sends slack message(s) to specified channel(s)
    Use: slack_send_message(channels, messages))
    -------------------------------------------------------
        channels: list
            contains list of channels to send messages to via slack
        messages: list
            contains list of messages to send
    Returns:
       NONE
    ------------------------------------------------------
    """
    sys.dont_write_bytecode = True
    for channel in channels:
        for message in messages:
            response = client.chat_postMessage(channel=channel, text=message)
    return


def slack_send_file(channels, files, titles):
    """
    -------------------------------------------------------
    Sends file(s) to specified channel(s)
    Use: slack_send_file(channels, files, titles)
    -------------------------------------------------------
        channels: list
            contains list of channels to send messages to via slack
        files: list
            contains list of files to send
        titles: list
            contains list of titles of files; titles shoud correspond to same
            order of items in files list.
    Returns:
       NONE
    ------------------------------------------------------
    """
    for channel in channels:
        i = 0
        for file in files:
            title = titles[i]
            client.files_upload(channels=channel, file=file, title=title)
            i += 1
    return
