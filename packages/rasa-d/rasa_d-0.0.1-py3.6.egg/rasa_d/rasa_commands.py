import socket
import logging
import datetime
import subprocess


logger = logging.getLogger("rasa-d.rasa")


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def launch_rasa(args):
    # Check that the port is available
    logger.info("Checking if rasa is already running...")
    if is_port_in_use(args.rasa_port):
        logger.error("Rasa port is already used. Please choose another port.")
        raise RuntimeError("Rasa port is already used. Please choose another port")

    logger.info("Starting rasa server...")
    popen_args = ["rasa", "run", f"--port", f"{args.rasa_port}"]
    if args.verbose:
        popen_args.append("--verbose")
    if args.debug:
        popen_args.append("--debug")
    proc = subprocess.Popen(popen_args, stdout=None, stderr=subprocess.STDOUT)

    start_time = datetime.datetime.now()
    while True:
        logger.debug("Checking if Rasa is ready...")
        if is_port_in_use(args.rasa_port):
            logger.debug("Rasa running...")
            break
        logger.debug("Rasa not ready yet...")
        now = datetime.datetime.now()
        if (start_time - now).total_seconds() > args.timeout:
            logger.error(f"Rasa timeout...")
            raise RuntimeError("Rasa timeout...")

    return proc


def launch_actions(args):
    # Check that the port is available
    logger.info("Checking if rasa is already running...")
    if is_port_in_use(args.rasa_port):
        logger.error("Rasa port is already used. Please choose another port.")
        raise RuntimeError("Rasa port is already used. Please choose another port")

    logger.info("Starting rasa actions server...")
    popen_args = ["rasa", "run", "actions", f"--port", f"{args.actions_port}"]
    if args.verbose:
        popen_args.append("--verbose")
    if args.debug:
        popen_args.append("--debug")
    if args.actions_package is not None:
        popen_args.append("--actions_package", args.action_package)
    if args.actions_auto_reload:
        popen_args.append("--actions_auto_reload")
    proc = subprocess.Popen(popen_args, stdout=None, stderr=subprocess.STDOUT)

    start_time = datetime.datetime.now()
    while True:
        logger.debug("Checking if Rasa actions server is ready...")
        if is_port_in_use(args.rasa_port):
            logger.debug("Rasa actions server running...")
            break
        logger.debug("Rasa actions server not ready yet...")
        now = datetime.datetime.now()
        if (start_time - now).total_seconds() > args.timeout:
            logger.error(f"Rasa actions server timeout...")
            raise RuntimeError("Rasa actions server timeout...")

    return proc