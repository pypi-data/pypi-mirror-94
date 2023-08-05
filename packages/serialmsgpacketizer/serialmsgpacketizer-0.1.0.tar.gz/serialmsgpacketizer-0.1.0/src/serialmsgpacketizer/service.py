"""Main classes for serialmsgpacketizer"""
from __future__ import annotations
from typing import cast, Union, Optional, Any
from dataclasses import dataclass, field
import logging


import asyncio


from datastreamcorelib.pubsub import PubSubMessage, Subscription
from datastreamcorelib.datamessage import PubSubDataMessage
from datastreamservicelib.service import SimpleService

LOGGER = logging.getLogger(__name__)


@dataclass
class SerialMsgPacketizerService(SimpleService):
    """Main class for serialmsgpacketizer"""

    _sendertask: Optional[asyncio.Task[Any]] = field(init=False, default=None)

    async def teardown(self) -> None:
        """Called once by the run method before exiting"""
        # Make sure our sender task shuts down
        if self._sendertask:
            if not self._sendertask.done():
                self._sendertask.cancel()
        # Remember to let SimpleServices own teardown work too.
        await super().teardown()

    def reload(self) -> None:
        """Load configs, restart sockets"""
        super().reload()
        # Do something

        # Example task sending messages forever
        self._sendertask = asyncio.create_task(self.example_message_sender("footopic"))

        # Example subscription for receiving messages (specifically DataMessages)
        sub = Subscription(
            self.config["zmq"]["pub_sockets"][0],  # Listen to our own heartbeat
            "HEARTBEAT",
            self.example_success_callback,
            decoder_class=PubSubDataMessage,
            # This is just an example, don't pass metadata you don't intent to use
            metadata={"somekey": "somevalue"},
        )
        self.psmgr.subscribe_async(sub)

    async def example_success_callback(self, sub: Subscription, msg: PubSubMessage) -> None:
        """Callback for the example subscription"""
        # We know it's actually datamessage but the broker deals with the parent type
        msg = cast(PubSubDataMessage, msg)
        LOGGER.info("Got {} (sub.metadata={})".format(msg, sub.metadata))
        # TODO: Do something with the message we got, maybe send some procsessing results out.
        outmsg = PubSubDataMessage(topic="bartopic")
        # Fire-and-forget republish task
        await self._republish_message(outmsg)

    async def _republish_message(self, msg: PubSubDataMessage) -> None:
        """Republish the given message"""
        return await self.psmgr.publish_async(msg)

    async def example_message_sender(self, topic: Union[bytes, str]) -> None:
        """Send messages in a loop, the topic is just an example for passing typed arguments"""
        msgno = 0
        while self.psmgr.default_pub_socket and not self.psmgr.default_pub_socket.closed:
            msgno += 1
            msg = PubSubDataMessage(topic=topic)
            msg.data = {
                "msgno": msgno,
            }
            LOGGER.debug("Publishing {}".format(msg))
            await self.psmgr.publish_async(msg)
            await asyncio.sleep(0.5)
        return None
