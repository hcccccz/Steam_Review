from multiprocessing import Process
from web_server import app
from crawl import *
import signal


def app_run():
    app.run()
try:
    process1 = Process(target=crawl)
    process2 = Process(target=app_run)
    process1.start()
    process2.start()
    #
    process1.join()
    process2.join()
except KeyboardInterrupt:
    process1.terminate()
    process2.terminate()
