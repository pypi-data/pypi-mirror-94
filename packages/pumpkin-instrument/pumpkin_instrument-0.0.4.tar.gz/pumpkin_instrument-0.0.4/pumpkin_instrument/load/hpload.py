# coding: utf-8
# ##############################################################################
#  (C) Copyright 2020 Pumpkin, Inc. All Rights Reserved.                       #
#                                                                              #
#  This file may be distributed under the terms of the License                 #
#  Agreement provided with this software.                                      #
#                                                                              #
#  THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,                   #
#  INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND                       #
#  FITNESS FOR A PARTICULAR PURPOSE.                                           #
# ##############################################################################
"""
Implementations for the following HP Digital Loads:
    - 6060B (Via Prologix GP-IB)
"""
from datetime import timedelta
from enum import Enum
from typing import ContextManager, List, Any
from contextlib import contextmanager

from .types import Load, LoadMode, LoadCapability, LoadChannelCapability
from ..prologix import PrologixController
from ..types import InstrumentType
from ..instrument import Instrument


_HP606XB_TERMINATOR = "\r\n"


# ---------------------------- HP662X Types ----------------------------
class HP606XType(Enum):
    """
    Represents the specific 606XB Digital load used in the below helper class decorator.
    """
    HP6060B = 0


HPLoadModes = [LoadMode.Current, LoadMode.Resistance, LoadMode.Voltage]
HP606XChannelCapabilities = {
    HP606XType.HP6060B: [LoadChannelCapability(min_voltage=0,
                                               max_voltage=60,
                                               max_power=300,
                                               modes=HPLoadModes)],
}
HP606XInstrumentCapabilities = {
    HP606XType.HP6060B: LoadCapability(),
}


