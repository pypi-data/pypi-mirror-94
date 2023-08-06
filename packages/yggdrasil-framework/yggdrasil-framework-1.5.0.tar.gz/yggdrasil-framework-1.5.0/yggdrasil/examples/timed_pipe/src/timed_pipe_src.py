from __future__ import print_function
import sys
from yggdrasil.interface.YggInterface import YggOutput


def run(args):
    msg_count = int(args[0])
    msg_size = int(args[1])
    print('Hello from Python pipe_src: msg_count = %d, msg_size = %d' % (
        msg_count, msg_size))

    # Ins/outs matching with the the model yaml
    outq = YggOutput('output_pipe')
    print("pipe_src(P): Created I/O channels")

    # Send test message multiple times
    test_msg = b'0' * msg_size
    count = 0
    for i in range(msg_count):
        ret = outq.send(test_msg)
        if not ret:
            raise RuntimeError('pipe_src(P): SEND ERROR ON MSG %d' % i)
        count += 1

    print('Goodbye from Python source. Sent %d messages.' % count)
    

if __name__ == '__main__':
    run(sys.argv[1:])
