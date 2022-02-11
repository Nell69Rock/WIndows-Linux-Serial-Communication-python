import subprocess
import class_serial_uart
import os, sys, platform, re
import argparse
from argparse import ArgumentParser
import datetime
import threading
try:
    import thread
except ImportError:
    import _thread as thread
import time

tx_data = u''
lock = threading.Lock()
uart_instance = None
log_fname = ''

def parse_cmd(argc):
    less_indent_formatter = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=10)
    parser = ArgumentParser(formatter_class=less_indent_formatter)
    parser.add_argument('-p', '--port', dest='port', type=str, required=True,
                    help='Enter device path for uart connection. i.e (/dev/ttyUSB1, COM30, etc...)', metavar='/dev/ttyUSB1')

    parser.add_argument('-buad', '--baudrate', dest='baudrate', type=int,
                    default = 115200,
                    help='Baud rate such as 9600 or 115200 etc. (Default : 115200)', metavar='9600')

    parser.add_argument('-bsize', '--bytesize', dest='bytesize', type=int, choices = [5, 6, 7, 8],
                    default = 8,
                    help='Number of data bits. (Default : 8)\nchoices [5, 6, 7, 8]', metavar='8')

    parser.add_argument('-prty', '--parity', dest='parity', type=str, choices=['N', 'E', 'O', 'M', 'S'],
                    default = 'N',
                    help='Enable parity checking. (Default : N)\nchoices=[N, E, O, M, S]', metavar='N')

    parser.add_argument('-sbits', '--stopbits', dest='stopbits', type=int, choices=[1, 1.5, 2],
                    default = 1,
                    help='Number of stop bits. (Default : 1)\nchoices=[1, 1.5, 2]', metavar='1')
    
    parser.add_argument('-tout', '--timeout', dest='timeout', type=float,
                    default = None,
                    help='Set a read timeout value in seconds. (Default : None)', metavar='1')

    parser.add_argument('-xonxoff', '--xonxoff', dest='xonxoff', action='store_true', 
                    default = False,
                    help='Enable software flow control. (Default : False)\nif this feature activated xonxoff is True state.')
    
    parser.add_argument('-rtscts', '--rtscts', dest='rtscts', action='store_true', 
                    default = False,
                    help='Enable hardware (RTS/CTS) flow control. (Default : False)\nif this feature activated rtscts is True state.')

    parser.add_argument('-wtout', '--write_timeout', dest='write_timeout', type=float,
                    default = None,
                    help='Set a write timeout value in seconds. (Default : None)', metavar='1')

    parser.add_argument('-dsrdtr', '--dsrdtr', dest='dsrdtr', action='store_true', 
                    default = False,
                    help='Enable hardware (DSR/DTR) flow control. (Default : False)\nif this feature activated dsrdtr is True state.')

    parser.add_argument('-ibtout', '--inter_byte_timeout', dest='inter_byte_timeout', type=float,
                    default=None,
                    help=' Inter-character timeout. (Default : None)', metavar='None')

    parser.add_argument('-exclusive', '--exclusive', dest='exclusive', type=bool, 
                    default=None,
                    help='Set exclusive access mode (POSIX only).\nA port cannot be opened in exclusive access mode\nif it is already open in exclusive access mode.(Default : None)',
                    metavar=True)
    parser.add_argument('-w', '--watch', dest='watch_pattern', nargs='+',
                    help='Enter the Watch pattern what you want. entered pattern ignores case.\nPatterns are separated by spaces.\
                        \ne.g. -w ASSERT WARNING ERROR etc...')

    parser.add_argument('-e', '--watch_end', dest='watch_end', action='store_true', default=False,
                    help='When this feature is activated, it is automatically terminated when the pattern is matched.')

    if argc <= 1:
        parser.print_help()
        sys.exit(0)

    (options, args) = parser.parse_known_args()
    return options

def init_log_folder(port_name):
    global log_fname
    port_name = re.sub("\!|\'|\/","", port_name)

    cmd = "awk -F'[/:]' '{if ($3 >= 1000 && $3 != 65534) print $1}' /etc/passwd"
    proc = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE,
                                             stderr = subprocess.STDOUT)
    
    res = proc.communicate()[0]

    res = res.decode('UTF-8', 'ignores').rstrip('\n')

    if (platform.system() == 'Linux'):
        log_dir = f'{os.path.expanduser(f"~/../home/{res}")}/log'
    elif (platform.system() == 'Windows'):
        log_dir = f'{os.path.expanduser("~")}/log'
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    log_fname = f'{log_dir}/{port_name}-{timestamp}.log'    
    check_exist_log_folder(log_dir)
    return 0

