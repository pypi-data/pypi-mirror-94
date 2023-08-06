import logging
import os

import pytest

from .authenticator import Authenticator
from .certs import generate_certs
from .config import Config
from .controller import AuthController

log = logging.getLogger(__name__)


class _Authenticator(Authenticator):
    def __init__(self, config=Config()):
        self.config = config

    def validate(self, username, password):
        if (
            username == self.config.SMTPD_LOGIN_NAME and
            password == self.config.SMTPD_LOGIN_PASSWORD
        ):
            log.debug((f"Validating username and password for {username} "
                       "succeeded"))
            return True

        log.debug(f"Validating username and password for {username} failed")
        return False

    def verify(self, address):
        """Method to verify that an address or username is correct.

        Possible inputs are:
        - a user name (e.g. "user")
        - an email address (e.g. "user@example.org")

        Should return a string in the form of "User <user@example.org>" if
        the address provided is valid. If there the valid is invalid return
        None. In this case we are returning a boolean true instead.
        """
        if (address == self.config.SMTPD_LOGIN_NAME):
            log.debug(f"Verified that username {address} is a valid user")
            return True

        log.debug(f"Verified that {address} is not a valid user")
        return None

    def get_password(self, username):
        log.debug(f"Password retrieved for {username}")
        return self.config.SMTPD_LOGIN_PASSWORD


class SMTPDFix():
    def __init__(self, hostname, port, config=None):
        self.hostname = hostname
        self.port = port
        self.config = config or Config()

    def __enter__(self):
        self.controller = AuthController(
            hostname=self.hostname,
            port=int(self.port),
            config=self.config,
            authenticator=_Authenticator(self.config)
        )
        log.debug("Enter called on SMTPDFix")
        self.controller.start()
        return self.controller

    def __exit__(self, type, value, traceback):
        log.debug("Exit called on SMTPDFix")
        self.controller.stop()


@pytest.fixture
def smtpd(tmp_path_factory):
    """A small SMTP server for use when testing applications that send email
    messages. To access the messages call `smtpd.messages` which returns a copy
    of the list of messages sent to the server.

    Example:
        def test_mail(smtpd):
            from smtplib import SMTP
            with SMTP(smtpd.hostname, smtpd.port) as client:
                code, resp = client.noop()
                assert code == 250
    """
    config = Config()

    if os.getenv("SMTPD_SSL_CERTS_PATH") is None:
        path = tmp_path_factory.mktemp("certs")
        generate_certs(path)
        os.environ["SMTPD_SSL_CERTS_PATH"] = str(path.resolve())

    # fixture = AuthController(
    #     hostname=config.SMTPD_HOST,
    #     port=int(config.SMTPD_PORT),
    #     config=config,
    #     authenticator=_Authenticator(config)
    # )
    # fixture.start()
    # yield fixture
    # fixture.stop()

    with SMTPDFix(config.SMTPD_HOST, config.SMTPD_PORT) as fixture:
        yield fixture
