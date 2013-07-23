import sys
import subprocess
import os
import time
from threading import Thread
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

ON_POSIX = 'posix' in sys.builtin_module_names


class WatchDog:
    def __init__(self, config):
        self.config = config
        self.sci = None
        self.outputthread = None
        self.queue = Queue()

    def startSci(self):
        self._openSci()
        self._startThread()
        self._watcher()

    def _restartSci(self):
        self._openSci()
        self._startThread()

    def _openSci(self):
        self.sci = subprocess.Popen([sys.executable, '-u', 'sci.py', config], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, close_fds=ON_POSIX)

    def _startThread(self):
        t = Thread(target=self.queue_output, args=(self.sci.stdout, self.queue))
        t.daemon = True  # thread dies with the program
        t.start()
        self.outputthread = t

    def queue_output(self, out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()

    def _watcher(self):
        while True:
            try:
                # read line without blocking
                try:
                    line = self.queue.get_nowait()  # or q.get(timeout=.1)
                except Empty:
                    pass
                else:  # got line
                    print line.rstrip()
                #polling
                status = self.sci.poll()
                if status is not None:
                    time.sleep(2)
                    self.outputthread.join()
                    print "-----------------------------"
                    self._restartSci()
                #thread sleep
                time.sleep(0.02)
            except KeyboardInterrupt:
                self.sci.terminate()
                sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        config = sys.argv[1]
    else:
        config = 'sci_config.xml'

    watchdog = WatchDog(config)
    watchdog.startSci()
