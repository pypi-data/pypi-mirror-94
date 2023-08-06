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
Implementations for the following HP Power supplies:
    - 6633A (Via Prologix GP-IB)
    - 6624A (Via Prologix GP-IB)
"""

from enum import Enum
from typing import ContextManager, List, Any
from contextlib import contextmanager

from .types import PowerSupplyProtectionModeAll, PowerSupplyCapability, \
    PowerSupplyChannelCapability, PowerSupply
from ..prologix import PrologixController
from ..types import InstrumentType
from ..instrument import Instrument


# ---------------------------- HP662X Types ----------------------------
class HP662XType(Enum):
    """
    Represents the specific 662X power supply used in the below helper class decorator.
    """
    HP6621A = 0
    HP6622A = 1
    HP6623A = 2
    HP6624A = 3
    HP6627A = 4


HP662XChannelCapabilities = {
    HP662XType.HP6621A: [PowerSupplyChannelCapability(min_voltage=0,
                                                      max_voltage=20.2,
                                                      max_current=10.3,
                                                      max_ocv=23,
                                                      protection_modes=PowerSupplyProtectionModeAll),
                         PowerSupplyChannelCapability(min_voltage=0,
                                                      max_voltage=20.2,
                                                      max_current=10.3,
                                                      max_ocv=23,
                                                      protection_modes=PowerSupplyProtectionModeAll)],
    HP662XType.HP6622A: [PowerSupplyChannelCapability(min_voltage=0,
                                                      max_voltage=50.5,
                                                      max_current=4.12,
                                                      max_ocv=55,
                                                      protection_modes=PowerSupplyProtectionModeAll),
                         PowerSupplyChannelCapability(min_voltage=0,
                                                      max_voltage=50.5,
                                                      max_current=4.12,
                                                      max_ocv=55,
                                                      protection_modes=PowerSupplyProtectionModeAll)],
    HP662XType.HP6623A: [PowerSupplyChannelCapability(min_voltage=0,
                                                      max_voltage=20.2,
                                                      max_current=5.15,
                                                      max_ocv=23,
                                                      protection_modes=PowerSupplyProtectionModeAll),
                         PowerSupplyChannelCapability(min_voltage=0,
                                                      max_voltage=20.2,
                                                      max_current=10.3,
                                                      max_ocv=23,
                                                      protection_modes=PowerSupplyProtectionModeAll),
                         PowerSupplyChannelCapability(min_voltage=0,
                                                      max_voltage=50.5,
                                                      max_current=2.06,
                                                      max_ocv=55,
                                                      protection_modes=PowerSupplyProtectionModeAll)],
    HP662XType.HP6624A: [PowerSupplyChannelCapability(min_voltage=0,
                                                      max_voltage=20.2,
                                                      max_current=5.15,
                                                      max_ocv=23,
                                                      protection_modes=PowerSupplyProtectionModeAll),
                         PowerSupplyChannelCapability(min_voltage=0,
                                                      max_voltage=20.2,
                                                      max_current=5.15,
                                                      max_ocv=23,
                                                      protection_modes=PowerSupplyProtectionModeAll),
                         PowerSupplyChannelCapability(min_voltage=0,
                                                      max_voltage=50.5,
                                                      max_current=2.06,
                                                      max_ocv=55,
                                                      protection_modes=PowerSupplyProtectionModeAll),
                         PowerSupplyChannelCapability(min_voltage=0,
                                                      max_voltage=50.5,
                                                      max_current=2.06,
                                                      max_ocv=55,
                                                      protection_modes=PowerSupplyProtectionModeAll)],
    HP662XType.HP6627A: [PowerSupplyChannelCapability(min_voltage=0,
                                                      max_voltage=50.5,
                                                      max_current=2.06,
                                                      max_ocv=55,
                                                      protection_modes=PowerSupplyProtectionModeAll),
                         PowerSupplyChannelCapability(min_voltage=0,
                                                      max_voltage=50.5,
                                                      max_current=2.06,
                                                      max_ocv=55,
                                                      protection_modes=PowerSupplyProtectionModeAll),
                         PowerSupplyChannelCapability(min_voltage=0,
                                                      max_voltage=50.5,
                                                      max_current=2.06,
                                                      max_ocv=55,
                                                      protection_modes=PowerSupplyProtectionModeAll),
                         PowerSupplyChannelCapability(min_voltage=0,
                                                      max_voltage=50.5,
                                                      max_current=2.06,
                                                      max_ocv=55,
                                                      protection_modes=PowerSupplyProtectionModeAll)]
}
HP662XInstrumentCapabilities = {
    HP662XType.HP6621A: PowerSupplyCapability(),
    HP662XType.HP6622A: PowerSupplyCapability(),
    HP662XType.HP6623A: PowerSupplyCapability(),
    HP662XType.HP6624A: PowerSupplyCapability(),
    HP662XType.HP6627A: PowerSupplyCapability()
}


class _HP662XAContext(PowerSupply):
    """Represents the implementation of the SCPI protocol for the HP662X series of power supply."""

    def __init__(self,
                 controller: PrologixController,
                 address: int,
                 psu_type: HP662XType,
                 inst_capabilities: PowerSupplyCapability,
                 chan_capabilities: List[PowerSupplyChannelCapability]):
        """
        Initializes the HP663X power supply context, commanding the PSU with the given `controller`,
        `address` and `psu_type`.
        """
        super(_HP662XAContext, self).__init__()
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

    def set_output_ocp(self, channel: int, is_on: bool):
        """Sets the OCP ON or OFF on the HP662X PSU."""
        self._validate_channel(channel)

        self._write_cmd(f'OCP {channel + 1},{"1" if is_on else "0"}')

    def set_output_ovp(self, channel: int, value: float):
        """Sets the OVP to the specified value."""
        self._validate_channel(channel)

        if value > self.channel_capabilities[channel].max_ocv:
            raise ValueError(
                f'{value} is greater than the OCV max of {self.channel_capabilities[channel].max_ocv} for the {self.name} on channel #{channel + 1}.')

        self._write_cmd(f'OVSET {channel + 1},{value}')

    def get_output_voltage(self, channel: int) -> float:
        """Gets the voltage on the output of the power supply."""
        self._validate_channel(channel)

        self._write_cmd(f'VOUT? {channel + 1}')
        resp = str(self.controller.read_until(self.address, _HP66XX_TERMINATOR.encode('ascii')), 'ascii')
        resp = resp[:resp.index(_HP66XX_TERMINATOR)]
        return float(resp)

    def get_output_current(self, channel: int) -> float:
        """Gets the output current on `channel` of the PSU."""
        self._validate_channel(channel)

        self._write_cmd(f'IOUT? {channel + 1}')
        resp = str(self.controller.read_until(self.address, _HP66XX_TERMINATOR.encode('ascii')), 'ascii')
        resp = resp[:resp.index(_HP66XX_TERMINATOR)]
        return float(resp)

    def clear_errors(self):
        """Same as clear_faults in this case."""
        self.clear_faults()

    def clear_faults(self):
        """Clears OVP and OCP faults via RST command."""
        for chan in range(self.num_channels):
            self._write_cmd(f'OVRST {chan + 1}')
            self._write_cmd(f'OCRST {chan + 1}')

    @property
    def error_count(self) -> int:
        """Reads the ERR register on the PSU via `ERR?` query."""
        self._write_cmd('ERR?')
        resp = str(self.controller.read_until(self.address, _HP66XX_TERMINATOR.encode('ascii')), 'ascii')
        resp = resp[:resp.index(_HP66XX_TERMINATOR)]
        return int(resp)

    @property
    def fault_count(self) -> int:
        """Reads the FAULT register on the PSU via `FAULT?` query"""
        self._write_cmd('FAULT?')
        resp = str(self.controller.read_until(self.address, _HP66XX_TERMINATOR.encode('ascii')), 'ascii')
        resp = resp[:resp.index(_HP66XX_TERMINATOR)]
        return int(resp)

    def set_output_on(self, channel: int, is_on: bool):
        """Uses the 663XA Syntax for the output command."""
        self._validate_channel(channel)
        self._write_cmd(f'OUT {channel + 1},{"1" if is_on else "0"}')

    def set_output_voltage(self, channel: int, voltage: float):
        """Uses the 663XA syntax for the output voltage command."""
        self._validate_channel(channel)

        if voltage > self.channel_capabilities[channel].max_voltage \
                or voltage < self.channel_capabilities[channel].min_voltage:
            raise ValueError(
                f'{voltage} is outside of the voltage range [{self.channel_capabilities[channel].min_voltage}, {self.channel_capabilities[channel].max_voltage}] for the {self.name} on channel #{channel + 1}.')

        self._write_cmd(f'VSET {channel + 1},{voltage}')

    def set_output_current(self, channel: int, current: float):
        """Uses the 663XA syntax for the output current command."""
        self._validate_channel(channel)

        if current > self.channel_capabilities[channel].max_current:
            raise ValueError(
                f'{current} is greater than the current max of {self.channel_capabilities[channel].max_current} for the {self.name} on channel #{channel + 1}.')

        self._write_cmd(f'ISET {channel + 1},{current}')

    def close(self):
        """Closes the context to the power supply, doing any necessary cleanup."""
        # Make power supply set all voltage to 0 and current to 0
        for i in range(self.num_channels):
            self.set_output_current(i, 0)
            self.set_output_voltage(i, 0)
        self._write_cmd('CLR')


# ---------------------------- HP663X Types ----------------------------
class HP663XType(Enum):
    """Represents the specific HP 663X implementation to use."""
    HP6632A = 0
    HP6633A = 1
    HP6634A = 2


HP663XChannelCapabilities = {
    HP663XType.HP6632A: [PowerSupplyChannelCapability(min_voltage=0,
                                                      max_voltage=20.5,
                                                      max_current=5.2,
                                                      max_ocv=22,
                                                      protection_modes=PowerSupplyProtectionModeAll)],
    HP663XType.HP6633A: [PowerSupplyChannelCapability(min_voltage=0,
                                                      max_voltage=51.2,
                                                      max_current=2.05,
                                                      max_ocv=55,
                                                      protection_modes=PowerSupplyProtectionModeAll)],
    HP663XType.HP6634A: [PowerSupplyChannelCapability(min_voltage=0,
                                                      max_voltage=102.4,
                                                      max_current=1.03,
                                                      max_ocv=110,
                                                      protection_modes=PowerSupplyProtectionModeAll)]
}
HP663XInstrumentCapabilities = {
    HP663XType.HP6632A: PowerSupplyCapability(),
    HP663XType.HP6633A: PowerSupplyCapability(),
    HP663XType.HP6634A: PowerSupplyCapability()
}
_HP66XX_TERMINATOR = "\r\n"


class _HP663XAContext(PowerSupply):
    """The implementation of the SCPI protocol for the HP663X series of power supply."""

    def __init__(self,
                 controller: PrologixController,
                 address: int,
                 psu_type: HP663XType,
                 inst_capabilities: PowerSupplyCapability,
                 chan_capabilities: List[PowerSupplyChannelCapability]):
        """
        Initializes the HP663X power supply context, commanding the PSU with the given `controller`,
        `address` and `psu_type`.
        """
        super(_HP663XAContext, self).__init__()
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
        """Validates the channel, raising an exception if it is incorrect."""
        if channel >= self.num_channels:
            raise ValueError(f'There is no #{channel + 1} channel on the {self.name}')

    def set_output_ocp(self, channel: int, is_on: bool):
        """Sets the OCP ON or OFF on the HP663X PSU. Channel should always be 0."""
        self._validate_channel(channel)

        self._write_cmd(f'OCP {"1" if is_on else "0"}')

    def set_output_ovp(self, channel: int, value: float):
        """Sets the OVP to the specified value. Channel should always be 0."""
        self._validate_channel(channel)

        if value > self.channel_capabilities[channel].max_ocv:
            raise ValueError(
                f'{value} is greater than the OCV max of {self.channel_capabilities[channel].max_ocv} for the {self.name}')

        self._write_cmd(f'OVSET {value}')

    def get_output_voltage(self, channel: int) -> float:
        """Gets the voltage on the output of the power supply. Channel should always be 0."""
        self._validate_channel(channel)

        self._write_cmd('VOUT?')
        resp = str(self.controller.read_until(self.address, _HP66XX_TERMINATOR.encode('ascii')), 'ascii')
        resp = resp[:resp.index(_HP66XX_TERMINATOR)]
        return float(resp)

    def get_output_current(self, channel: int) -> float:
        """Gets the output current on the PSU."""
        self._validate_channel(channel)

        self._write_cmd('IOUT?')
        resp = str(self.controller.read_until(self.address, _HP66XX_TERMINATOR.encode('ascii')), 'ascii')
        resp = resp[:resp.index(_HP66XX_TERMINATOR)]
        return float(resp)

    def clear_errors(self):
        """Clears the command errors on the power supply via RST command. Same as clear_faults in this case."""
        self.clear_faults()

    def clear_faults(self):
        """Clears OVP and OCP faults via RST command."""
        self._write_cmd('RST')

    @property
    def error_count(self) -> int:
        """Reads the ERR register on the PSU via `ERR?` query."""
        self._write_cmd('ERR?')
        resp = str(self.controller.read_until(self.address, _HP66XX_TERMINATOR.encode('ascii')), 'ascii')
        resp = resp[:resp.index(_HP66XX_TERMINATOR)]
        return int(resp)

    @property
    def fault_count(self) -> int:
        """Reads the FAULT register on the PSU via `FAULT?` query"""
        self._write_cmd('FAULT?')
        resp = str(self.controller.read_until(self.address, _HP66XX_TERMINATOR.encode('ascii')), 'ascii')
        resp = resp[:resp.index(_HP66XX_TERMINATOR)]
        return int(resp)

    def set_output_on(self, channel: int, is_on: bool):
        """Uses the 663XA Syntax for the output command."""
        self._validate_channel(channel)
        self._write_cmd(f'OUT {"1" if is_on else "0"}')

    def set_output_voltage(self, channel: int, voltage: float):
        """Uses the 663XA syntax for the output voltage command."""
        self._validate_channel(channel)

        if voltage > self.channel_capabilities[channel].max_voltage \
                or voltage < self.channel_capabilities[channel].min_voltage:
            raise ValueError(
                f'{voltage} is outside of the voltage range [{self.channel_capabilities[channel].min_voltage}, {self.channel_capabilities[channel].max_voltage}] for the {self.name}')

        self._write_cmd(f'VSET {voltage}')

    def set_output_current(self, channel: int, current: float):
        """Uses the 663XA syntax for the output current command."""
        self._validate_channel(channel)

        if current > self.channel_capabilities[channel].max_current:
            raise ValueError(
                f'{current} is greater than the OCV max of {self.channel_capabilities[channel].max_current} for the {self.name}')

        self._write_cmd(f'ISET {current}')

    def close(self):
        """Closes the context to the power supply, doing any necessary cleanup. Does nothing presently"""
        self.set_output_voltage(0, 0)
        self.set_output_current(0, 0)
        self._write_cmd('CLR')


# ---------------------------- HP PSU Implementations ----------------------------
def HP66XXAInstrument(psu_type):
    """
    Decorator to concretely implement each subtype of the HP662X PSU line.
    """
    try:
        chan_capabilities = HP662XChannelCapabilities if psu_type in HP662XChannelCapabilities else HP663XChannelCapabilities
        chan_capabilities = chan_capabilities[psu_type]
        inst_capabilities = HP662XInstrumentCapabilities if psu_type in HP662XInstrumentCapabilities else HP663XInstrumentCapabilities
        inst_capabilities = inst_capabilities[psu_type]
    except KeyError:
        # This is really a type error, user specified power supply that doesnt exist.
        raise TypeError(f'{psu_type} is not apart of HP662XType or HP663XType.')
    context = _HP662XAContext if psu_type in HP662XChannelCapabilities else _HP663XAContext

    def wrap(c):
        class _HP66XXA(Instrument, c):
            """
            The base HP662XA instruments decorator. Use this to define the HP662XA series instruments.
            """

            def __init__(self, controller: PrologixController, gpib_address: int):
                """
                Initializes the HP 66XXA pumpkin_instrument with the given GPIB Prologix controller at the specified
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
            def use(self) -> ContextManager[PowerSupply]:
                psu = context(self.controller, self.address, psu_type, inst_capabilities, chan_capabilities)
                # Prepare the powersupply by zeroing out the settings
                psu.clear_faults()
                for i in range(psu.num_channels):
                    psu.set_output_current(i, 0)
                    psu.set_output_voltage(i, 0)
                yield psu
                psu.close()

            @classmethod
            def instrument_type(cls) -> InstrumentType:
                return InstrumentType.PowerSupply

        return _HP66XXA

    return wrap


@HP66XXAInstrument(HP662XType.HP6621A)
class HP6621A:
    pass


@HP66XXAInstrument(HP662XType.HP6622A)
class HP6622A:
    pass


@HP66XXAInstrument(HP662XType.HP6623A)
class HP6623A:
    pass


@HP66XXAInstrument(HP662XType.HP6624A)
class HP6624A:
    pass


@HP66XXAInstrument(HP662XType.HP6627A)
class HP6627A:
    pass


@HP66XXAInstrument(HP663XType.HP6632A)
class HP6632A:
    pass


@HP66XXAInstrument(HP663XType.HP6633A)
class HP6633A:
    pass


@HP66XXAInstrument(HP663XType.HP6634A)
class HP6634A:
    pass
