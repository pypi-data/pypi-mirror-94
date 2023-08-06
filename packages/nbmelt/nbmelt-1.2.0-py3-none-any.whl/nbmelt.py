"""nbmelt: shutdown notebook servers that don't get used

nbmelt starts a timer when the notebook server starts.
If no authenticated request is made by that time, the server will exit.

That's it!

Usage: jupyter server extension enable nbmelt
"""

__version__ = "1.2.0"

import os

from tornado.ioloop import IOLoop


def _load_extension(app, AuthenticatedHandler):
    """Load the extension

    Wrapped below
    """
    timeout_env = os.environ.get('NBMELT_TIMEOUT')
    print("loading!", app, AuthenticatedHandler)
    if not timeout_env:
        app.log.info("nbmelt: $NBMELT_TIMEOUT not set, not enabling timeout")
        return
    timeout = int(timeout_env)
    app.log.info(
        "This notebook will self destruct if you don't use it in %s seconds!", timeout
    )
    state = {'called': False}
    save_method = AuthenticatedHandler.get_current_user

    # monkeypatch method so we notice when it gets called
    # all we want to know is if one authenticated request
    # was made in the time limit

    def stop_melting(*args, **kwargs):
        user = save_method(*args, **kwargs)
        if user:
            app.log.debug("Received authenticated request, halting nbmelt")
            state['called'] = True
            # only do this once:
            AuthenticatedHandler.get_current_user = save_method
        return user

    AuthenticatedHandler.get_current_user = stop_melting

    def shutdown_if_unused():
        if not state['called']:
            app.log.error(
                "No authenticated requests received in %ss, exiting.", timeout
            )
            IOLoop.current().stop()

    IOLoop.current().call_later(timeout, shutdown_if_unused)


def _load_jupyter_server_extension(app):
    """load for jupyter-server"""
    from jupyter_server.base.handlers import AuthenticatedHandler

    return _load_extension(app, AuthenticatedHandler)


def load_jupyter_server_extension(app):
    """load for notebook server"""
    from notebook.base.handlers import AuthenticatedHandler

    return _load_extension(app, AuthenticatedHandler)
