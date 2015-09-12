# Copyright (c) 2015 Nicolas JOUANIN
#
# See the file license.txt for copying permission.
import unittest
import asyncio
from hbmqtt.plugins.manager import PluginManager
from hbmqtt.session import Session
from hbmqtt.mqtt.protocol.handler import ProtocolHandler
from hbmqtt.adapters import BufferReader, BufferWriter


class ProtocolHandlerTest(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        self.plugin_manager = PluginManager("hbmqtt.test.plugins", context=None, loop=self.loop)

    def test_init_handler(self):
        s = Session()
        handler = ProtocolHandler(s, self.plugin_manager, loop=self.loop)
        self.assertIs(handler.session, s)
        self.assertIs(handler._loop, self.loop)
        self.assertFalse(handler._puback_waiters)
        self.assertFalse(handler._pubrec_waiters)
        self.assertFalse(handler._pubrel_waiters)
        self.assertFalse(handler._pubcomp_waiters)

    def test_start_stop(self):
        @asyncio.coroutine
        def server_coro(reader, writer):
            pass

        @asyncio.coroutine
        def test_coro():
            s = Session()
            buffer = b''
            s.reader = BufferReader(buffer)
            s.writer = BufferWriter(buffer)
            handler = ProtocolHandler(s, self.plugin_manager, loop=self.loop)
            yield from handler.start()
            yield from handler.stop()
            return handler
        handler = self.loop.run_until_complete(test_coro())