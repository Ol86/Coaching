"""Class to handle Garmin Connect operations."""

import json
from datetime import datetime, timedelta
from typing import Final

from loguru import logger

from coaching.garmin_connection import GarminConnection

__all___: list[str] = [
    "run",
]

OUTPUT_PATH = "./garmin_output"


def run():
    """Main function to run the coaching project."""

    today: Final = datetime.now()
    current_week: Final = int(today.strftime("%V"))
    monday_of_current_week: Final = (today - timedelta(days=today.weekday())).strftime("%Y-%m-%d")
    sunday_of_current_week: Final = (today + timedelta(days=6 - today.weekday())).strftime("%Y-%m-%d")
    file_name: Final = f"{OUTPUT_PATH}/Summary_KW{current_week}.json"

    # Connect to Garmin Connect.
    garmin_connection = GarminConnection()
    garmin = garmin_connection.get_garmin()
    logger.debug("Connected to Garmin Connect.")

    # Get sleep data for the current week.
    sleep_data = garmin.get_sleep_daily(
        start=monday_of_current_week,
        end=sunday_of_current_week,
    )
    if not sleep_data:
        logger.warning("No sleep data found for the current week.")
        sleep_data = []
    logger.debug(f"Sleep data for week {current_week}: {len(sleep_data)}")

    # Get HRV data for the current week.
    hrv_data = garmin.get_hrv_data_range(
        start=monday_of_current_week,
        end=sunday_of_current_week,
    )
    if not hrv_data:
        logger.warning("No HRV data found for the current week.")
        hrv_data = {"hrvSummaries": []}
    hrv_data = hrv_data["hrvSummaries"]
    logger.debug(f"HRV data for week {current_week}: {len(hrv_data)}")

    # Get activities for the current week.
    activities = garmin.get_activities_by_date(
        startdate=monday_of_current_week,
        enddate=sunday_of_current_week,
    )
    if not activities:
        logger.warning("No activities found for the current week.")
        activities = []
    logger.debug(f"Number of activities for week {current_week}: {len(activities)}")

    summary = {
        "current_week": current_week,
        "monday_of_current_week": monday_of_current_week,
        "sunday_of_current_week": sunday_of_current_week,
        "garmin_data": {
            "sleep_data": sleep_data,
            "hrv_data": hrv_data,
            "activities": activities,
        }
    }

    # Write the summary to a JSON file.
    with open(file_name, "w") as f:
        f.write(
            json.dumps(
                summary,
                indent=4,
            )
        )
    logger.debug(f"Summary for week {current_week} written to {file_name}.")
