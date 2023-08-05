#!/usr/bin/env python3

import asyncio
from collections import deque
from pprint import pprint  # noqa: W0611 F401
from threading import Barrier, Thread

import janus
from box import Box

from .component import Component
from .pipe import Manifold, Message
from .utils import aiter, isdict, islist


class Node(Component):
    """Processes messages."""

    def configure(self, process=None, scale=None, blocking=False,
                  inbox=None, ifilters=None, ofilters=None, outbox=None, **settings):
        if callable(process):
            self.process = process
        self.scale = int(scale or 1)
        self.blocking = self.__class__ is ThreadedNode or blocking
        self.inbox = self._join_pipes(inbox, Inbox)
        self.ifilters = ifilters or PriorityRegistry()
        self.ofilters = ofilters or PriorityRegistry()
        self.outbox = self._join_pipes(outbox, Outbox)
        self.layers = list()
        self.streams = dict()
        return settings

    def __str__(self):
        process_str = ''
        if not hasattr(self.process, 'stub') and not hasattr(self.process, 'overloaded'):
            process_str = f' {self.process}'
        return f'<{self.type} {self.id}{process_str}>'

    def _join_pipes(self, pipes, class_):
        if not isinstance(pipes, dict):
            pipes = dict(default=pipes)
        msgbox = self.workflow.make_component(class_, id=self.id, **pipes)
        for channel, pipe in pipes.items():
            pipe.parent = self  # FIXME: other node overwrites .parent
        return msgbox

    def start(self, *args):
        coroutines = [super().start(*args)]
        self.layers = ([self.inbox] +
                       self.ifilters.ordered() +
                       [self.spawn_processor()] +
                       self.ofilters.ordered() +
                       [self.outbox])
        for layer in self.layers:
            if isinstance(layer, Component):
                coroutines.append(layer.start())
        return asyncio.gather(*coroutines)

    async def test(self, messages):
        self.debug(f'~~~~~~ begin {messages}')
        async for c, m in messages:
            self.debug(f'~~~~~~ message from {messages} {c} {m}')
            yield c, m
            self.debug(f'~~~~~~ yielded from {messages} {c} {m}')
        self.debug(f'~~~~~~ end {messages}')

    async def run(self):
        await super().run()
        for layer in self.layers:
            if isinstance(layer, Component) and hasattr(layer, 'ready'):
                self.debug(f'Waiting on layer {layer} to be ready')
                await layer.ready.wait()
                self.debug(f'Layer {layer} is ready')
        # TODO: handle exceptions, and possibly restart
        if self.running and self.inbox.running:
            stack = self.layers[0]
            for layer in self.layers[1:]:
                stack = layer(stack)
                # stack = layer(self.test(stack))
            self.debug('Processing messages')
            try:
                async for result in stack:
                # async for result in self.test(stack):
                    result
            except Exception:
                self.exception('Node failure')
                raise

            self.debug('Finished processing')

    def spawn_processor(self):
        processor = self.get_processor()
        if self.blocking:
            raise NotImplementedError(f'Node.blocking in {self}')
            # processor = ThreadedProcessor(processor, scale=self.scale)

        if self.scale == 1:
            return processor

        elif self.scale > 1:
            return MultiProcessor(self)

    def get_processor(self):
        if isinstance(self, WithRetry):
            self._retryable = None
            return self._retryable_processor

        return self.processor

    async def _retryable_processor(self, messages, id_=None):
        if self._retryable is None:
            self._retryable = RetryableMessages(self, messages)
        async for channel, message in self.processor(self._retryable, id_):
            yield channel, message

    async def processor(self, messages, id_=None):
        """Process and yield new (channel, message)."""
        async for channel, message in messages:
            yield await self.process(channel, message)

    async def process(self, channel, message):
        raise NotImplementedError(f'process() in {self}')

    process.stub = True

    def drop(self, message):  # TODO: implement message accounting and leak detection
        # self.outbox.drop(message)
        raise NotImplementedError(f'drop() in {self}')

    def merged_settings(self, message, key=None, msgmap=None):
        """Return node settings, with values overridden from the message if present."""
        settings = self.settings.to_dict()
        message = message.to_dict()
        if key:
            settings = settings[key]
            message = message[key]
        if msgmap is None:
            msgmap = list(settings)
        if islist(msgmap):
            msgmap = dict(zip(msgmap, msgmap))
        elif not isdict(msgmap):
            raise TypeError(f'Argument msgmap must be a mapping or a sequence, not {type(msgmap)}')

        return Box(settings, **dict((arg, message[msgarg]) for arg, msgarg in msgmap.items()))


