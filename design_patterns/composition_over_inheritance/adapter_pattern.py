import socket
import sys
import syslog


# https://python-patterns.guide/gang-of-four/composition-over-inheritance/
# The initial class.
class Logger(object):
    def __init__(self, file):
        self.file = file

    def log(self, message):
        self.file.write(message + '\n')
        self.file.flush()


# Two more classes, that send messages elsewhere.
class SocketLogger(Logger):
    def __init__(self, sock):
        self.sock = sock

    def log(self, message):
        # ?: This method is just overwriting parent's log, giving us a similar interface as a user but not really doing the same things.
        self.sock.sendall((message + '\n').encode('ascii'))


class SyslogLogger(Logger):
    def __init__(self, priority):
        self.priority = priority

    def log(self, message):
        syslog.syslog(self.priority, message)


# New design direction: filtering messages.
class FilteredLogger(Logger):
    def __init__(self, pattern, file):
        self.pattern = pattern
        super().__init__(file)

    def log(self, message):
        if self.pattern in message:
            super().log(message)


# # This will work but this can get out of hand really quickly if we start designing filters for each type of logger.
# f = FilteredLogger('Error', sys.stdout)
# f.log('Ignored: this is not important')
# f.log('Error: but you want to see this')

# ?: This is a prime example of “proliferation of classes” and “explosion of subclasses”. We can see that SocketLogger and SyslogLogger are both writng to their specific output using the log() method. What if the task of logging is left to Logger and where it needs to log is passed as a parameter?


class FileLikeSocket:
    def __init__(self, sock):
        self.sock = sock

    def write(self, message_and_newline):
        self.sock.sendall(message_and_newline.encode('ascii'))

    def flush(self):
        pass


class FileLikeSyslog:
    def __init__(self, priority):
        self.priority = priority

    def write(self, message_and_newline):
        message = message_and_newline.rstrip('\n')
        syslog.syslog(self.priority, message)

    def flush(self):
        pass

# ?: These two classes act/behave like FileSystem (file) classes. Even though they don't have all the methods in them but they have the methods which we will interact with like write().

# # This is better
# sock1, sock2 = socket.socketpair()

# fs = FileLikeSocket(sock1)
# logger = FilteredLogger('Error', fs)
# logger.log('Warning: message number one')
# logger.log('Error: message number two')

# print('The socket received: %r' % sock2.recv(512))
