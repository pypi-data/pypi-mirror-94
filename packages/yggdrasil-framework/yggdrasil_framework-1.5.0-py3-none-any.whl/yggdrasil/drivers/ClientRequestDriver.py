from yggdrasil.drivers.ConnectionDriver import ConnectionDriver
from yggdrasil.drivers.ClientResponseDriver import ClientResponseDriver

# ----
# Client sends resquest to local client output comm
# Client recvs response from local client input comm
# ----
# Client request driver recvs from local client output comm
# Client request driver creates client response driver
# Client request driver sends to server request comm (w/ response comm header)
# ----
# Client response driver recvs from client response comm
# Client response driver sends to local client input comm
# ----
# Server recvs request from local server input comm
# Server sends response to local server output comm
# ----
# Server request driver recvs from server request comm
# Server request driver creates server response driver
# Server request driver sends to local server input comm
# ----
# Server response driver recvs from local server output comm
# Server response driver sends to client response comm
# ----


YGG_CLIENT_INI = b'YGG_BEGIN_CLIENT'
YGG_CLIENT_EOF = b'YGG_END_CLIENT'


class ClientRequestDriver(ConnectionDriver):
    r"""Class for handling client side RPC type communication.

    Args:
        model_request_name (str): The name of the channel used by the client
            model to send requests.
        request_name (str, optional): The name of the channel used to
            send requests to the server request driver. Defaults to
            model_request_name + '_SERVER' if not set.
        comm (str, optional): The comm class that should be used to
            communicate with the server request driver. Defaults to
            tools.get_default_comm().
        comm_address (str, optional): Address for the server request driver.
            Defaults to None and a new address is generated.
        **kwargs: Additional keyword arguments are passed to parent class.

    Attributes:
        comm (str): The comm class that should be used to communicate with the
            server request driver.
        comm_address (str): Address for the server request driver.
        response_drivers (list): Response drivers created for each request.

    """

    _connection_type = None
    _direction = 'output'

    def __init__(self, model_request_name, request_name=None,
                 comm=None, comm_address=None, **kwargs):
        if request_name is None:
            request_name = model_request_name + '_SERVER'
        # Input communicator
        icomm_kws = kwargs.get('icomm_kws', {})
        icomm_kws['comm'] = None
        icomm_kws['name'] = model_request_name
        kwargs['icomm_kws'] = icomm_kws
        # Output communicator
        ocomm_kws = kwargs.get('ocomm_kws', {})
        ocomm_kws['comm'] = comm
        ocomm_kws['name'] = request_name
        if comm_address is not None:
            ocomm_kws['address'] = comm_address
        ocomm_kws['no_suffix'] = True
        ocomm_kws['is_client'] = True
        ocomm_kws['close_on_eof_send'] = False
        kwargs['ocomm_kws'] = ocomm_kws
        # Parent and attributes
        super(ClientRequestDriver, self).__init__(model_request_name, **kwargs)
        self.env[self.icomm.name] = self.icomm.address
        self.response_drivers = []
        self.comm = comm
        self.comm_address = self.ocomm.opp_address
        self._block_response = False

    @property
    def last_header(self):
        r"""dict: Information contained in the header of the last message
        received from the client model."""
        if self._last_header is None:
            raise AttributeError("No new requests have been received, so there "
                                 + "does not yet exist information required for "
                                 + "creating a response comm and fowarding the "
                                 + "request.")
        return self._last_header

    @property
    def request_id(self):
        r"""str: Unique ID for the last message."""
        return self.last_header['request_id']

    @property
    def model_response_address(self):
        r"""str: The address of the channel used by the client model to receive
        responses."""
        return self.last_header['response_address']

    @property
    def client_model(self):
        r"""str: Name of the client model."""
        # NOTE: This means that any client_model value in the last
        # header will not be propagated to the server. This also assumes
        # that there is only one client model serviced by this driver
        return self.name.split(':')[0]

    @property
    def request_name(self):
        r"""str: The name of the channel used to send requests to the server
        request driver."""
        return self.ocomm.name
    
    @property
    def request_address(self):
        r"""str: The address of the channel used to send requests to the server
        request driver."""
        return self.ocomm.opp_address

    def close_response_drivers(self):
        r"""Close response driver."""
        # To force response server to connect after response client has stopped
        # self.sleep(0.5)
        with self.lock:
            self.debug("Closing response drivers.")
            self._block_response = True
            for x in self.response_drivers:
                x.terminate()
            self.response_drivers = []

    def close_comm(self):
        r"""Close response drivers."""
        self.close_response_drivers()
        super(ClientRequestDriver, self).close_comm()
            
    def printStatus(self, *args, **kwargs):
        r"""Also print response drivers."""
        super(ClientRequestDriver, self).printStatus(*args, **kwargs)
        for x in self.response_drivers:
            x.printStatus(*args, **kwargs)

    def before_loop(self):
        r"""Send client sign on to server response driver."""
        super(ClientRequestDriver, self).before_loop()
        # self.sleep()  # Help ensure that the server is connected
        self.debug("Sending client sign on")
        super(ClientRequestDriver, self).send_message(YGG_CLIENT_INI,
                                                      header_kwargs={'raw': True})
        self.ocomm._send_serializer = True
        # self.info("%s: before loop complete", self.name)

    def send_message(self, *args, **kwargs):
        r"""Start a response driver for a request message and send message with
        header.

        Args:
            *args: Arguments are passed to parent class send_message.
            **kwargs: Keyword arguments are passed to parent class send_message.

        Returns:
            bool: Success or failure of send.

        """
        if self.ocomm.is_closed:
            return False
        # Start response driver
        is_eof = kwargs.get('is_eof', False)
        if is_eof:
            kwargs.setdefault('header_kwargs', {})
            kwargs['header_kwargs'].setdefault('client_model',
                                               self.client_model)
        else:
            with self.lock:
                if (not self.is_comm_open) or self._block_response:  # pragma: debug
                    return False
                drv_args = [self.model_response_address]
                drv_kwargs = dict(comm=self.comm, msg_id=self.request_id,
                                  request_name=self.name)
                self.debug("Creating response comm: address = %s, request_id = %s",
                           self.model_response_address, self.request_id)
                try:
                    response_driver = ClientResponseDriver(*drv_args, **drv_kwargs)
                    self.response_drivers.append(response_driver)
                    response_driver.start()
                    self.debug("Started response comm: address = %s, request_id = %s",
                               self.model_response_address, self.request_id)
                except BaseException:  # pragma: debug
                    self.exception("Could not create/start response driver.")
                    return False
            # Send response address in header
            kwargs.setdefault('header_kwargs', {})
            kwargs['header_kwargs'].setdefault(
                'response_address', response_driver.response_address)
            kwargs['header_kwargs'].setdefault('request_id', self.request_id)
            kwargs['header_kwargs'].setdefault('client_model',
                                               self.client_model)
        return super(ClientRequestDriver, self).send_message(*args, **kwargs)

    def run_loop(self):
        r"""Run the driver. Continue looping over messages until there are not
        any left or the communication channel is closed.
        """
        super(ClientRequestDriver, self).run_loop()
        if not self.was_break:
            self.prune_response_drivers()

    def prune_response_drivers(self):
        r"""Remove response drivers that are no longer being used."""
        with self.lock:
            remove_idx = []
            for i, x in enumerate(self.response_drivers):
                if (((not x.is_alive())
                     and x.icomm.is_confirmed_recv
                     and x.ocomm.is_confirmed_send)):
                    x.cleanup()
                    remove_idx.append(i)
            for i in remove_idx[::-1]:
                self.response_drivers.pop(i)