class WithRetry:
    pass


class MultiProcessor:

    def __init__(self, node):
        self.node = node
        self.processor = self.node.get_processor()

    async def feeder(self, messages):
        """Loop through all messages from the inbox and relay them to the input queue."""
        # self.node.debug(f'*** collector feeder running')
        async for channel, message in messages:
            self.pending += 1
            # self.node.debug(f'*** collector feeder got msg [{self.pending}] {message}')
            await self.iqueue.put((channel, message))
            # self.node.debug(f'*** collector feeder sent msg [{self.pending}] {message}')
        # self.node.debug(f'*** collector feeder done')
        self.exhausted = True
        if self.pending > 0:
            await self.finished.wait()
        for i in range(self.node.scale):
            await self.iqueue.put(Message.EOT)
        # self.node.debug(f'*** collector feeder exited')

    async def collector(self, id_):
        """Launch an instance of the node processor, and relay its output to the output queue."""
        # self.node.debug(f'*** collector [{id_}] running')
        async for channel, message in self.processor(aiter(self.iqueue.get, Message.EOT), id_=id_):
            # self.node.debug(f'*** collector [{id_}] got msg {message}')
            await self.oqueue.put((channel, message))
            # self.node.debug(f'*** collector [{id_}] sent msg {message}')
        # self.node.debug(f'*** collector [{id_}] stopped')
        await self.oqueue.put((None, Message.EOT))
        # self.node.debug(f'*** collector [{id_}] exited')

    async def outfeed(self, messages):
        """Launch all processor instances and return an iterator that feeds on the output queue."""
        self.iqueue = asyncio.Queue(maxsize=self.node.scale)  # input queue
        self.oqueue = asyncio.Queue(maxsize=1)                # output queue
        self.finished = asyncio.Event()
        self.exhausted = False
        self.pending = 0  # number of messages currently handled by node processor
        coroutines = [self.node.loop.create_task(self.feeder(messages))]
        for i in range(self.node.scale):
            coroutines.append(self.node.loop.create_task(self.collector(i)))
        running = self.node.scale
        # self.node.debug(f'*** started {running} collectors')
        while running or not self.oqueue.empty():
            channel, message = await self.oqueue.get()
            # self.node.debug(f'*** collector outfeed got msg [{self.pending}] {message}')
            self.oqueue.task_done()
            if message is Message.EOT:
                running -= 1
                # self.node.debug(f'*** a collector ended, left={running}')
            else:
                self.pending -= 1
                if self.pending == 0 and self.exhausted:
                    # self.node.debug(f'*** collector finishing')
                    self.finished.set()
                yield channel, message

            # self.node.debug(f'*** collector outfeed processed msg [{self.pending}] {message}')

        # self.node.debug(f'*** waiting on all collectors')
        for coroutine in coroutines:
            await coroutine
        # self.node.debug(f'*** all collectors ended')

    __call__ = outfeed


