import hmac
import tornado.escape
import tornado.web
import os
import re
import math
import threading
import json
import time
import traceback
import email.utils
import datetime
import omnitools
import filehandling
import utils
import urllib.parse
from aescipher import AESCipher
from base64 import b32decode, b32encode


__ALL__ = ["BaseRequestHandler", "StaticFileHandler", "ErrorHandler", "NotFound", "File", "HTML", "AJAX"]


class BaseRequestHandler(tornado.web.RequestHandler):
    org_app_root = None
    app_root = None
    db_port = None
    writer_port = None
    cookies_domain = None
    cookies_expires_day = None
    server = None
    api_key = None
    decrypted_params = None
    under_maintenance = False

    def prepare(self):
        if "X-Real-Ip" in self.request.headers:
            if self.request.headers["Host"] == "127.0.0.1":
                self.write_error(401, msg="401 Unauthorized")
        if self.under_maintenance:
            self.set_status(503)
            try:
                self.write(open(os.path.join(self.org_app_root, "common", "maintenance.html"), "rb").read())
            except:
                self.write("<title>{msg}</title><body>{msg}</body>".format(msg="503 Service Unavailable"))
            self.finish()

    def set_cookie(self, k, v, expires_day=None, **kwargs) -> None:
        if expires_day is None:
            expires_day = self.cookies_expires_day
        try:
            kwargs.pop("expires_days")
        except:
            pass
        try:
            kwargs.pop("domain")
        except:
            pass
        super().set_cookie(k, v, domain=self.cookies_domain, expires_days=expires_day, **kwargs)

    def set_secure_cookie(self, k, v, expires_day=None, **kwargs) -> None:
        if expires_day is None:
            expires_day = self.cookies_expires_day
        if isinstance(v, str):
            v = v.encode()
        v += b" "+str(int(time.time()+self.cookies_expires_day*24*60*60)).encode()
        v = AESCipher(key=self.application.settings["cookie_secret"]).encrypt(v)
        self.set_cookie(k, v, domain=self.cookies_domain, expires_days=expires_day, **kwargs)

    def _get_secure_cookie(self, v):
        v = AESCipher(key=self.application.settings["cookie_secret"]).decrypt(v)
        if isinstance(v, bytes):
            v, ts = v.split(b" ")
            ts = ts.decode()
        else:
            v, ts = v.split(" ")
        if time.time() >= int(ts):
            return None
        return v

    def get_secure_cookie(self, k):
        v = self.get_cookie(k)
        if not v:
            return None
        return self._get_secure_cookie(v)

    def __init__(self, *args, **kwargs):
        self.org_app_root = self.app_root
        if self.server is not None:
            self.app_root = os.path.join(self.app_root, self.server)
        self.cookies_macros = {
            "get": self.get_cookie,
            "set": self.set_cookie,
            "get_secure": self.get_secure_cookie,
            "set_secure": self.set_secure_cookie,
        }
        super().__init__(*args, **kwargs)
        self.prepare_request_summary()
        self.prepare_xsrf()
        self.prepare_session_key()

    def prepare_xsrf(self):
        if self.get_secure_cookie("_xsrf") is None:
            self.set_secure_cookie("_xsrf", self.xsrf_token)

    def prepare_session_key(self):
        if self.get_cookie("session_key") is None:
            self.set_cookie("session_key", self.gen_session_key())

    def prepare_request_summary(self):
        try:
            _body = self.request.body.decode()
        except:
            _body = ""
            for _ in self.request.body:
                _body += "\\x{:02x}".format(_)
        headers = dict(self.request.headers)
        self.request_summary = {
            "timestamp": int(round(time.time()))
        }
        if "Host" in headers:
            self.request_summary.update({
                "Host": headers["Host"]
            })
            headers.pop("Host")
        if "X-Real-Ip" in headers:
            self.request_summary.update({
                "X-Real-Ip": headers["X-Real-Ip"]
            })
            del headers["X-Real-Ip"]
        self.request_summary.update({
            "method": self.request.method,
            "uri": self.request.uri,
            "body": _body,
        })
        self.request_summary.update(headers)

    def b32p(self, v):
        if len(v) % 8 > 0:
            v += "=" * (8 - len(v) % 8)
        return v

    def xor(self, k, v):
        v = b32decode(self.b32p(v))
        return bytes([_ ^ k[math.floor(i % len(k))] for i, _ in enumerate(v)])

    def gen_session_key(self):
        session_key = "_".join([str(_) for _ in omnitools.randb(16)])
        ts = str(int(time.time()+self.cookies_expires_day*24*60*60))
        sign = omnitools.mac(self.application.settings["cookie_secret"], session_key+ts, omnitools.sha256)
        return "|".join([session_key, ts, sign])

    def get_session_key(self):
        session_key, ts, sign = self.get_cookie("session_key").split("|")
        hd = omnitools.mac(self.application.settings["cookie_secret"], session_key+ts, omnitools.sha256)
        if time.time() >= int(ts) or hd != sign:
            return
        return [int(_) for _ in session_key.split("_")]

    def check_xsrf_cookie(self):
        if "X-Real-Ip" not in self.request.headers:
            if self.request.remote_ip == "127.0.0.1":
                return
        xsrf_error = "XSRF Token Error\n(Try remove cookies)"
        import binascii
        try:
            k = list(self.request.arguments.items())[0][0]
            self.api_key = json.loads(self.xor(self.get_session_key(), k))
            raw_params = list(self.request.arguments.items())[0][1][0]
            raw_params = self.xor(self.api_key, raw_params.decode())
            raw_params = "?"+raw_params.decode()
            raw_params = re.findall(r"(?:\?|\&)([^=]+)(?:\=)([^\&]*)", raw_params)
            params = {}
            for k, v in raw_params:
                if k not in params:
                    params[k] = []
                params[k].extend([urllib.parse.unquote(v)])
        except (IndexError, binascii.Error, UnicodeDecodeError, TypeError):
            return self.write_error(403, msg=xsrf_error)
        except:
            import traceback
            traceback.print_exc()
            return self.write_error(500, msg=traceback.format_exc())
        cookie_token = self.get_secure_cookie("_xsrf")
        if "_xsrf" not in params:
            return self.write_error(403, msg=xsrf_error)
        post_token = self._get_secure_cookie(params["_xsrf"][0])
        if post_token != cookie_token:
            return self.write_error(403, msg=xsrf_error)
        self.decrypted_params = params

    def dump_request_summary(self, fn):
        filehandling.WriterU(writer_port=self.writer_port).write(
            os.path.join(self.app_root, "log", fn+".log"),
            "ab",
            (json.dumps(self.request_summary, ensure_ascii=False)+"\n").encode()
        )

    def check_etag_header(self):
        return False

    def compute_etag(self):
        return None

    def format_exc(self, exc):
        return re.sub(r"File.*?site-packages.", "File \"", exc)

    def write_error(self, status_code, **kwargs):
        self.dump_request_summary("error")
        msg = {
            "status_code": status_code,
            "msg": "unknown error" if "msg" not in kwargs else self.format_exc(kwargs["msg"])
        }
        self.set_header("Content-Type", "text/plain")
        self.set_status(status_code)
        self.write(json.dumps(msg))
        self.finish()


