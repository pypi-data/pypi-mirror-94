"""Chiron support for Hangouts"""

from __future__ import print_function, unicode_literals

import asyncio

import hangups #pylint:disable=import-error

from . import engine

def format_user(user):
    """Format a Hangouts User object for display"""
    return "%s %s" % (user.full_name, user.emails)

class HangoutsMessage(engine.Message):
    """Chiron Hangouts protocol class"""
    def __init__(self, client, conv_list, conv_event):
        self._client = client
        self._conv_event = conv_event
        self._conversation = conv_list.get(conv_event.conversation_id)
        self._sender = conv_list._user_list.get_user(conv_event.user_id)
        self._friendly_users = [format_user(user) for user in self._conversation.users]

    def body(self):
        return self._conv_event.text

    def cls(self):
        return self._conv_event.conversation_id

    def instance(self):
        return ""

    def sender(self):
        return format_user(self._sender)

    def recipient(self):
        return self._conversation.name or self._friendly_users

    def is_personal(self):
        return len(self._conversation.users) <= 2

    def skip_message(self):
        return self._sender.is_self

    def send_reply(self, messages):
        segments = []
        newline = hangups.ChatMessageSegment('', segment_type=hangups.SEGMENT_TYPE_LINE_BREAK)

        if messages:
            for title, url in messages:
                # Below would be ideal, but doesn't seem to work. At a guess,
                # Google requires link text match link target (making the
                # link_target parameter kinda redundant, but *shrug*).
                #segments.append(hangups.ChatMessageSegment(seg_body, link_target=url))
                segments.append(hangups.ChatMessageSegment(title))
                segments.append(hangups.ChatMessageSegment(" ("))
                segments.append(hangups.ChatMessageSegment(url, link_target=url))
                segments.append(hangups.ChatMessageSegment(")"))
                segments.append(newline)
            segments = segments[:-1]
        else:
            segments.append(hangups.ChatMessageSegment("No ticket number found in message."))

        if messages or self.is_personal():
            print("  ->", "sending reply with %d segments and %d messages" %
                  (len(segments), len(messages)))
            # Py3.7: switch to asyncio.get_running_loop()
            loop = asyncio.get_event_loop()
            loop.create_task(self._conversation.send_message(segments))

    @classmethod
    def build_processor(cls, match_engine, client):
        """Build message callback"""
        def process(conv_list, conv_event):
            """Hangouts message callback"""
            if isinstance(conv_event, hangups.ChatMessageEvent):
                msg = cls(client, conv_list, conv_event)
                match_engine.process(msg)
        return process

    @classmethod
    def main(cls, match_engine, options):
        """Main function for running Chiron with Hangouts"""
        cookies = hangups.auth.get_auth_stdin(options.hangouts_token)
        client = hangups.Client(cookies)
        event_cb = cls.build_processor(match_engine, client)
        loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(_async_main(event_cb, client),
                                     loop=loop)
        try:
            print("Listening...")
            loop.run_until_complete(task)
        except KeyboardInterrupt:
            task.cancel()
            loop.run_until_complete(task)
        finally:
            loop.close()


async def _async_main(event_cb, client):
    """Run the example coroutine."""
    # Spawn a task for hangups to run in parallel with the handler coroutine.
    task = asyncio.ensure_future(client.connect())

    # Wait for hangups to either finish connecting or raise an exception.
    on_connect = asyncio.Future()
    client.on_connect.add_observer(lambda: on_connect.set_result(None))
    done, _ = await asyncio.wait(
        (on_connect, task), return_when=asyncio.FIRST_COMPLETED
    )
    await asyncio.gather(*done)

    # Run the handler coroutine. Afterwards, disconnect hangups gracefully and
    # yield the hangups task to handle any exceptions.
    try:
        await receive_messages(event_cb, client)
    except asyncio.CancelledError:
        pass
    finally:
        await client.disconnect()
        await task


async def receive_messages(event_cb, client):
    """Setup observer to handle messages"""
    print('loading conversation list...')
    dummy_user_list, conv_list = (
        await hangups.build_user_conversation_list(client)
    )
    conv_list.on_event.add_observer(lambda event: event_cb(conv_list, event))

    print('waiting for chat messages...')
    while True:
        await asyncio.sleep(1)


def main(match_engine, options):
    """Main function for running Chiron with Hangouts"""
    HangoutsMessage.main(match_engine, options)