class Inbox(Manifold):

    def receive(self):
        raise NotImplementedError(f'receive() in {self}')

    async def receiver(self):
        message = None
        active_channels = 0
        last_channel = False
        self.debug('Receiving')
        for channel, pipe in self._active_channels():
            if not self.running:
                return

            if pipe is None:
                if active_channels == 1:
                    last_channel = True
                if message is False:  # all channels are empty
                    # self.debug(f'***** channels sweep empty')
                    await asyncio.sleep(0.05)
                    # self.debug(f'***** resuming channels sweep')

                message = False
                active_channels = 0
                continue

            active_channels += 1
            try:
                # self.debug(f'***** waiting for message on channel {channel}')
                message = await pipe.receive(wait=last_channel)
            except asyncio.QueueEmpty:
                continue

            except Exception:
                self.exception(f'Error while receiving on channel {channel}, {pipe}')
                raise

            self.debug(f'Got message from {channel}: {message}')
            if message == Message.EOT:
                self.debug('Exhausted channel: %s' % channel)
                pipe.stop()
            else:
                message.checkin(self)
                yield (channel, message)

        self.debug('Finished receiving')

    def _active_channels(self):
        active_channels = self.channels.copy()
        while active_channels:
            yield None, None  # signal start of channels sweep

            for channel, pipe in active_channels.copy().items():
                if not pipe.running:
                    self.debug(f'skipping stopped channel {channel}')
                    del active_channels[channel]
                else:
                    yield channel, pipe

    async def Xreceiver(self):
        self.debug('Receiving')
        self.debug(f'Setting up channels {list(self.channels)}')
        # __import__('pudb').set_trace()
        # import sys; sys.exit()
        feeder = deque()
        events = Box(received=asyncio.Event())
        # receivers = dict()
        for channel, pipe in self._active_channels():
            self.debug(f'Setting up channel {channel}')
            events[channel] = asyncio.Event()
            events[channel].set()
            # receivers[channel] = asyncio.ensure_future(
            #     self.channel_receiver(channel, feeder, events))
            asyncio.ensure_future(self.channel_receiver(channel, feeder, events))

        self.debug('Waiting for feeder')
        while self.running and (len(feeder) or await events.received.wait()):
            for channel in self.channels:
                events[channel].clear()
            events.received.clear()
            channel, message = feeder.popleft()

            self.debug(f'Got message from {channel}: {message}')
            if message == Message.EOT:
                self.debug('Exhausted channel: %s' % channel)
                pipe.stop()
                # self.debug(f'* setting event for channel {channel}')
                events[channel].set()
                # receivers[channel].cancel()
                try:
                    await pipe.send(Message.EOT)
                except NotImplementedError:
                    pass
                # self.debug('-----------------------------')
                if not list(self._active_channels()):
                    self.debug('Stopping: no more active channels')
                    self.stop()
                    # TODO: cancel channel receiver coroutines
                    break
            else:
                message.checkin(self)
                yield channel, message

            for channel in self.channels:
                events[channel].set()

        self.debug('Finished receiving')

    async def channel_receiver(self, channel, feeder, events):
        self.debug(f'Receiver for {channel} is ready')
        pipe = self.channels[channel]
        while pipe.running and self.running and await events[channel].wait():
            # self.debug(f'* receiving from channel {channel}')
            events[channel].clear()
            try:
                feeder.append((channel, await pipe.receive()))
            except Exception:
                self.exception(f'Error while receiving on channel {channel}, {pipe}')
                raise

            # self.debug(f'* received from channel {channel} (next event: {events[channel].is_set()})')  # noqa: E501
            events.received.set()
        self.debug(f'Receiver for {channel} is exiting')

    def X_active_channels(self):
        channels = self.channels.copy()
        while channels:
            for channel, pipe in channels.copy().items():
                del channels[channel]
                if not pipe.running:
                    self.debug(f'skipping stopped channel {channel}')
                else:
                    yield channel, pipe
        if channels:
            pass  # TODO: channel clean-ups


class RetryableMessages:
    """Interfaces a queue between the inbox and the processor where we can insert back retries."""

    def __init__(self, node, messages):
        self.node = node
        self.messages = messages
        self._forwarder = None

    def __aiter__(self):
        if self._forwarder is None:  # singleton forwarder, for when we're using MultiProcessor
            self._forwarder = self.forwarder()
        return self._forwarder

    async def feeder(self):
        """Feed the inbox to the queue."""
        async for channel, self.newmsg in self.messages:
            # self.node.debug(f'*** collector retry: feeding {self.newmsg.type} msg {self.newmsg.meta.id}')  # noqa: E501
            self.forwarded.clear()
            await self.queue.put((channel, self.newmsg))
            await self.forwarded.wait()
        # self.node.debug('*** collector retry: feeder done')
        self.exhausted = True
        if self.pending > 0:
            await self.finished.wait()
        # self.node.debug('*** collector retry: feeder ready to exit')
        await self.queue.put(Message.EOT)
        # self.node.debug('*** collector retry: feeder exited')

    async def forwarder(self):
        """Turn the queue into an iterator that the processor can consume."""
        self.queue = asyncio.Queue()
        self.forwarded = asyncio.Event()
        self.finished = asyncio.Event()
        self.exhausted = False
        self.newmsg = None
        self.pending = 0  # number of messages currently handled by node processor
        feeder = self.node.loop.create_task(self.feeder())
        async for channel, message in aiter(self.queue.get, Message.EOT):
            # self.node.debug(f'*** collector retry: forwarding {message.type} msg {message.meta.id}')  # noqa: E501
            self.queue.task_done()
            if message is self.newmsg:
                self.forwarded.set()
            self.pending += 1
            yield channel, message

        # self.node.debug(f'*** collector retry: forwarder exiting')
        self.queue.task_done()
        await feeder
        # self.node.debug(f'*** collector retry: forwarder exited')

    def processing_done(self):
        """Signal that a message is not in the processor anymore."""
        self.pending -= 1
        # self.node.debug(f'*** collector retry: processing done {self.pending}')
        if self.exhausted:
            self.finished.set()

    async def retry(self, channel, message, wait=0.001, id_=None):
        """Insert a message back into the queue for retrying it."""
        # self.node.debug(f'*** collector retry{"" if id_ is None else " %s" % id_}: retrying {message.type} msg {message.meta.id}')  # noqa: E501
        await asyncio.sleep(wait)
        await self.node.loop.create_task(self.queue.put((channel, message)))
        self.processing_done()


