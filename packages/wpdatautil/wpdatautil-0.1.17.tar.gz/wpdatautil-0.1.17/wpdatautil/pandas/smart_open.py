"""pandas smart_open utilities."""
import logging
from typing import Any

import pandas as pd
import smart_open

from wpdatautil.timeit import Timer

log = logging.getLogger(__name__)


def write_parquet(df: pd.DataFrame, uri: str, *, df_description: str = "dataframe", **kwargs: Any) -> None:
    """Write the given dataframe to the given URI using `smart_open`, thereby supporting both local and S3 URIs.

    `kwargs` are forwarded to `df.to_parquet`.
    """
    timer = Timer()
    write_description = f"{df_description} to {uri}"
    log.info(f"Writing {write_description}.")
    try:
        with smart_open.open(uri, "wb") as output_file:
            df.to_parquet(output_file, **kwargs)
    except Exception as exception:  # pylint: disable=broad-except
        log.error(f"Error writing {write_description}: {exception.__class__.__qualname__}: {exception}")
        raise
    log.info(f"Wrote {write_description} in {timer}.")
