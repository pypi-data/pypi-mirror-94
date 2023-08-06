import logging
from sys import stdout
from os import environ

date_format = '%m/%d/%Y %I:%M:%S %p',


def config(
        disable_rich: bool = False,
        systemd: bool = None,
        system_vital: bool = False,
) -> None:
    """
    Configure logging to use a nice format.

    Args:
        disable_rich: Disable the 'rich' library activation.
            This will also disable color output.
            'rich' activation can also disable by the NO_COLOR or
            OMNIBLACK_NO_COLOR environment variables.

        systemd: Should the systemd format be used.
            By default we check if 'omniblack.systemd' is installed
            to make the decision to use the systemd format, as it is required
            to add the extra functionality.
            If enabled rich will be disabled

        system_vital: This program is consider vital to the operation of
            the overall system. This is used to decide sys log levels.
            This has no effect is systemd is not enabled.

    """
    if systemd is not False:
        try:
            # Check if systemd integration is enabled
            import omniblack.systemd # noqa F401
        except ImportError:
            systemd = False
        else:
            systemd = True

    handlers = None
    format = '%(levelname)s %(asctime)s: %(message)s'

    omniblack_no_color = 'OMNIBLACK_NO_COLOR' in environ

    rich_disabled = systemd or omniblack_no_color or disable_rich

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

        formatter.vital = system_vital

        for handler in handlers:
            handler.setFormatter(formatter)

    logging.basicConfig(
        format=format,
        datefmt=date_format,
        handlers=handlers,
    )