class Outbox(Manifold):
    def __call__(self, messages):
        return self.sender(messages)

    async def sender(self, messages):
        self.debug('Ready to send')
        async for channel, message in messages:
            channel = channel or 'default'
            if channel is Message.DROP:
                self.drop(message)
            else:
                self.debug(f'Sending message to {channel}: {message}')
                if channel in self.channels:
                    await self.channels[channel].send(message)
                    # self.debug(f'Sent to    {channel}: {message} [{self.channels[channel].id}]')
                    message.checkout(self)
                    yield channel, message

                    # self.debug(f'Yielded    {channel}: {message}')
                else:
                    raise KeyError(f'Channel "{channel}" does not exist in {self}')

        self.debug('Finished sending')
        for pipe in self.channels.values():
            try:
                self.debug(f'EOT to {pipe}')
                await pipe.send(Message.EOT)
            except Exception:
                __import__('pudb').set_trace()


class ThreadedNode(Node):
    pass


class ThreadedProcessor:
    def __init__(self, processor, scale):
        self.processor = processor
        self.scale = scale
        self.iqueue = janus.Queue(maxsize=self.scale)
        self.oqueue = janus.Queue(maxsize=self.scale)
        self.barrier = Barrier(self.scale)

    async def __call__(self, messages):
        async for channel, message in self.run_threads(messages):
            yield channel, message

    async def run_threads(self, messages):
        asyncio.ensure_future(self.thread_feeder(messages))
        self.threads = dict((i, Thread(target=self.thread_consumer, args=(i,)).start())
                            for i in range(self.scale))
        queue_iter = aiter(self.oqueue.async_q.get, (None, Message.EOT))
        async for channel, message in queue_iter:
            self.oqueue.async_q.task_done()
            yield channel, message

        # Empty queue of threads' EOTs
        for i in range(self.scale):
            if i:  # skip the one already consumed by aiter above
                await self.oqueue.async_q.get()
            self.oqueue.async_q.task_done()
            # print(f'thread {i} EOT received back')

        while self.threads:  # FIXME: join threads instead, and move or retire del self.threads[]
            asyncio.sleep(0.1)      # while at it, catch exceptions and clean up queue with task_done  # noqa: E501
        # print(f'all threads stopped')

    async def thread_feeder(self, messages):
        async for (channel, message) in messages:
            # TODO: recreate dead threads, report thread failures
            await self.iqueue.async_q.put((channel, message))
        for i in range(self.scale):
            await self.iqueue.async_q.put((None, Message.EOT))
            # print(f'thread {i} EOT sent')

    def thread_consumer(self, threadnum):  # runs in thread
        # print(f'thread {threadnum} started')
        queue_iter = iter(self.iqueue.sync_q.get, (None, Message.EOT))
        for channel, message in self.processor(queue_iter):
            self.iqueue.sync_q.task_done()
            self.oqueue.sync_q.put((channel, message))
        # print(f'thread {threadnum} EOT received')
        self.iqueue.sync_q.task_done()  # for EOT which does not make it past queue iterator
        # print(f'thread {threadnum} task done')
        self.barrier.wait()
        self.oqueue.sync_q.put((None, Message.EOT))  # TODO: use threading.Event to send just one
        # print(f'thread {threadnum} EOT sent back')
        del self.threads[threadnum]
        # print(f'thread {threadnum} stopped')


class PriorityRegistry(dict):
    def ordered(self):
        return [item for _, item in sorted(self.items())]


class CmdRunner:

    async def runcmd(self, *args, raise_=True, **kwargs):
        try:
            proc = await asyncio.create_subprocess_exec(
                *map(str, args), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                **kwargs)
            await proc.wait()
            exitcode = await proc.wait()
            stdout = (await proc.stdout.read()).decode()
            stderr = (await proc.stderr.read()).decode()
            if exitcode:
                raise RuntimeError(f'Command {args} ({kwargs}) returned with exitcode {exitcode}, '
                                   f'stdout: {stdout or None}, stderr: {stderr or None}')

        except Exception as e:
            self.logger.exception(f'Error running command: {e}')
            if raise_:
                raise

        return exitcode, stdout, stderr