def check_exist_log_folder(log_dir):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

def get_current_time():
    now = datetime.datetime.now()
    nowTime = now.strftime('[%Y-%m-%d %H:%M:%S.%f] ')
    return nowTime

def watch_dog_pattern_match(rx_data, watch_pattern_list, b_watch_end, out_fd):
    msg = ''
    for pattern in watch_pattern_list:
        if (rx_data.find(pattern) == -1):
            continue
        print('\r\n\n==========PATTERN DECTED==========')
        out_fd.write('\r\n==========PATTERN DECTED==========\n')
        msg = 'UART : '+ pattern + ' detected!'
        print(msg, end = '')
        out_fd.write(msg)
        print('\r\n===============END===============')
        out_fd.write('\r\n===============END===============\n')
        if (b_watch_end):
            print('Termination due to pattern found.')
            return 1
        return 0
    return 0

def terminal_write_handler():
    global tx_data
    while True:
        try:
            tx_data = input()
            if (tx_data):
                uart_instance.WriteBytes((tx_data + u'\n').encode("utf8"))
                sys.stdout.flush()
                tx_data = u''
            time.sleep(1)
        except (KeyboardInterrupt):
            break

        except (class_serial_uart.SerialException, class_serial_uart.SerialTimeoutException, class_serial_uart.PortNotOpenError) as ex:
            print(ex)
            break

def run_read_proc(watch_pattern_list, b_watch_end):
    global tx_data
    byte_to_str = ''
    newline = 1
    out_fd = open(log_fname, 'w')
    while True:
        try:
            res = uart_instance.ReadBytes()

            if len(res) == 0:
                continue

            if res == b'\r': # carriage return to continue
                continue

            if newline == 1: # if the newline enable, send current time
                print(get_current_time(), end = '')
                out_fd.write(get_current_time())
                newline = 0

            rx_byte = res.decode('utf8', 'ignore')
            byte_to_str += rx_byte

            if rx_byte == '\n' and newline == 0:
                if (watch_pattern_list is not None):
                    ret = watch_dog_pattern_match(byte_to_str, watch_pattern_list, b_watch_end, out_fd)
                    if (ret):
                        break
                newline = 1
                byte_to_str = ''
            print(rx_byte, end = '')
            out_fd.write(rx_byte)
            sys.stdout.flush()
            out_fd.flush()
        except (KeyboardInterrupt):
            out_fd.close()
            break

        except (class_serial_uart.SerialException, class_serial_uart.SerialTimeoutException, class_serial_uart.PortNotOpenError) as ex:
            print(ex)
            out_fd.close()
            break
    return 0

def main(argc, argv):
    global uart_instance
    parse_option = parse_cmd(argc)
    uart_instance = class_serial_uart.UART(parse_option.port, parse_option.baudrate,
                    parse_option.bytesize, parse_option.parity, parse_option.stopbits,
                    parse_option.timeout, parse_option.xonxoff, parse_option.rtscts,
                    parse_option.write_timeout, parse_option.dsrdtr, parse_option.inter_byte_timeout,
                    parse_option.exclusive)
    
    if (uart_instance.Connection()):
        print('UART Connection Fail')
        return
    init_log_folder(parse_option.port)
    print('UART Connection Success')

    print('Name               : ', uart_instance.Serial.name)
    print('Baudrate           : ', uart_instance.Serial.baudrate)
    print('Bytesize           : ', uart_instance.Serial.bytesize)
    print('Parity Check       : ', uart_instance.Serial.parity)
    print('Stopbits           : ', uart_instance.Serial.stopbits)
    print('Timeout            : ', uart_instance.Serial.timeout)
    print('XON/XOFF           : ', uart_instance.Serial.xonxoff)
    print('RTS/CTS            : ', uart_instance.Serial.rtscts)
    print('Write timeout      : ', uart_instance.Serial.write_timeout)
    print('DSR/DTR            : ', uart_instance.Serial.dsrdtr)
    print('Inter byte timeout : ', uart_instance.Serial.inter_byte_timeout)
    print('Exclusive          : ', uart_instance.Serial.exclusive)
    print('UART Exit Command  : CTRL - C')

    thread.start_new_thread(terminal_write_handler, ())

    if (run_read_proc(parse_option.watch_pattern, parse_option.watch_end) == 0):
        uart_instance.Disconnection()

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
    sys.exit(1)