class StaticFileHandler(BaseRequestHandler, tornado.web.StaticFileHandler):
    pass


class ErrorHandler(BaseRequestHandler):
    def check_xsrf_cookie(self):
        return


class NotFound(ErrorHandler):
    def prepare(self):
        self.write_error(404, msg="File Not Found")


class File(BaseRequestHandler):
    rh = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        import time
        self.ts = self.request.remote_ip+"/"+str(time.time())+"/"+self.request.path
        File.rh.append(self.ts)
        p = threading.Thread(target=self._monitor_count)
        p.daemon = True
        p.start()

    def _monitor_count(self):
        while True:
            if self._finished:
                File.rh.remove(self.ts)
                break
            import time
            # time.sleep(1/1000)
            time.sleep(1)
        self.dump_request_summary("success")


class HTML(File):
    file_name = None
    file_path = None
    file_modified = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.file_path = os.path.join(self.app_root, self.file_name+".html")
        self.file_modified = self.get_file_modified()

    def get_file_stat(self):
        return os.stat(self.file_path)

    def get_file_modified(self):
        return datetime.datetime.utcfromtimestamp(int(self.get_file_stat().st_mtime))

    def should_return_304(self) -> bool:
        ims_value = self.request.headers.get("If-Modified-Since")
        if ims_value is not None:
            date_tuple = email.utils.parsedate(ims_value)
            if date_tuple is not None:
                if_since = datetime.datetime(*date_tuple[:6])
                if if_since >= self.file_modified:
                    return True
        return False

    def set_modified_header(self):
        self.set_header("Last-Modified", self.file_modified)

    def set_304_header(self):
        self.set_status(304)
        self.finish()

    def get_what(self):
        return None

    def get(self, *args):
        self.set_modified_header()
        if self.should_return_304():
            return self.set_304_header()
        self.write(self.get_what() or open(self.file_path, "rb").read())
        self.finish()


class AJAX(File):
    api_name = None

    def _run(self, method: str):
        params = self.decrypted_params if self.decrypted_params else utils.parse_params(self.request.arguments.items())
        exec(open(os.path.join(self.app_root, self.api_name + "_api.py"), "rb").read().decode(), globals())
        return globals()["api_"+method](
            params,
            self.cookies_macros,
            app_root=self.app_root,
            db_port=self.db_port,
            writer_port=self.writer_port,
            x_real_ip=self.request.remote_ip if "X-Real-Ip" not in self.request_summary else self.request_summary["X-Real-Ip"]
        )

    def get(self, *args):
        self.write(self._run("get"))
        self.finish()

    def post(self, *args):
        raw_params = self._run("post")
        is_exc = isinstance(raw_params, Exception)
        is_traceback = False
        if not is_exc:
            is_traceback = "Traceback (most recent call last):" in raw_params
        if is_exc or is_traceback:
            if is_traceback:
                raw_params = json.loads(raw_params)
            if is_exc:
                raw_params = str(raw_params)
            return self.write_error(500, msg=raw_params)
        raw_params = raw_params.encode()
        if self.decrypted_params:
            raw_params = bytes([_ ^ self.api_key[math.floor(i%len(self.api_key))] for i, _ in enumerate(raw_params)])
            raw_params = b32encode(raw_params)
            self.write(raw_params.replace(b"=", b""))
        else:
            self.set_header("Content-Type", "application/json")
            self.write(raw_params)
        self.finish()


