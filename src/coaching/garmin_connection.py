"""The Garmin connection module."""

import os
from getpass import getpass

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)
from loguru import logger

__all___: list[str] = [
    "GarminConnection",
]


class GarminConnection:
    """A class to handle the connection to Garmin Connect."""
    TOKENSTORE = "./.garminconnect"
    garmin: Garmin

    def __init__(self):
        self.garmin = self.connect_to_garmin()

    def connect_to_garmin(self) -> Garmin:
        """Connect to Garmin Connect and return the Garmin object."""
        logger.debug("Connecting to Garmin Connect.")

        if os.path.exists(self.TOKENSTORE):
            self.login_with_token()
        else:
            self.login_with_credentials()

        # Skip the mobile strategies to avoid issues with the Garmin Connect API.
        self.garmin.client.skip_strategies.update({
            "mobile+cffi",
            "mobile+requests",
        })

        # Log in to Garmin Connect.
        self.login()
        return self.garmin

    def login_with_credentials(self) -> None:
        """Connect to Garmin Connect using username and password."""
        logger.debug("Token store not found. Logging in to Garmin Connect.")
        username = input("Enter your Garmin Connect username: ")
        password = getpass("Enter your Garmin Connect password: ")
        self.garmin = Garmin(username, password)

    def login_with_token(self) -> None:
        """Connect to Garmin Connect using a stored token."""
        logger.debug("Logging in to Garmin Connect with token.")
        self.garmin = Garmin()

    def login(self) -> None:
        """Login to Garmin Connect."""
        try:
            # Log in to Garmin Connect.
            self.garmin.login(tokenstore=f"{self.TOKENSTORE}")
            logger.debug("Successfully logged in to Garmin Connect.")
        except GarminConnectTooManyRequestsError as e:
            logger.error(f"Too many requests to Garmin Connect: {e}")
            raise
        except (GarminConnectConnectionError, GarminConnectAuthenticationError) as e:
            logger.warning(f"Failed to connect to Garmin Connect: {e}")
            self.login_with_credentials()
            self.login()

    def get_garmin(self) -> Garmin:
        """Return the Garmin object."""
        return self.garmin