class _HP606XBContext(Load):
    """Represents the implementation of the SCPI protocol for the HP606X series of loads."""

    def __init__(self,
                 controller: PrologixController,
                 address: int,
                 psu_type: HP606XType,
                 inst_capabilities: LoadCapability,
                 chan_capabilities: List[LoadChannelCapability]):
        """
        Initializes the HP663X power supply context, commanding the PSU with the given `controller`,
        `address` and `psu_type`.
        """
        super(_HP606XBContext, self).__init__()
        self.controller = controller
        self.address = address
        self.psu_type = psu_type
        self.instrument_capabilities = inst_capabilities
        self.channel_capabilities = chan_capabilities
        self.num_channels = len(chan_capabilities)
        self.name = psu_type.name

    def _write_cmd(self, cmd_str: str):
        """Writes a command to the prologix controller, postfixing a newline to the end."""
        self.controller.write(self.address, f'{cmd_str}\n'.encode('ascii'))

    def _validate_channel(self, channel):
        """Validates the channel, making sure the channel number is within the bounds of the PSU."""
        if channel >= self.num_channels:
            raise ValueError(f'There is no #{channel + 1} channel on the {self.name}')

    def set_output_on(self, channel: int, is_on: bool):
        """
        Sets the output ON or OFF.

        :param channel: Not used, must be 0.
        :param is_on: True if ON, False if OFF.
        """
        is_on = "ON" if is_on else "OFF"
        self._write_cmd(f"INPUT {is_on}")

    def set_output_state(self, channel: int, mode: LoadMode, value: float):
        """
        Sets the load into CC/CV/CR modes depending on `mode` parameter.
        Channel is always `0`.
        Value is the voltage/current/resistance in volts/amps/ohms respectively.
        Will set input off as first step.

        :param channel: Is always 0, ignored
        :param mode: The mode to set the instrument to
        :param value: The value to set the instrument to.
        """
        # The flow is:
        # - turn off inputs, always
        # - set the CC/CR/CV mode
        # - set value for mode
        self._write_cmd("INPUT OFF")

        if mode == LoadMode.Current:
            self._write_cmd("MODE:CURR")
            self._write_cmd(f"CURR {value:0.3f}")
        elif mode == LoadMode.Resistance:
            self._write_cmd("MODE:RES")
            self._write_cmd(f"RES {value:0.3f}")
        elif mode == LoadMode.Voltage:
            self._write_cmd("MODE:VOLT")
            self._write_cmd(f"VOLT {value:0.3f}")
        else:
            raise ValueError(f'Load mode {mode} is not supported on the HP 6060B.')

    def get_load_voltage(self, channel: int) -> float:
        """
        Gets the current voltage input on the load. Channel is required, but not used. Use `0`

        Looks like this only returns the last set value for the VOLT command, not current voltage on the load.

        :return: Last set voltage
        """
        self._write_cmd(f'VOLT?')
        resp = str(self.controller.read_until(self.address, _HP606XB_TERMINATOR.encode('ascii')), 'ascii')
        resp = resp[:resp.index(_HP606XB_TERMINATOR)]
        return float(resp)

    def get_load_current(self, channel: int) -> float:
        """
        Gets the current amps input on the load. Channel is required, but not used. Use `0`

        :return: The current output on the load.
        """
        self._write_cmd(f'MEAS:CURR?')
        resp = str(self.controller.read_until(self.address, _HP606XB_TERMINATOR.encode('ascii')), 'ascii')
        resp = resp[:resp.index(_HP606XB_TERMINATOR)]
        return float(resp)

    def get_load_power(self, channel: int) -> float:
        """
        Gets the current power input on the load. Channel is required, but not used. Use `0`

        :return: Measurement of power in watts
        """
        self._write_cmd(f'MEAS:POW?')
        resp = str(self.controller.read_until(self.address, _HP606XB_TERMINATOR.encode('ascii')), 'ascii')
        resp = resp[:resp.index(_HP606XB_TERMINATOR)]
        return float(resp)

    def get_load_resistance(self, channel: int) -> float:
        """
        Gets the current resistance input on the load. Channel is required, but not used. Use `0`

        Looks like this only returns the last set value for the RES command, not current voltage on the load.

        :return: Last set resistance
        """
        self._write_cmd(f'RES?')
        resp = str(self.controller.read_until(self.address, _HP606XB_TERMINATOR.encode('ascii')), 'ascii')
        resp = resp[:resp.index(_HP606XB_TERMINATOR)]
        return float(resp)

    def get_load_discharge_time(self, channel: int) -> timedelta:
        raise NotImplementedError()

    def get_load_watthours(self, channel: int) -> float:
        raise NotImplementedError()

    def get_load_capacity(self, channel: int) -> float:
        raise NotImplementedError()

    def clear_errors(self):
        """Clears errors in remote commanding."""
        self._write_cmd("*CLS")

    def reset(self):
        """Resets the HP Load to a known state via the *RST command."""
        # The *RST command will set the Load back to a known state
        self._write_cmd("*RST")

    def close(self):
        """Closes the context to the power supply, doing any necessary cleanup."""
        self.reset()


# ---------------------------- HP PSU Implementations ----------------------------
def HP606XBInstrument(load_type):
    """
    Decorator to concretely implement each subtype of the HP606X Load line.
    """
    try:
        chan_capabilities = HP606XChannelCapabilities[load_type]
        inst_capabilities = HP606XInstrumentCapabilities[load_type]
    except KeyError:
        # This is really a type error, user specified power supply that doesnt exist.
        raise TypeError(f'{load_type} is not apart of HP662XType or HP663XType.')
    context = _HP606XBContext

    def wrap(c):
        class _HP66XXA(Instrument, c):
            """
            The base HP662XA instruments decorator. Use this to define the HP662XA series instruments.
            """

            def __init__(self, controller: PrologixController, gpib_address: int):
                """
                Initializes the HP 606XB pumpkin_instrument with the given GPIB Prologix controller at the specified
                GPIB address
                """
                self.controller = controller
                self.address = gpib_address

            @classmethod
            def instrument_capabilities(cls) -> Any:
                return inst_capabilities

            @classmethod
            def channel_capabilities(cls) -> List[Any]:
                return chan_capabilities

            @contextmanager
            def use(self) -> ContextManager[Load]:
                load = context(self.controller, self.address, load_type, inst_capabilities, chan_capabilities)
                # Prepare the powersupply by zeroing out the settings
                load.reset()
                yield load
                load.close()

            @classmethod
            def instrument_type(cls) -> InstrumentType:
                return InstrumentType.PowerSupply

        return _HP66XXA

    return wrap


@HP606XBInstrument(HP606XType.HP6060B)
class HP6060B:
    pass
