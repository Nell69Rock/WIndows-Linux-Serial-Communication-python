# LINUX_WIN_PYTHON_SERIAL_COMMUNICATION
- This program is for basic serial communication. It supports input and output.
- Supported OS WIN, LINUX, MAC (coming soon...)

## Preperlation

```
> pip3 install -r requirements.txt

- If it does not work, enter the following command and install it again.

> pip3 uninstall -r requirements.txt
```

## Run UART

```
usage: UART.py [-h] -p /dev/ttyUSB1 [-buad 9600] [-bsize 8] [-prty N] [-sbits 1] [-tout 1] [-xonxoff] [-rtscts] [-wtout 1] [-dsrdtr] [-ibtout None] [-exclusive True]
               [-w WATCH_PATTERN [WATCH_PATTERN ...]] [-e]

optional arguments:
  -h, --help
          show this help message and exit
  -p /dev/ttyUSB1, --port /dev/ttyUSB1
          Enter device path for uart connection. i.e (/dev/ttyUSB1, COM30, etc...)
  -buad 9600, --baudrate 9600
          Baud rate such as 9600 or 115200 etc. (Default : 115200)
  -bsize 8, --bytesize 8
          Number of data bits. (Default : 8)
          choices [5, 6, 7, 8]
  -prty N, --parity N
          Enable parity checking. (Default : N)
          choices=[N, E, O, M, S]
  -sbits 1, --stopbits 1
          Number of stop bits. (Default : 1)
          choices=[1, 1.5, 2]
  -tout 1, --timeout 1
          Set a read timeout value in seconds. (Default : None)
  -xonxoff, --xonxoff
          Enable software flow control. (Default : False)
          if this feature activated xonxoff is True state.
  -rtscts, --rtscts
          Enable hardware (RTS/CTS) flow control. (Default : False)
          if this feature activated rtscts is True state.
  -wtout 1, --write_timeout 1
          Set a write timeout value in seconds. (Default : None)
  -dsrdtr, --dsrdtr
          Enable hardware (DSR/DTR) flow control. (Default : False)
          if this feature activated dsrdtr is True state.
  -ibtout None, --inter_byte_timeout None
           Inter-character timeout. (Default : None)
  -exclusive True, --exclusive True
          Set exclusive access mode (POSIX only).
          A port cannot be opened in exclusive access mode
          if it is already open in exclusive access mode.(Default : None)
  -w WATCH_PATTERN [WATCH_PATTERN ...], --watch WATCH_PATTERN [WATCH_PATTERN ...]
          Enter the Watch pattern what you want. entered pattern ignores case.
          Patterns are separated by spaces.                        
          e.g. -w ASSERT WARNING ERROR etc...
  -e, --watch_end
          When this feature is activated, it is automatically terminated when the pattern is matched.

i.e) > LINUX : 'sudo python3 UART.py -p /dev/ttyUSB1'
     > WIN   : 'python3 UART.py -p COM27'

See help for more information.
```
## Log Directory
- Windows
    - `'C:\Users\[USERNAME]\log'`
- Ubuntu
    -  `'~/log'`
    - Warning : If you want to view the log, run it as administrator privileges.