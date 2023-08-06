import time
import random
from pathlib import Path
from adcopen.win_service_base import WinServiceBase

class ServiceExample(WinServiceBase):
    _svc_name_ = "ADC Service Example"
    _svc_display_name_ = "ADC WinServiceBase Example"
    _svc_description_ = "An example of making a service in python."

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        i = 0
        while self.isrunning:
            random.seed()
            x = random.randint(1, 1000000)
            Path(f'c:{x}.txt').touch()
            time.sleep(5)

if __name__ == '__main__':
    ServiceExample.parse_command_line()