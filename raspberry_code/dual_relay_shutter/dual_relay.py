from time import sleep
from machine import Pin


class DualRelayController():
    def __init__(self, pin_in1: int = 0, pin_in2: int = 1) -> None:
        """Initializes a DualRelayController object which allows to control a dual \
relay module such as the one shown in the following link: \
http://wiki.sunfounder.cc/index.php?title=2_Channel_5V_Relay_Module

        Parameters:
        -----------
            `pin_in1 {int, optional}`: The Raspberry's digital pin's number associated \
to the In1 pin of the Dual Relay Module. Defaults to 0.

            `pin_in2 {int, optional}`: The Raspberry's digital pin's number associated \
to the In2 pin of the Dual Relay Module. Defaults to 1.
        """
        self.rele0 = Pin(pin_in1, Pin.OUT, Pin.PULL_DOWN)
        self.rele1 = Pin(pin_in2, Pin.OUT, Pin.PULL_DOWN)
        print(self.rele_values())
        return None

    def rele_values(self, val0: int = None, val1: int = None) -> tuple[int]:
        if val0 is not None:
            self.rele0.value(val0)
        if val1 is not None:
            self.rele1.value(val1)
        return self.rele0.value(), self.rele1.value()

    def toggle_both(self, ) -> tuple[int]:
        self.rele0.toggle()
        self.rele1.toggle()
        return self.rele_values()

    def sleep_toggles(self, sleep_time_seconds: float | int) -> tuple[int]:
        self.rele0.toggle()
        sleep(sleep_time_seconds)
        self.rele1.toggle()
        return self.rele_values()


if __name__ == '__main__':
    relay_controller = DualRelayController(pin_in1=0, pin_in2=1)
    print(relay_controller.rele_values())
