import sys
class Logger(object):
    def __init__(self, filename='a.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message+'\n')
        self.log.write(message+'\n')

    def flush(self):
        pass

sys.stdout = Logger('a.log', sys.stdout)
sys.stderr = Logger('a.log', sys.stderr)     # redirect std err, if necessary

# now it works
# print('print something')