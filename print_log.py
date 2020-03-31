import argparse
import struct
import codecs

from joycontrol.report import InputReport, OutputReport


def eof_read(file, size):
    """
    Raises EOFError if end of file is reached.
    """
    data = file.read(size)
    if not data:
        raise EOFError()
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('capture_file')
    args = parser.parse_args()

    with open(args.capture_file, 'rb') as capture:
        try:
            start_time = None
            while True:
                # parse capture time
                time = struct.unpack('d', eof_read(capture, 8))[0]
                if start_time is None:
                    start_time = time

                # parse data size
                size = struct.unpack('i', eof_read(capture, 4))[0]
                # parse data
                data = list(eof_read(capture, size))

                if data[0] == 0xA1:
                    input_report = InputReport(data)
                    print("Input  ", codecs.encode(bytes(input_report), 'hex'))
                elif data[0] == 0xA2:
                    output_report = OutputReport(data)
                    print("Output ", codecs.encode(bytes(output_report), 'hex'))
                else:
                    raise ValueError('unexpected data')
        except EOFError:
            pass

