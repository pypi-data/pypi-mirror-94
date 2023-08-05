__version__ = "0.0.10"
__keywords__ = ["tornado ajax wrapper framework"]


# if not __version__.endswith(".0"):
#     import re
#     print(f"version {__version__} is deployed for automatic commitments only", flush=True)
#     print("install version " + re.sub(r"([0-9]+\.[0-9]+\.)[0-9]+", r"\g<1>0", __version__) + " instead")
#     import os
#     os._exit(1)


import sys
from filehandling import abs_main_dir


app_root = abs_main_dir(depth=2)
sys.path.extend([abs_main_dir(depth=1)])
print("sys.path:", sys.path)


import tornado
import tornado.web
import tornado.gen
import os
import threading
import time
import core
import handlers
import traceback
import requests
import aescipher
from omnitools import sha3_512hd


def start_app_worker():
    for app_worker in app_workers:
        app_worker.start()


def stop_app_worker():
    for app_worker in app_workers:
        app_worker.stop()


def start():
    handlers.BaseRequestHandler.app_root = app_root
    handlers.BaseRequestHandler.db_port = app_settings["db_port"]
    handlers.BaseRequestHandler.writer_port = app_settings["writer_port"]
    handlers.BaseRequestHandler.cookies_domain = "." + app_settings["domain"]
    handlers.BaseRequestHandler.cookies_expires_day = app_settings["cookies_expires_day"]
    handlers.BaseRequestHandler.under_maintenance = True
    for app_worker in app_workers:
        app_worker.maintenance(True)
    ta = core.TA(
        app_settings["domain"],
        app_settings["servers"],
        app_settings["db"],
        app_settings["db_port"],
        app_settings["writer_port"],
        sha3_512hd(app_settings["cookie_secret"]),
        app_settings["port"]
    )
    ta.start()
    start_app_worker()
    print("started")
    interactive_input(ta)


def stop(ta):
    ta.stop(stop_app_worker)
    print("exiting")
    time.sleep(2)
    os._exit(0)


def printTable(myDict, colList=None):
       if not colList:
           colList = list(myDict[0].keys() if myDict else [])
       myList = [colList]
       for item in myDict:
           myList.append([str(item[col] if item[col] is not None else '') for col in colList])
       colSize = [max(map(len,col)) for col in zip(*myList)]
       formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
       myList.insert(1, ['-' * i for i in colSize])
       for item in myList:
           print(formatStr.format(*item))


def interactive_input(ta):
    while True:
        print("Enter 'help' for commands.")
        command = input("> ")
        if not command:
            continue
        elif command == "help":
            print('''Commands:
    commit: Commit sqlite database
    maintenance: Render server as '503 Service Unavailable'
    resume: Resume server from maintenance
    sql <SQL statement>: Execute SQL statement
    stop: Stop server and commit
    terminate: Force stop server''')
        elif command == "clear":
            from sys import platform
            if platform == "win32":
                os.system("cls")
            else:
                os.system("clear")
        elif command == "commit":
            ta.sqlqueue.commit()
            print("sqlite: committed")
        elif command == "maintenance":
            handlers.BaseRequestHandler.under_maintenance = True
            for app_worker in app_workers:
                app_worker.maintenance(True)
            print("maintenance: True")
        elif command == "resume":
            handlers.BaseRequestHandler.under_maintenance = False
            for app_worker in app_workers:
                app_worker.maintenance(False)
            print("maintenance: False\nresume")
        elif command.startswith("sql "):
            sql = command[4:]
            try:
                result = ta.sqlqueue.sql(sql)
                printTable(result)
            except:
                pass
        elif command == "stop":
            print("stopping")
            stop(ta)
        elif command == "terminate":
            print("terminating")
            os._exit(1)
        else:
            print("unknown command")
        print()


exec(open(os.path.join(app_root, "app.py"), "rb").read().decode(), globals())
app_settings = globals()["app_settings"](app_root)
app_workers = globals()["app_workers"]()
if not os.path.isabs(app_settings["db"]):
    app_settings["db"] = os.path.join(app_root, app_settings["db"])
start()

