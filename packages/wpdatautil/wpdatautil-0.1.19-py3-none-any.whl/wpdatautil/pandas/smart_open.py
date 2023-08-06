"""pandas smart_open utilities."""
import logging
from typing import Any

import pandas as pd
import smart_open

from wpdatautil.timeit import Timer

log = logging.getLogger(__name__)


def read_parquet(uri: str, *, df_description: str = "dataframe", **kwargs: Any) -> pd.DataFrame:
    """Return a dataframe read from the given URI using `smart_open`, thereby supporting both local and S3 URIs.

    `kwargs` are forwarded to `pd.read_parquet`.
    """
    timer = Timer()
    read_description = f"{df_description} from {uri} using smart-open"
    log.info(f"Reading {read_description}.")
    try:
        with smart_open.open(uri, "rb") as input_file:
            df = pd.read_parquet(input_file, **kwargs)
    except Exception as exception:  # pylint: disable=broad-except
        log.info(f"Error reading {read_description}: {exception.__class__.__qualname__}: {exception}")
        raise
    log.info(f"Read {read_description} in {timer}.")
    return df


def write_parquet(df: pd.DataFrame, uri: str, *, df_description: str = "dataframe", **kwargs: Any) -> None:
    """Write the given dataframe to the given URI using `smart_open`, thereby supporting both local and S3 URIs.

    `kwargs` are forwarded to `df.to_parquet`.
    """
    timer = Timer()
    write_description = f"{df_description} to {uri} using smart-open"
    log.info(f"Writing {write_description}.")
    try:
        with smart_open.open(uri, "wb") as output_file:
            df.to_parquet(output_file, **kwargs)
    except Exception as exception:  # pylint: disable=broad-except
        log.info(f"Error writing {write_description}: {exception.__class__.__qualname__}: {exception}")
        raise
    log.info(f"Wrote {write_description} in {timer}.")
