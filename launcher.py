import asyncio
import contextlib
import logging

import click

from bot import TurnipBot


@contextlib.contextmanager
def setup_logging():
    try:
        logging.getLogger('discord').setLevel(logging.INFO)
        logging.getLogger('discord.http').setLevel(logging.WARNING)

        log = logging.getLogger()
        log.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='discord.log',
                                      encoding='utf-8',
                                      mode='w')
        formatter = logging.Formatter(
            "[{asctime}] [{levelname:<7}][{filename}:{lineno:<4}] {name}: {message}",
            datefmt="%Y-%m-%d %H:%M:%S",
            style="{")
        handler.setFormatter(formatter)
        log.addHandler(handler)

        yield
    finally:
        handlers = log.handlers[:]
        for h in handlers:
            h.close()
            log.removeHandler(h)


def run_bot():
    bot = TurnipBot()
    bot.run()


@click.group(invoke_without_command=True, options_metavar='[options]')
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        loop = asyncio.get_event_loop()
        with setup_logging():
            run_bot()


if __name__ == '__main__':
    main()
