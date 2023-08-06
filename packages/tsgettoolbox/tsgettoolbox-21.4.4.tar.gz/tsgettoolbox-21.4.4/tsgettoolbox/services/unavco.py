from __future__ import print_function
from __future__ import absolute_import

import logging
import os
from builtins import object
from io import BytesIO

from tsgettoolbox.odo import convert
from tsgettoolbox.odo import odo
from tsgettoolbox.odo import resource

import pandas as pd

import requests

from tstoolbox import tsutils

# unavco

# pd.read_csv('http://web-services.unavco.org:80/met/data/P0005/beta?starttime=2012-05-01T00%3A00%3A00&endtime=2012-05-02T23%3A59&tsFormat=iso8601'


class Unavco(object):
    def __init__(self, url, **query_params):
        try:
            station = query_params.pop("station")
        except KeyError:
            raise KeyError(
                """
*
*   The station keyword is required.  You have given me
*   {0}.
*
""".format(
                    query_params
                )
            )
        self.url = "{0}/{1}/beta".format(url, station)
        if "/met/" in self.url or "/strain/" in self.url:
            self.comment = None
        else:
            self.comment = "#"
        query_params["starttime"] = tsutils.parsedate(
            query_params["starttime"]
        ).isoformat()
        query_params["endtime"] = tsutils.parsedate(query_params["endtime"]).isoformat()
        self.query_params = query_params
        self.query_params["tsFormat"] = "iso8601"


# Function to make `resource` know about the new unavco type.


@resource.register(r"http://web-services.unavco.org:80/met/data.*", priority=17)
@resource.register(
    r"http://web-services.unavco.org:80/pore/data/temperature.*", priority=17
)
@resource.register(
    r"http://web-services.unavco.org:80/pore/data/pressure.*", priority=17
)
@resource.register(r"http://web-services.unavco.org:80/tilt/data.*", priority=17)
@resource.register(r"http://web-services.unavco.org:80/strain/data/L2.*", priority=17)
def resource_unavco(uri, **kwargs):
    return Unavco(uri, **kwargs)


# Function to convert from Unavco type to pd.DataFrame


@convert.register(pd.DataFrame, Unavco)
def unavco_to_df(data, **kwargs):
    req = requests.get(data.url, params=data.query_params)
    if os.path.exists("debug_tsgettoolbox"):
        logging.warning(req.url)
    df = pd.read_csv(
        BytesIO(req.content),
        header=0,
        index_col=0,
        parse_dates=[0],
        comment=data.comment,
        skiprows=5,
    )
    df.columns = [
        "unavco-{0}".format(
            i.strip()
            .replace(" ", "_")
            .replace("(", ":")
            .replace(")", "")
            .replace("deg._C", "degC")
        )
        for i in df.columns
    ]
    df.index.name = "Datetime:UTC"
    return df


if __name__ == "__main__":
    r = resource(
        r"http://web-services.unavco.org:80/met/data",
        station="P005",
        starttime="2012-05-01T00:00:00",
        endtime="2012-05-02T23:59:59",
    )

    as_df = odo(r, pd.DataFrame)
    print("Unavco_met")
    print(as_df)

    r = resource(
        r"http://web-services.unavco.org:80/pore/data/temperature",
        station="B078",
        starttime="2012-05-02T00:00:00",
        endtime="2012-05-02T23:59:59",
    )

    as_df = odo(r, pd.DataFrame)
    print("Unavco_pore_temperature")
    print(as_df)

    r = resource(
        r"http://web-services.unavco.org:80/pore/data/pressure",
        station="B078",
        starttime="2012-05-02T00:00:00",
        endtime="2012-05-02T23:59:59",
    )

    as_df = odo(r, pd.DataFrame)
    print("Unavco_pore_pressure")
    print(as_df)

    r = resource(
        r"http://web-services.unavco.org:80/tilt/data",
        station="P693",
        starttime="2012-05-01T00:00:00",
        endtime="2012-05-01T01:00:00",
    )

    as_df = odo(r, pd.DataFrame)
    print("Unavco_tilt")
    print(as_df)

    r = resource(
        r"http://web-services.unavco.org:80/strain/data/L2",
        station="B007",
        starttime="2012-05-01T00:00:00",
        endtime="2012-05-01T23:59:59",
    )

    as_df = odo(r, pd.DataFrame)
    print("Unavco_strain")
    print(as_df)
