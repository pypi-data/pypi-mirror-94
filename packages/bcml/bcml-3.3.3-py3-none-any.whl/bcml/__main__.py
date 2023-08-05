import os
import sys
from contextlib import redirect_stderr, redirect_stdout
from multiprocessing import set_start_method, Process
from os import chmod  # pylint: disable=ungrouped-imports
from pathlib import Path
from subprocess import Popen, DEVNULL
from shutil import rmtree
from threading import Thread
from time import sleep

import webviewb as webview

from bcml import DEBUG, util, _oneclick
from bcml.util import Messager, LOG, SYSTEM
from bcml._api import Api
from bcml._server import start_server

logger = None  # pylint: disable=invalid-name


def stop_it(messager: Messager = None):
    if messager:
        messager.save()
    try:
        del globals()["logger"]
    except KeyError:
        pass
    if SYSTEM == "Windows":
        Popen(
            "taskkill /F /IM subprocess.exe /T".split(),
            stdout=DEVNULL,
            stderr=DEVNULL,
            creationflags=0x08000000,
        )
        rmtree(Path() / "blob_storage", ignore_errors=True)
        rmtree(Path() / "webrtc_event_logs", ignore_errors=True)
        return
    else:
        os.killpg(0, 9)


def configure_cef(debug):
    from webviewb.platforms.cef import (  # pylint: disable=import-outside-toplevel
        settings,
    )

    cache = util.get_storage_dir() / "cef_cache"
    settings.update(
        {"cache_path": str(cache), "context_menu": {"enabled": debug, "devtools": True}}
    )
    if not cache.exists():
        cache.mkdir(parents=True, exist_ok=True)


def main(debug: bool = False):
    set_start_method("spawn", True)
    global logger  # pylint: disable=invalid-name,global-statement
    logger = None

    try:
        if SYSTEM != "Windows":
            chmod(util.get_exec_dir() / "helpers/msyt", int("755", 8))
            chmod(util.get_exec_dir() / "helpers/7z", int("755", 8))
            os.setpgrp()
        LOG.parent.mkdir(parents=True, exist_ok=True)
        for folder in util.get_work_dir().glob("*"):
            rmtree(folder)
        (util.get_data_dir() / "tmp_settings.json").unlink()
    except (FileNotFoundError, OSError, PermissionError):
        pass

    _oneclick.register_handlers()
    oneclick = Thread(target=_oneclick.listen)
    oneclick.daemon = True
    oneclick.start()

    server_port = util.get_open_port()
    server = Process(target=start_server, args=(server_port,))
    server.daemon = True
    server.start()
    host = f"http://localhost:{server_port}"

    api = Api(host)

    gui = "cef" if SYSTEM == "Windows" else "qt"

    if not debug:
        debug = DEBUG or "bcml-debug" in sys.argv

    if SYSTEM == "Windows":
        configure_cef(debug)

    if (util.get_data_dir() / "settings.json").exists():
        url = f"{host}/index.html"
        width, height = 907, 680
    else:
        url = f"{host}/index.html?firstrun=yes"
        width, height = 750, 600

    api.window = webview.create_window(
        "BOTW Cross-Platform Mod Loader",
        url=url,
        js_api=api,
        text_select=DEBUG,
        width=width,
        height=height,
        min_size=(width if width == 750 else 820, 600),
    )
    logger = Messager(api.window)
    api.window.closing += stop_it

    messager = Messager(api.window)
    with redirect_stderr(sys.stdout):
        with redirect_stdout(messager):  # type: ignore
            sleep(0.5)
            webview.start(
                gui=gui, debug=debug, http_server=True, func=_oneclick.process_arg
            )
    api.cleanup()
    stop_it(messager=messager)


def main_debug():
    main(True)


if __name__ == "__main__":
    main()
