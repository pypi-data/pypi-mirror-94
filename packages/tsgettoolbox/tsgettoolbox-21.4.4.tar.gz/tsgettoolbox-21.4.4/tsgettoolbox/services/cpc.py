"""
This module provides direct access to `Climate Predicition Center`_.

`Weekly Drought Index`_ dataset from `Climate Prediction Center`_.

.. _Climate Prediction Center: http://www.cpc.ncep.noaa.gov/
.. _Weekly Drought Index: http://www.cpc.ncep.noaa.gov/products/analysis_monitoring/cdus/palmer_drought/
"""
from __future__ import print_function
from __future__ import absolute_import

import pandas as pd

from tsgettoolbox.ulmo.cpc.drought.core import get_data

unit_conv = {
    "precipitation": "precipitation:in",
    "temperature": "temperature:degF",
    "potential_evap": "potential_evap:in",
    "runoff": "runoff:in",
    "soil_moisture_upper": "soil_moisture_upper:in",
    "soil_moisture_lower": "soil_moisture_lower:in",
}


def ulmo_df(state=None, climate_division=None, start_date=None, end_date=None):
    df = get_data(
        state=state,
        climate_division=climate_division,
        start=start_date,
        end=end_date,
        as_dataframe=True,
    )
    df = df.set_index("period")
    df.index = pd.PeriodIndex(df.index)
    df.index.name = "Datetime"
    df.columns = [unit_conv.get(i, i) for i in df.columns]
    return df


if __name__ == "__main__":
    r = ulmo_df(
        state="FL", climate_division=1, start_date="2017-01-01", end_date="2017-10-02"
    )

    print("FL EVERYTHING")
    print(r)
