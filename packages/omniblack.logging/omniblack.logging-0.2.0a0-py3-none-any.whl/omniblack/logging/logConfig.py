import logging
from sys import stdout
from os import environ

date_format = '%m/%d/%Y %I:%M:%S %p',


def config(disable_rich=False, systemd=None):
    """
    Configure logging to use a nice format.

    Args:
        disable_rich: Disable the 'rich' library activation.
            This will also disable color output.
            'rich' activation can also disable by the NO_COLOR or
            NO_RICH environment variables.

        systemd: Should the systemd format be used.
            If this is set to 'None' then we will check if
            'omniblack.systemd' is install to make the decision
            to use the systemd format.
            If True rich will be disabled.

    """
    if systemd is None:
        try:
            # Check if systemd integration is enabled
            import omniblack.systemd # noqa F401
        except ImportError:
            systemd = False
        else:
            systemd = True
    handlers = None
    format = '%(levelname)s %(asctime)s: %(message)s'
    rich_disabled = systemd or 'NO_RICH' in environ or disable_rich
    if 'NO_COLOR' not in environ and not rich_disabled:
        try:
            from rich.logging import RichHandler
            from rich.traceback import install
            install()
            # We change the format string when rich is enabled, because
            # it will auto color the level when for us
            format = '%(asctime)s: %(message)s'
            handlers = (
                RichHandler(
                    rich_tracebacks=True,
                    show_time=False,
                ),
            )
        except ImportError:
            # Rich is optional
            pass

    if handlers is None:
        handlers = (logging.StreamHandler(stream=stdout), )

    if systemd:
        from omniblack.systemd.formatter import SystemdFormatter
        format = '%(syslog_priority)s %(message)s [%(name)s]'
        formatter = SystemdFormatter(
            fmt=format,
            datefmt=date_format,
        )

        for handler in handlers:
            handler.setFormatter(formatter)

    logging.basicConfig(
        format=format,
        datefmt=date_format,
        handlers=handlers,
    )
