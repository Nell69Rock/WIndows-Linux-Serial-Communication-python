import serial
import serial.serialutil
from serial.serialutil import SerialBase, SerialException, to_bytes, \
    PortNotOpenError, SerialTimeoutException, Timeout

class UART:
    def __init__(self, port_name = '/dev/ttyUSB1', baudrate = 115200, bytesize = 8,
        parity = 'N', stopbits = 1, timeout = None, xonxoff = False, rtscts = False,
        write_timeout = None, dsrdtr = False, inter_byte_timeout = None, exclusive = None):
        self.Serial = None
        self.port_name = port_name
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self.write_timeout = write_timeout
        self.dsrdtr = dsrdtr
        self.inter_byte_timeout = inter_byte_timeout
        self.exclusive = exclusive

    def Connection(self):
        try:
            self.Serial = serial.Serial(self.port_name, self.baudrate, self.bytesize,
            self.parity, self.stopbits, self.timeout, self.xonxoff, self.rtscts, self.write_timeout,
            self.dsrdtr, self.inter_byte_timeout, self.exclusive)
        except (SerialException, PortNotOpenError) as ex:
            self.Serial = None
            print(ex)
            return 1
        return 0

    def Disconnection(self):
        self.Serial.close()
        pass
    
    def ReadBytes(self):
        res = self.Serial.read(1)
        return res

    def WriteBytes(self, send_byte):
        self.Serial.write(send_byte)

    def ReadLine(self):
        res = self.Serial.readline()
        return res

    def WriteLine(self, send_line):
        self.Serial.writelines(send_line)