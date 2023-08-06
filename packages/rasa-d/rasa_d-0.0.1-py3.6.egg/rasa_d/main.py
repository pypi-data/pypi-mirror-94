import asyncio
import argparse
import logging
import namegenerator


from .rasa_commands import launch_actions, launch_rasa
from .tunnel_commands import open_tunnel


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("rasa-d")


def main():
    parser = argparse.ArgumentParser(description="Rasa-d connects your Rasa model to the world.")
    rasa_d = parser.add_argument_group("Rasa-d Arguments")
    rasa_d.add_argument("--host", type=str, help="host of the remote server", default="rasa-d.com")
    rasa_d.add_argument("--timeout", type=int, help="wait for X seconds for Rasa to start", default=60)
    rasa_d.add_argument("-s", "--subdomain", type=str, help="sub-domain where the rasa will be accessible")
    rasa_d.add_argument("-d", "--debug", action="store_true")
    rasa_d.add_argument("-v", "--verbose", action="store_true")
    rasa = parser.add_argument_group("Rasa Arguments")
    rasa.add_argument("--rasa_port", type=int, default=5005, help="local port on which the rasa server will be listening.")
    actions = parser.add_argument_group("Actions Arguments")
    actions.add_argument("--actions", action="store_true", help="run the action server")
    actions.add_argument("--actions_port", type=int, default=5055)
    actions.add_argument("--actions_package", help="name of action package to be loaded")
    actions.add_argument("--actions_auto_reload", action="store_true", help="enable auto-reloading of modules containing Action subclasses.")
    args = parser.parse_args()
    assert args.actions_port != args.rasa_port

    # Launch Rasa
    rasa = launch_rasa(args)

    # Launch Actions (if necessary)
    actions = launch_actions(args) if args.actions else None

    # Launch the socket
    if args.subdomain is None:
        args.subdomain = namegenerator.gen()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            open_tunnel(
                ws_uri=f'wss://{args.host}/_ws/?username={args.subdomain}&port={args.rasa_port}',
                http_uri=f'http://127.0.0.1:{args.rasa_port}',
            )
        )
    except KeyboardInterrupt:
        print("\njprq tunnel closed")

if __name__ == "__main__":
    main()
