import threading
import serial
from PySide6.QtCore import QObject, Signal
from time import sleep
class SerialReader(QObject):
    barcode_read = Signal(str)

    def __init__(self,port=None,baud=115200, timeout=1):
        super().__init__()
        self._port = port
        self._baudrate = baud
        self._timeout = timeout
        self._running = False
        self._serial = None
        self._thread = None
        if self._port and self._baudrate:
            self.start(self._port,self._baudrate)

    def start(self,port:str,baud=115200):
        if self._running:
            self.stop()
        self._port = port
        self._baudrate = baud
        if not port:
            return
        self._running = True
        self._serial = serial.Serial(self._port, self._baudrate, timeout=self._timeout)
        self._thread = threading.Thread(target=self._read_loop)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()
        if self._serial and self._serial.is_open:
            self._serial.close()

    @staticmethod
    def get_ports():
        available_ports = [port.device for port in serial.tools.list_ports.comports() if 'ttyS' not in port.device]
        return available_ports

    def _read_loop(self):
        while self._running:
            if self._port == None:
                sleep(1)
                continue
            try:
                if not self._serial.is_open:
                    self._serial.open()
                
                if self._serial.in_waiting > 0:
                    data = self._serial.readline().decode().strip()
                    self.barcode_read.emit(data)
            except Exception as e:
                print("Serial Loop:" + str(e))
                sleep(1)
            sleep(0.1)

