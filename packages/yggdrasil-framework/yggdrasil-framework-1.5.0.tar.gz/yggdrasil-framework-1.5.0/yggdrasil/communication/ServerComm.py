import os
import uuid
from collections import OrderedDict
from yggdrasil.components import import_component
from yggdrasil.communication import CommBase, get_comm
from yggdrasil.drivers.ClientRequestDriver import YGG_CLIENT_EOF


class ServerComm(CommBase.CommBase):
    r"""Class for handling Server side communication.

    Args:
        name (str): The environment variable where communication address is
            stored.
        request_comm (str, optional): Comm class that should be used for the
            request comm. Defaults to None.
        response_kwargs (dict, optional): Keyword arguments for the response
            comm. Defaults to empty dict.
        **kwargs: Additional keywords arguments are passed to the input comm.

    Attributes:
        response_kwargs (dict): Keyword arguments for the response comm.
        icomm (Comm): Request comm.
        ocomm (OrderedDict): Response comms for each request.

    """

    _dont_register = True
    
    def __init__(self, name, request_comm=None, response_kwargs=None,
                 dont_open=False, **kwargs):
        if response_kwargs is None:
            response_kwargs = dict()
        icomm_name = name
        icomm_kwargs = kwargs
        icomm_kwargs['direction'] = 'recv'
        icomm_kwargs['dont_open'] = True
        icomm_kwargs['comm'] = request_comm
        self.response_kwargs = response_kwargs
        self.icomm = get_comm(icomm_name, **icomm_kwargs)
        self.ocomm = OrderedDict()
        self.response_kwargs.setdefault('comm', self.icomm.comm_class)
        self.response_kwargs.setdefault('recv_timeout', self.icomm.recv_timeout)
        self.response_kwargs.setdefault('language', self.icomm.language)
        self._used_response_comms = dict()
        self.clients = []
        self.closed_clients = []
        self.nclients_expected = int(os.environ.get('YGG_NCLIENTS', 0))
        super(ServerComm, self).__init__(self.icomm.name, dont_open=dont_open,
                                         recv_timeout=self.icomm.recv_timeout,
                                         is_interface=self.icomm.is_interface,
                                         direction='recv', no_suffix=True,
                                         address=self.icomm.address)

    def get_status_message(self, nindent=0, **kwargs):
        r"""Return lines composing a status message.
        
        Args:
            nindent (int, optional): Number of tabs that should
                be used to indent each line. Defaults to 0.
            *kwargs: Additional arguments are passed to the
                parent class's method.
                
        Returns:
            tuple(list, prefix): Lines composing the status message and the
                prefix string used for the last message.

        """
        lines, prefix = super(ServerComm, self).get_status_message(
            nindent=nindent, **kwargs)
        lines.append('%s%-15s:' % (prefix, 'request comm'))
        lines += self.icomm.get_status_message(nindent=(nindent + 1))[0]
        lines.append('%s%-15s:' % (prefix, 'response comms'))
        for x in self.ocomm.values():
            lines += x.get_status_message(nindent=(nindent + 1))[0]
        return lines, prefix
        
    @classmethod
    def is_installed(cls, language=None):
        r"""Determine if the necessary libraries are installed for this
        communication class.

        Args:
            language (str, optional): Specific language that should be checked
                for compatibility. Defaults to None and all languages supported
                on the current platform will be checked.

        Returns:
            bool: Is the comm installed.

        """
        return import_component('comm').is_installed(language=language)

    @property
    def maxMsgSize(self):
        r"""int: Maximum size of a single message that should be sent."""
        return self.icomm.maxMsgSize
        
    @classmethod
    def underlying_comm_class(self):
        r"""str: Name of underlying communication class."""
        return import_component('comm').underlying_comm_class()

    @classmethod
    def comm_count(cls):
        r"""int: Number of communication connections."""
        return import_component('comm').comm_count()

    @classmethod
    def new_comm_kwargs(cls, name, request_comm=None, **kwargs):
        r"""Initialize communication with new comms.

        Args:
            name (str): Name for new comm.
            request_comm (str, optional): Name of class for new input comm.
                Defaults to None.

        """
        args = [name]
        icomm_class = import_component('comm', request_comm)
        kwargs['direction'] = 'recv'
        if 'address' not in kwargs:
            iargs, kwargs = icomm_class.new_comm_kwargs(name, **kwargs)
        kwargs['request_comm'] = request_comm
        return args, kwargs

    @property
    def opp_comms(self):
        r"""dict: Name/address pairs for opposite comms."""
        out = super(ServerComm, self).opp_comms
        out.update(**self.icomm.opp_comms)
        return out

    def opp_comm_kwargs(self):
        r"""Get keyword arguments to initialize communication with opposite
        comm object.

        Returns:
            dict: Keyword arguments for opposite comm object.

        """
        kwargs = super(ServerComm, self).opp_comm_kwargs()
        kwargs['comm'] = "ClientComm"
        kwargs['request_comm'] = self.icomm.comm_class
        kwargs['response_kwargs'] = self.response_kwargs
        return kwargs
        
    def open(self):
        r"""Open the connection."""
        super(ServerComm, self).open()
        self.icomm.open()

    def close(self, *args, **kwargs):
        r"""Close the connection."""
        self.icomm.close(*args, **kwargs)
        for ocomm in self.ocomm.values():
            ocomm.close()
        for ocomm in self._used_response_comms.values():
            ocomm.close()
        super(ServerComm, self).close(*args, **kwargs)

    @property
    def is_open(self):
        r"""bool: True if the connection is open."""
        return self.icomm.is_open

    @property
    def is_closed(self):
        r"""bool: True if the connection is closed."""
        return self.icomm.is_closed

    @property
    def n_msg_recv(self):
        r"""int: The number of messages in the connection."""
        return self.icomm.n_msg_recv

    @property
    def n_msg_recv_drain(self):
        r"""int: The number of messages in the connection to drain."""
        return self.icomm.n_msg_recv_drain

    @property
    def open_clients(self):
        r"""list: Available open clients."""
        return list(set(self.clients) - set(self.closed_clients))

    @property
    def all_clients_connected(self):
        r"""bool: True if all expected clients have connected.
        False otherwise."""
        return ((self.nclients_expected > 0)
                and (len(self.clients) >= self.nclients_expected))

    # RESPONSE COMM
    def create_response_comm(self, header):
        r"""Create a response comm based on information from the last header."""
        if not isinstance(header, dict):  # pragma: debug
            raise RuntimeError("No header received with last message.")
        elif 'response_address' not in header:  # pragma: debug
            raise RuntimeError("Last header does not contain response address.")
        comm_kwargs = dict(address=header['response_address'],
                           direction='send', is_response_server=True,
                           single_use=True, **self.response_kwargs)
        request_id = header['request_id']
        while request_id in self.ocomm:  # pragma: debug
            request_id += str(uuid.uuid4())
        header['response_id'] = request_id
        self.ocomm[request_id] = get_comm(
            self.name + '.server_response_comm.' + request_id,
            **comm_kwargs)
        client_model = header.get('client_model', '')
        self.ocomm[request_id].client_model = client_model
        if client_model and (client_model not in self.clients):
            self.clients.append(client_model)

    def remove_response_comm(self, request_id):
        r"""Remove response comm.

        Args:
            request_id (str): The ID used to register the response
                comm that should be removed.

        """
        ocomm = self.ocomm.pop(request_id, None)
        if ocomm is not None:
            ocomm.close_in_thread(no_wait=True)
            self._used_response_comms[ocomm.name] = ocomm

    # SEND METHODS
    def send_to(self, request_id, *args, **kwargs):
        r"""Send a message to a specific response comm.

        Args:
            request_id (str): ID used to register the response comm.
            *args: Arguments are passed to output comm send method.
            **kwargs: Keyword arguments are passed to output comm send method.
    
        Returns:
            obj: Output from output comm send method.

        """
        # if self.is_closed:
        #     self.debug("send(): Connection closed.")
        #     return False
        out = self.ocomm[request_id].send(*args, **kwargs)
        self.remove_response_comm(request_id)
        return out
        
    def send(self, *args, **kwargs):
        r"""Send a message to the output comm.

        Args:
            *args: Arguments are passed to output comm send method.
            **kwargs: Keyword arguments are passed to output comm send method.

        Returns:
            obj: Output from output comm send method.

        """
        if len(self.ocomm) == 0:  # pragma: debug
            raise RuntimeError("There is no registered response comm.")
        return self.send_to(next(iter(self.ocomm.keys())),
                            *args, **kwargs)

    # RECV METHODS
    def recv_from(self, *args, **kwargs):
        r"""Receive a message from the input comm and open a new response comm
        for output using address from the header, returning the request_id.

        Args:
            *args: Arguments are passed to input comm recv method.
            **kwargs: Keyword arguments are passed to input comm recv method.

        Returns:
            tuple(bool, obj, str): Success or failure of recv call,
                output from input comm recv method, and request_id that
                response should be sent to.

        """
        kwargs['return_header'] = True
        request_id = None
        flag, msg, header = self.recv(*args, **kwargs)
        if ((flag and (not self.icomm.is_eof(msg))
             and (not self.icomm.is_empty_recv(msg)))):
            request_id = header['response_id']
        return flag, msg, request_id
    
    def recv(self, *args, **kwargs):
        r"""Receive a message from the input comm and open a new response comm
        for output using address from the header.

        Args:
            *args: Arguments are passed to input comm recv method.
            **kwargs: Keyword arguments are passed to input comm recv method.

        Returns:
            obj: Output from input comm recv method.

        """
        # if self.is_closed:
        #     self.debug("recv(): Connection closed.")
        #     return (False, None)
        return_header = kwargs.pop('return_header', False)
        kwargs['return_header'] = True
        flag, msg, header = self.icomm.recv(*args, **kwargs)
        if flag:
            if isinstance(msg, bytes) and (msg == YGG_CLIENT_EOF):
                self.closed_clients.append(header['client_model'])
                kwargs['return_header'] = return_header
                return self.recv(*args, **kwargs)
            elif not (self.icomm.is_eof(msg) or self.icomm.is_empty_recv(msg)):
                self.create_response_comm(header)
        if return_header:
            out = (flag, msg, header)
        else:
            out = (flag, msg)
        return out

    # OLD STYLE ALIASES
    def rpcSend(self, *args, **kwargs):
        r"""Alias for RPCComm.send"""
        return self.send(*args, **kwargs)

    def rpcRecv(self, *args, **kwargs):
        r"""Alias for RPCComm.recv"""
        return self.recv(*args, **kwargs)
    
    def drain_messages(self, direction='recv', **kwargs):
        r"""Sleep while waiting for messages to be drained."""
        if direction == 'recv':
            self.icomm.drain_messages(direction='recv', **kwargs)

    def purge(self):
        r"""Purge input and output comms."""
        self.icomm.purge()
        # Not sure if server should purge the response queue...
        # for ocomm in self.ocomm.values():
        #     ocomm.purge()
        super(ServerComm, self).purge()
