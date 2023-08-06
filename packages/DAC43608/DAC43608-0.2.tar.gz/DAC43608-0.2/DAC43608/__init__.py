import busio
import board
from adafruit_bus_device.i2c_device import I2CDevice


class DAC43608:

    # DAC43608 Command Byte
    # Controls which command is executed and which is being accessed.
    _DEVICE_CONFIG = 1
    _STATUS        = 2
    _BRDCAST       = 3
    A = 8
    B = 9
    C = 10
    D = 11



    def __init__(self, address=0x49):
        comm_port = busio.I2C(board.SCL, board.SDA)
        self.i2c = I2CDevice(comm_port, address)

    def power_up_all(self):
        # sets all channels to their registered value (default is 1 if nothing is in the register, i.e. maximum)
        self.write_config([0x00, 0x00])

    def power_up(self, channel):
        """
        Turn on the LED to its register value

        Parameters
        -----------

        channel: int
           an int between 8 to 11, aka, a `DAC43608.X` value
        """
        # this needs to first read the current state of the config, and then make the modification
        write_buffer = bytearray([self._DEVICE_CONFIG])
        read_buffer = bytearray(2)
        self.i2c.write_then_readinto(write_buffer, read_buffer)
        current_config = read_buffer[0] # the order is reversed from what I expected

        # write back to config the bitwise-or of our new channel and the old config.
        # example, if the current config is
        # 0b00001101
        # and we want to flip channel A on (the right-most digit), start with
        # 0b0001111
        # subtract 1 from the desired position (start from the right)
        # 0b0001111 - (1 << position)
        # and AND that with the original
        self.write_config([current_config & (0x0F - (1 << (channel-8))), 0x00])

    def power_down_all(self):
        # power down all outputs
        self.write_config([0xFF, 0xFF])

    def set_intensity_to(self, channel, fraction):
        """
        Set the output to a fraction of the maximum output. This only set it's in the register, you
        still need to power up the channel using `power_up`. This can happen before or after the register is
        populated.

        Parameters
        -----------

        channel: int
           an int between 8 to 11, aka, a `DAC43608.X` value
        fraction: float
           a float between 0 to 1, representing how much of the total maximum current
           to release.
        """

        assert 0 <= fraction <= 1, "must be between 0 and 1 inclusive."

        # first make sure it's powered up
        self.power_up(channel)


        SPAN = 112
        target = round(SPAN * fraction)
        a = target // 16
        b = target - a * 16

        self.write_dac(channel, [a, b * 16])
        return

    ### low level API

    def write_dac(self, command, data):
        buffer_ = bytearray([command, *data])
        self.i2c.write(buffer_)
        return

    def write_config(self, config_byte):
        self.write_dac(self._DEVICE_CONFIG, config_byte)
        return

    def write_dac_A(self, DACn_DATA):
        """
        DACn_DATA is an array of two bytes/integers, ex: [0x08, 0x04] or [15, 20]
        """
        self.write_dac(self.A, DACn_DATA)
        return

    def write_dac_B(self, DACn_DATA):
        self.write_dac(self.B, DACn_DATA)
        return

    def write_dac_C(self, DACn_DATA):
        self.write_dac(self.C, DACn_DATA)
        return

    def write_dac_D(self, DACn_DATA):
        self.write_dac(self.D, DACn_DATA)
        return
