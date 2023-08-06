import uuid
from yggdrasil import multitasking
from yggdrasil.communication import CommBase


class AsyncTryAgain(Exception):
    r"""Exception raised when comm open, but send should be attempted again."""
    pass


class AsyncComm(CommBase.CommBase):
    r"""Class for handling asynchronous I/O.

    Args:
        name (str): The name of the message queue.
        dont_backlog (bool, optional): If True, the backlog will not be started
            and all messages will be sent/received directly to/from the comm.
            Defaults to False.
        **kwargs: Additional keyword arguments are passed to CommBase.
        
    Attributes:
        dont_backlog (bool): If True, the backlog will not be started and all
            messages will be sent/received directly to/from the comm.
        backlog_send_ready (multitasking.Event): Event set when there is a
            message in the send backlog.
        backlog_recv_ready (multitasking.Event): Event set when there is a
            message in the recv backlog.
        
    """
    
    _disconnect_attr = (CommBase.CommBase._disconnect_attr
                        + ['backlog_send_ready', 'backlog_recv_ready',
                           '_backlog_thread'])

    def __init__(self, name, dont_backlog=False, **kwargs):
        self.dont_backlog = (dont_backlog or kwargs.get('is_interface', False))
        self._backlog_recv = []
        self._backlog_send = []
        self._backlog_thread = None
        self.backlog_send_ready = multitasking.Event()
        self.backlog_recv_ready = multitasking.Event()
        self.backlog_open = False
        self._used_direct = False
        super(AsyncComm, self).__init__(name, **kwargs)

    def get_status_message(self, nindent=0):
        r"""Return lines composing a status message.
        
        Args:
            nindent (int, optional): Number of tabs that should be used to
                indent each line. Defaults to 0.
                
        Returns:
            tuple(list, prefix): Lines composing the status message and the
                prefix string used for the last message.

        """
        lines, prefix = super(AsyncComm, self).get_status_message(nindent=nindent)
        lines += ['%s%-15s: %s' % (prefix, 'open (backlog)', self.is_open_backlog),
                  '%s%-15s: %s' % (prefix, 'open (direct)', self.is_open_direct),
                  '%s%-15s: %s' % (prefix, 'nsent (backlog)', self.n_msg_backlog_send),
                  '%s%-15s: %s' % (prefix, 'nrecv (backlog)', self.n_msg_backlog_recv),
                  '%s%-15s: %s' % (prefix, 'nsent (direct)', self.n_msg_direct_send),
                  '%s%-15s: %s' % (prefix, 'nrecv (direct)', self.n_msg_direct_recv)]
        if len(self._work_comms) > 0:
            lines.append('%sWork comms:' % prefix)
            for v in self._work_comms.values():
                lines += v.get_status_message(nindent=nindent + 1)[0]
        return lines, prefix
        
    @property
    def backlog_thread(self):
        r"""tools.YggTask: Task that will handle sinding or receiving
        backlogged messages."""
        if self._backlog_thread is None:
            if self.direction == 'send':
                self._backlog_thread = CommBase.CommTaskLoop(
                    self, target=self.run_backlog_send, suffix='SendBacklog')
            else:
                self._backlog_thread = CommBase.CommTaskLoop(
                    self, target=self.run_backlog_recv, suffix='RecvBacklog')
        return self._backlog_thread

    def open(self):
        r"""Open the connection by connecting to the queue."""
        super(AsyncComm, self).open()
        self._open_direct()
        if self.is_open_direct:
            self._open_backlog()

    def _open_direct(self):
        r"""Open the comm directly."""
        pass

    def _open_backlog(self):
        r"""Open the backlog."""
        if not self.is_open_backlog:
            self.backlog_open = True
            if not self.dont_backlog:
                self.backlog_thread.start()

    def _close_direct(self, linger=False):
        r"""Close the comm directly."""
        pass

    def _close_backlog(self, wait=False):
        r"""Close the backlog thread."""
        self.debug('')
        self.backlog_open = False
        if self._backlog_thread is not None:
            self.backlog_thread.set_break_flag()
        self.backlog_send_ready.set()
        self.backlog_recv_ready.set()
        if ((wait and (not self.dont_backlog)
             and (self._backlog_thread is not None))):
            self.backlog_thread.wait(key=str(uuid.uuid4()))

    def _close(self, linger=False):
        r"""Close the connection.

        Args:
            linger (bool, optional): If True, drain messages before closing the
                comm. Defaults to False.

        """
        self.debug('')
        self._close_backlog(wait=True)
        self._close_direct()
        super(AsyncComm, self)._close(linger=linger)

    def stop_backlog(self):
        r"""Stop the asynchronous backlog, turning this into a direct comm."""
        self._close_backlog(wait=True)
        self.dont_backlog = True

    @property
    def is_open(self):
        r"""bool: True if the backlog is open."""
        return self.is_open_direct or self.is_open_backlog

    @property
    def is_open_direct(self):
        r"""bool: True if the direct comm is not None."""
        return False

    @property
    def is_open_backlog(self):
        r"""bool: True if the backlog thread is running."""
        return self.backlog_open

    @property
    def n_msg_direct_recv(self):
        r"""int: Number of messages currently being routed in recv."""
        return 0

    @property
    def n_msg_direct_send(self):
        r"""int: Number of messages currently being routed in send."""
        return 0

    @property
    def n_msg_direct(self):
        r"""int: Number of messages currently being routed."""
        if self.direction == 'send':
            return self.n_msg_direct_send
        else:
            return self.n_msg_direct_recv

    @property
    def n_msg_backlog_recv(self):
        r"""int: Number of messages in the receive backlog."""
        if self.is_open_backlog:
            return len(self.backlog_recv)
        return 0

    @property
    def n_msg_backlog_send(self):
        r"""int: Number of messages in the send backlog."""
        if self.is_open_backlog:
            return len(self.backlog_send)
        return 0

    @property
    def n_msg_backlog(self):
        r"""int: Number of messages in the backlog."""
        if self.direction == 'recv':
            return self.n_msg_backlog_recv
        else:
            return self.n_msg_backlog_send

    @property
    def n_msg_recv(self):
        r"""int: Number of messages in the receive backlog."""
        if self.direction == 'recv':
            if self.dont_backlog:
                return self.n_msg_direct_recv
            else:
                return self.n_msg_backlog_recv
        else:
            return self.n_msg_direct_recv

    @property
    def n_msg_send(self):
        r"""int: Number of messages in the send backlog."""
        if self.direction == 'send':
            if self.dont_backlog:
                return self.n_msg_direct_send
            else:
                return self.n_msg_backlog_send
        else:
            return self.n_msg_direct_send

    @property
    def n_msg_recv_drain(self):
        r"""int: Number of messages in the receive backlog and direct comm."""
        return self.n_msg_direct_recv + self.n_msg_backlog_recv

    @property
    def n_msg_send_drain(self):
        r"""int: Number of messages in the send backlog and direct comm."""
        return self.n_msg_direct_send + self.n_msg_backlog_send

    @property
    def is_confirmed_send(self):
        r"""bool: True if all sent messages have been confirmed."""
        for v in self._work_comms.values():
            if (v.direction == 'send') and not v.is_confirmed_send:  # pragma: debug
                return False
        if self.is_open_backlog and self.n_msg_backlog_send:  # pragma: debug
            return False
        return (self.n_msg_direct_send == 0)

    @property
    def is_confirmed_recv(self):
        r"""bool: True if all received messages have been confirmed."""
        for v in self._work_comms.values():
            if (v.direction == 'recv') and not v.is_confirmed_recv:  # pragma: debug
                return False
        return (self.n_msg_direct_recv == 0)

    @property
    def backlog_recv(self):
        r"""list: Messages that have been received."""
        with self.backlog_thread.lock:
            return self._backlog_recv

    @property
    def backlog_send(self):
        r"""list: Messages that should be sent."""
        with self.backlog_thread.lock:
            return self._backlog_send

    def add_backlog_recv(self, msg):
        r"""Add a message to the backlog of received messages.

        Args:
            msg (str): Received message that should be backlogged.

        """
        with self.backlog_thread.lock:
            self.debug("Added %d bytes to recv backlog.", len(msg))
            self._backlog_recv.append(msg)
            self.backlog_recv_ready.set()

    def add_backlog_send(self, msg, **kwargs):
        r"""Add a message to the backlog of messages to be sent.

        Args:
            msg (str): Message that should be backlogged for sending.
            **kwargs: Additional keyword arguments are added along with
                the message.

        """
        with self.backlog_thread.lock:
            self.debug("Added %d bytes to send backlog.", len(msg))
            self._backlog_send.append((msg, kwargs))
            self.backlog_send_ready.set()

    def pop_backlog_recv(self):
        r"""Pop a message from the front of the recv backlog.

        Returns:
            str: First backlogged recv message.

        """
        with self.backlog_thread.lock:
            msg = self._backlog_recv.pop(0)
            self.debug("Popped %d bytes from recv backlog.", len(msg))
            if len(self._backlog_recv) == 0:
                self.backlog_recv_ready.clear()
        return msg

    def pop_backlog_send(self):
        r"""Pop a message from the front of the send backlog.

        Returns:
            tuple (str, dict): First backlogged send message and
                keyword arguments.

        """
        with self.backlog_thread.lock:
            msg, kwargs = self._backlog_send.pop(0)
            self.debug("Popped %d bytes from send backlog.", len(msg))
            if len(self._backlog_send) == 0:
                self.backlog_send_ready.clear()
        return msg, kwargs

    def run_backlog_send(self):
        r"""Continue trying to send buffered messages."""
        if not self.is_open_backlog:  # pragma: debug
            self.debug("Backlog closed")
            self._close_backlog()
            return
        if not self.send_backlog():  # pragma: debug
            self.debug("Stopping because send_backlog failed")
            self._close_backlog()
            return
        self.periodic_debug('run_backlog_send', period=1000)(
            "Sleeping (is_confirmed_send=%s, n_msg_send=%d)",
            str(self.is_confirmed_send), self.n_msg_backlog_send)
        self.sleep()

    def run_backlog_recv(self):
        r"""Continue buffering received messages."""
        if self.backlog_thread.main_terminated:  # pragma: debug
            self.debug("Main thread terminated")
            self._close_backlog()
            self.close()
        if not self.is_open_backlog:  # pragma: debug
            self.debug("Backlog closed")
            self._close_backlog()
            return
        if not self.recv_backlog():
            # Stop the thread, but don't close the backlog
            self.debug("Stopping backlog recv thread")
            self.backlog_thread.set_break_flag()
            return
        self.periodic_debug('run_backlog_recv', period=1000)(
            "Sleeping (is_confirmed_recv=%s)",
            str(self.is_confirmed_recv))
        self.sleep()

    def send_backlog(self):
        r"""Send a message from the send backlog to the queue."""
        if len(self.backlog_send) == 0:
            self.confirm_send()
            return True
        try:
            imsg, ikwargs = self.backlog_send[0]
            if not self._used_direct:
                self.suppress_special_debug = True
            flag = self._send_direct(imsg, **ikwargs)
            self.suppress_special_debug = False
            if flag:
                self.debug("Sent %d bytes to %s", len(imsg), self.address)
                self.pop_backlog_send()
                self._used_direct = True
        except AsyncTryAgain:  # pragma: debug
            flag = True
        except BaseException:  # pragma: debug
            self.exception('Error sending backlogged message')
            flag = False
        self.confirm_send()
        return flag

    def recv_backlog(self):
        r"""Check for any messages in the queue and add them to the recv
        backlog."""
        if not self.is_open_direct:
            self.debug("Direct comm closed.")
            flag = False
        elif self.n_msg_direct_recv == 0:
            self.verbose_debug("No messages waiting.")
            flag = True
        else:
            try:
                if not self._used_direct:
                    self.suppress_special_debug = True
                flag, data = self._recv_direct()
                self.suppress_special_debug = False
                if flag and data:
                    self.debug("Recv %d bytes from %s", len(data), self.address)
                    self.add_backlog_recv(data)
                    self._used_direct = True
            except BaseException:  # pragma: debug
                self.exception('Error receiving into backlog.')
                flag = False
        self.confirm_recv()
        return flag

    def _send_direct(self, payload):  # pragma: debug
        r"""Send a message to the comm directly.

        Args:
            payload (str): Message to send.

        Returns:
            bool: Success or failure of sending the message.

        """
        return False

    def _recv_direct(self):  # pragma: debug
        r"""Receive a message from the comm directly.

        Returns:
            tuple (bool, str): The success or failure of receiving a message
                and the message received.

        """
        return (False, self.empty_bytes_msg)

    def _send(self, payload, no_backlog=False, no_confirm=False, **kwargs):
        r"""Send a message to the backlog.

        Args:
            payload (str): Message to send.
            no_backlog (bool, optional): If False, any messages that can't be
                sent because the queue is full will be added to a list of
                messages to be sent once the queue is no longer full. If True,
                messages are not backlogged and an error will be raised if the
                queue is full. Defaults to False.
            no_confirm (bool, optional): If False and no_backlog is True, then
                this will block until the sent message is confirmed. If True,
                this will return without confirmation. Defaults to False.

        Returns:
            bool: Success or failure of sending the message.

        """
        if not self.is_open_direct:  # pragma: debug
            return False
        if self.dont_backlog:
            no_backlog = True
        if self.direction == 'recv':
            self.debug("Receive comm sending %d bytes direct.", len(payload))
            no_backlog = True
        if no_backlog or not self.backlog_send_ready.is_set():
            try:
                if not self._used_direct:
                    self.suppress_special_debug = True
                out = self._send_direct(payload, **kwargs)
                self.suppress_special_debug = False
                if out:
                    self._used_direct = True
                if no_backlog:
                    if out and (self.direction == 'send'):
                        out = self.wait_for_confirm(active_confirm=True,
                                                    timeout=False,
                                                    noblock=no_confirm,
                                                    direction='send')
                    return out
                elif out:
                    return out
            except AsyncTryAgain:
                if no_backlog:  # pragma: debug
                    if (not self._used) and self._multiple_first_send:
                        return False
                    else:
                        raise
        self.add_backlog_send(payload, **kwargs)
        self.debug('%d bytes backlogged', len(payload))
        return True

    def _recv(self, timeout=None, no_backlog=False, no_confirm=False):
        r"""Receive a message from the backlog.

        Args:
            timeout (float, optional): Time in seconds to wait for a message.
                Defaults to self.recv_timeout.
            no_backlog (bool, optional): If False and there are messages in the
                receive backlog, they will be returned first. Otherwise the
                queue is checked for a message. Defaults to False.
            no_confirm (bool, optional): If False and no_backlog is True, then
                this will block until the sent message is confirmed. If True,
                this will return without confirmation. Defaults to False.

        Returns:
            tuple (bool, str): The success or failure of receiving a message
                and the message received.

        """
        if timeout is None:
            timeout = self.recv_timeout
        if self.dont_backlog:
            no_backlog = True
        if self.direction == 'send':
            self.debug("Send comm receiving direct.")
            no_backlog = True
        # If no backlog, receive from queue
        if no_backlog:
            T = self.start_timeout(timeout, key_suffix='_recv:direct')
            while ((not T.is_out) and (self.n_msg_direct_recv == 0)
                   and self.is_open_direct):
                self.sleep()
            self.stop_timeout(key_suffix='_recv:direct', quiet=True)
            if not self.is_open_direct:  # pragma: debug
                self.debug("Comm closed")
                return (False, self.empty_bytes_msg)
            if self.n_msg_direct_recv == 0:  # pragma: debug
                self.verbose_debug("No messages waiting.")
                return (True, self.empty_bytes_msg)
            if not self._used_direct:
                self.suppress_special_debug = True
            out = self._recv_direct()
            self.suppress_special_debug = False
            if out:
                self._used_direct = True
            if out and (self.direction == 'recv'):
                self.wait_for_confirm(active_confirm=True,
                                      timeout=False,
                                      noblock=no_confirm,
                                      direction='recv')
            return out
        # Sleep until there is a message
        T = self.start_timeout(timeout, key_suffix='_recv:backlog')
        while (not T.is_out) and (not self.backlog_recv_ready.is_set()):
            self.backlog_recv_ready.wait(self.sleeptime)
        self.stop_timeout(key_suffix='_recv:backlog')
        # Return False if the queue is closed
        if (not self.is_open_backlog):  # pragma: debug
            self.debug("Backlog closed")
            return (False, self.empty_bytes_msg)
        # Return True, '' if there are no messages
        if not self.backlog_recv_ready.is_set():
            self.verbose_debug("No messages waiting.")
            return (True, self.empty_bytes_msg)
        # Return backlogged message
        self.debug('Returning backlogged received message')
        return (True, self.pop_backlog_recv())

    def purge(self):
        r"""Purge all messages from the comm."""
        super(AsyncComm, self).purge()
        with self.backlog_thread.lock:
            if self.direction == 'recv':
                while self.n_msg_direct > 0:  # pragma: debug
                    self._recv_direct()
            self.backlog_recv_ready.clear()
            self.backlog_send_ready.clear()
            self._backlog_recv = []
            self._backlog_send = []
