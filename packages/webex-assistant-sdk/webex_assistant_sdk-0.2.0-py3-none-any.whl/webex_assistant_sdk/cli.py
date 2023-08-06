import logging
import sys

import click
import click_log
from mindmeld import __version__ as mm_version
from mindmeld.cli import app_cli as mm_cli

from ._version import __version__

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


def _version_msg():
    """Returns the MindMeld version, location and Python powering it."""
    py_version = sys.version.split(' ')[0]
    message = f"Webex Assistant SDK {__version__}, MindMeld {mm_version}, Python {py_version}"
    return message


@click.group()
@click.version_option(__version__, "-V", "--version", message=_version_msg())
@click.pass_context
@click_log.simple_verbosity_option()
@click_log.init(__package__)
def _sdk_cli(ctx):
    """Command line interface for MindMeld apps."""

    # configure logger settings for dependent libraries
    urllib3_logger = logging.getLogger("urllib3")
    urllib3_logger.setLevel(logging.ERROR)
    es_logger = logging.getLogger("elasticsearch")
    es_logger.setLevel(logging.ERROR)
    warnings.filterwarnings(
        "module", category=DeprecationWarning, module="sklearn.preprocessing.label"
    )

    if ctx.obj is None:
        ctx.obj = {}


@_sdk_cli.command("invoke", context_settings=CONTEXT_SETTINGS)
@click.pass_context
@click.option("--context", help="JSON object to be used as the context")
@click.option("--public-key", help="Path to a file containing the public key to use for requests")
@click.option("--url", default="http://localhost:7150/parse", help="The URL where the agent can be accessed")
def invoke(ctx, context, public_key, url):
    """Starts a conversation with the app."""

    try:
        app = ctx.obj.get("app")
        if isinstance(context, str):
            context = json.loads(context)
        if app is None:
            raise ValueError("No app was given. Run 'python -m <app-name> converse'.")


        with open(public_key, 'r') as f:
            raw_public_key = f.read()

        convo = AssistantAgentConversation(
            url, secret=app.secret, raw_public_key=raw_public_key, context=context
        )

        if app.async_mode:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(_invoke_async(convo))
            return

        while True:
            message = click.prompt("You")
            responses = convo.say(message)
            _print_responses(responses)

    except MindMeldError as ex:
        logger.error(ex.message)
        ctx.exit(1)


def _print_response(responses):
    for index, response in enumerate(responses):
        prefix = "App: " if index == 0 else "...  "
        click.secho(prefix + response, fg="blue", bg="white")


async def _invoke_async(convo):
    while True:
        message = click.prompt("You")
        responses = await convo.say(message)
        _print_responses(responses)


@click.command(
    cls=click.CommandCollection,
    context_settings=CONTEXT_SETTINGS,
    sources=[_sdk_cli, mm_cli],
)
@click.version_option(__version__, "-V", "--version", message=_version_msg())
@click.pass_context
@click_log.simple_verbosity_option()
@click_log.init(__package__)
def app_cli(ctx):
    if ctx.obj is None:
        ctx.obj = {}
