import tornado.web
import tornado.ioloop
import tornado.platform.asyncio
import asyncio
import threading
import time
import filehandling
import sqlq
import re
import handlers


__ALL__ = ["TA"]


asyncio.set_event_loop_policy(tornado.platform.asyncio.AnyThreadEventLoopPolicy())


class TA(object):
    def __init__(self, domain: str, servers: dict, db: str, db_port: int, writer_port: int, cookie_secret: str, port: int = 8888):
        def _translate_host(server, pages):
            NotFound_page = handlers.NotFound
            if server == "" or server == "root":
                host = domain
            elif re.search(r"[0-9]{1,3}(\.[0-9]{1,3}){3}", server):
                host = server
            else:
                NotFound_page = type("NotFound_{}".format(server), (handlers.NotFound,), {"server": server})
                host = server+"."+domain
            return (tornado.web.HostMatches(host), pages+[(r"/(.*)", NotFound_page)])
        self.cookie_secret = cookie_secret
        self.port = port
        self.servers = [_translate_host(k, v) for k, v in servers.items()]
        self.servers.append((tornado.web.HostMatches(r".*"), [(r"/(.*)", handlers.NotFound)]))
        self.sqlqueue = sqlq.SqlQueueU(server=True, db=db, db_port=db_port, timeout_commit=30*1000, auto_backup=False)
        self.writer = filehandling.WriterU(server=True, writer_port=writer_port)

    def _start(self) -> None:
        self.server = tornado.ioloop.IOLoop.instance()
        app = tornado.web.Application(
            self.servers,
            xsrf_cookies=True,
            cookie_secret=self.cookie_secret
        )
        app.listen(self.port)
        self.server.start()

    def start(self) -> None:
        p = threading.Thread(target=self._start)
        p.daemon = True
        p.start()

    def stop(self, stop_app_worker) -> None:
        self.server.stop()
        while True:
            if len(handlers.File.rh) == 0:
                break
            print("no. of requests remaining:", len(handlers.File.rh), flush=True)
            time.sleep(0.5)
        stop_app_worker()
        self.sqlqueue.commit()
        self.sqlqueue.stop()
        self.writer.stop()


