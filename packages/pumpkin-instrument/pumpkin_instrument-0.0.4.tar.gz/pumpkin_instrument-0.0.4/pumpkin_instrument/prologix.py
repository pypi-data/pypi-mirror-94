# coding: utf-8
import socket
import time
from enum import Enum
from select import select

from serial import Serial

PROLOGIX_BAUD = 9600
PROLOGIX_PORT = 1234


class PrologixType(Enum):
    Ethernet = 1
    USB = 2


def read_poll_socket(sock: socket.socket, amount: int) -> bytes:
    """
    Reads the socket by polling it via select call, returning bytes if anything was read from the socket.

    :param sock: The socket to read the bytes from.
    :param amount: The amount of bytes to read from the socket
    :return: 0 or more bytes read from the socket.
    """
    readable, _, _ = select([sock], [], [], 0)
    if readable:
        return sock.recv(amount)
    else:
        return bytes()


class PrologixController:
    """Abstraction of the Prologix GP-IB controller. Handles both the Ethernet and USB controllers."""

    def __init__(self, controller_type: PrologixType, controller_address: str):
        """
        Opens the communication to the Prologix GP-IB controller via the specified `controller_type` and
        `controller_address`.

        `controller_address` is a COM|/dev/ttyUSB* port if type is USB, else it is an IP address.

        :param controller_type: The type of controller, either Ethernet or USB.
        :param controller_address: The device path or IP address of Prologix controller.
        """
        if controller_type == PrologixType.Ethernet:
            self._sock = socket.create_connection((controller_address, PROLOGIX_PORT))
            self._sock.setblocking(False)  # Make the socket non-blocking.
            self._write = self._sock.sendall
            self._read = lambda amt: read_poll_socket(self._sock, amt)
        elif controller_type == PrologixType.USB:
            self._ser = Serial(controller_address, PROLOGIX_BAUD)
            self._ser.timeout = 0  # Make the serial socket non-blocking.
            self._write = self._ser.write
            self._read = self._ser.read
        else:
            raise ValueError(f'Unsupported controller type {controller_type}')
        self._curr_address = -1
        self._controller_type = controller_type

    def _write_address(self, address):
        """
        Checks the currently addressed GPIB pumpkin_instrument and changes the device addressed by the Prologix
        controller if the current address does not match the requested `address`.

        :param address: The address to talk to on the GPIB bus.
        """
        if self._curr_address != address:
            self._write(f'++addr {address}\n'.encode('ascii'))
            self._curr_address = address

    @property
    def controller_type(self) -> PrologixType:
        """
        Gets the currently used prologix configuration type.

        :return: The type of prologix controller in use.
        """
        return self._controller_type

    def write(self, address: int, data: bytes):
        """
        Writes out the binary data to the address on the Prologix controller. Automatically switches the address the
        prologix controller is talking to if the previous address used is different.

        :param address: The address to write the data to.
        :param data: The binary data to write out to the controller.
        """
        self._write_address(address)
        self._write(data)

    def read(self, address: int, amount: int) -> bytes:
        """
        Reads binary data from the prologix GPIB controller. Automatically switches the address the
        prologix controller is talking to if the previous address used is different.

        :param address: The GPIB address to read from.
        :param amount: The amount of bytes to read from the prologix controller.
        :return: The bytes read from the prologix controller.
        """
        self._write_address(address)

        # Instruct pumpkin_instrument to talky talky and read back until EOI is asserted.
        self._write('++read eoi\n'.encode('ascii'))
        return self._read(amount)

    def read_until(self, address: int, terminator: bytes = '\r\n'.encode('ascii')) -> bytes:
        """
        Reads from the pumpkin_instrument until a terminator is asserted. This will raise a RuntimeError if the terminator
        is not found after retrying 10 times.

        :param address: The address of the GPIB pumpkin_instrument to read from.
        :param terminator: The terminator bytes to search for in the response.
        :return: The bytes of the response including the terminator.
        """
        # constants local to the method
        sleep_time = 0.05
        block_size = 64
        no_data_reads = 0
        fail_amount = 10

        # Instruct the pumpkin_instrument to talky talky and read back until EOI is asserted.
        self.write(address, '++read eoi\n'.encode('ascii'))
        response = bytearray()
        while True:
            b = self._read(block_size)

            # Check to see if we got something from the GPIB bus, if not, fail after fail_amount or sleep for sleep_time
            if not b:
                no_data_reads += 1
                if no_data_reads > fail_amount:
                    raise RuntimeError(f'Instrument failed to respond with {terminator} bytes terminator.')
                else:
                    time.sleep(sleep_time)
                continue

            response += b
            try:
                # Check for the terminator in the response.
                response.index(terminator)
                break
            except ValueError:
                # Terminator not found, we're good to continue.
                pass

        return bytes(response)