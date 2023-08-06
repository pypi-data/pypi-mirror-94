from __future__ import print_function
from __future__ import absolute_import

import logging
import os
from builtins import object

from tsgettoolbox.odo import convert
from tsgettoolbox.odo import odo
from tsgettoolbox.odo import resource

import pandas as pd

import requests

from tsgettoolbox import utils

from tstoolbox import tsutils

# darksky.net


class darksky_net_json(object):
    def __init__(self, url, **query_params):
        self.url = url
        self.url_params = {}
        self.url_params["latitude"] = query_params.pop("latitude")
        self.url_params["longitude"] = query_params.pop("longitude")
        self.url_params["time"] = tsutils.parsedate(
            query_params.pop("time"), strftime="%Y-%m-%dT%H:%M:%S"
        )
        self.include_db = query_params.pop("database")
        all_dbs = ["currently", "minutely", "hourly", "daily", "alerts", "flags"]
        all_dbs.remove(self.include_db)
        query_params["exclude"] = ",".join(all_dbs)
        query_params["units"] = "si"
        self.query_params = query_params


@resource.register(r"https://api\.darksky\.net/forecast.*", priority=17)
def resource_darksky_net(uri, **kwargs):
    return darksky_net_json(uri, **kwargs)


# Function to convert from darksky_io_json type to pd.DataFrame


@convert.register(pd.DataFrame, darksky_net_json)
def darksky_net_json_to_df(data, **kwargs):
    # Read in API key
    api_key = utils.read_api_key("darksky.net")

    urlvar = "{0},{1}".format(data.url_params["latitude"], data.url_params["longitude"])

    req = requests.get("/".join([data.url, api_key, urlvar]), data.query_params)

    if os.path.exists("debug_tsgettoolbox"):
        logging.warning(req.url)
    req.raise_for_status()

    time_zone_name = req.json()["timezone"]
    try:
        ndfj = pd.read_json(req.content, orient="index")
    except ValueError:
        return pd.DataFrame()

    try:
        if isinstance(ndfj.loc[data.include_db, 0], dict):
            ndfj.loc[data.include_db, 0] = [ndfj.loc[data.include_db, 0]]
    except KeyError:
        return pd.DataFrame()

    ndfj = pd.DataFrame(ndfj.loc[data.include_db, :])
    ndfj = ndfj.transpose()

    ndfj.dropna(inplace=True, how="all")
    if data.include_db in ["minutely", "hourly", "daily"]:
        ndfj = pd.DataFrame(ndfj.loc[data.include_db, 0][0]["data"])
    elif data.include_db in ["alerts", "currently"]:
        ndfj = pd.DataFrame(ndfj.loc[data.include_db, 0])

    if data.include_db != "flags":
        ndfj.index = pd.to_datetime(ndfj["time"], unit="s")
        ndfj.drop("time", axis=1, inplace=True)
        ndfj.sort_index(inplace=True)
        ndfj = ndfj.tz_localize(time_zone_name)

    for datecols in [
        "apparentTemperatureMinTime",
        "apparentTemperatureMaxTime",
        "apparentTemperatureLowTime",
        "apparentTemperatureHighTime",
        "precipIntensityMaxTime",
        "sunriseTime",
        "sunsetTime",
        "temperatureMaxTime",
        "temperatureMinTime",
        "uvIndexTime",
        "windGustTime",
    ]:
        if datecols in ndfj.columns:
            ndfj[datecols] = pd.to_datetime(ndfj[datecols], unit="s")

    ndfj.index.name = "Datetime:{0}".format(time_zone_name)
    unitsd = {
        "nearestStormDistance": ":km",
        "precipIntensity": ":mm/h",
        "precipIntensityMax": ":mm/h",
        "precipAccumulation": ":cm",
        "temperature": ":degC",
        "temperatureMin": ":degC",
        "temperatureMax": ":degC",
        "apparentTemperature": ":degC",
        "apparentTemperatureLow": ":degC",
        "apparentTemperatureHigh": ":degC",
        "apparentTemperatureMin": ":degC",
        "apparentTemperatureMax": ":degC",
        "dewPoint": ":degC",
        "windSpeed": ":m/s",
        "windGust": ":m/s",
        "pressure": ":hPa",
        "visibility": ":km",
        "ozone": "DU",
    }
    ndfj.columns = ["{0}{1}".format(i, unitsd.setdefault(i, "")) for i in ndfj.columns]
    return ndfj


if __name__ == "__main__":
    r = resource(
        r"https://api.darksky.net/forecast",
        latitude=28.45,
        longitude=-81.34,
        database="currently",
        time="2020-01-01T01:00:00",
    )

    as_df = odo(r, pd.DataFrame)
    print("darksky.net currently")
    print(as_df.head())

    r = resource(
        r"https://api.darksky.net/forecast",
        latitude=28.45,
        longitude=-81.34,
        database="minutely",
        time=None,
    )

    as_df = odo(r, pd.DataFrame)
    print("darksky.net minutely")
    print(as_df.head())

    r = resource(
        r"https://api.darksky.net/forecast",
        latitude=28.45,
        longitude=-81.34,
        database="hourly",
        time=None,
    )

    as_df = odo(r, pd.DataFrame)
    print("darksky.net hourly")
    print(as_df.head())

    r = resource(
        r"https://api.darksky.net/forecast",
        latitude=28.45,
        longitude=-81.34,
        database="daily",
        time=None,
    )

    as_df = odo(r, pd.DataFrame)
    print("darksky.net daily")
    print(as_df.head())

    r = resource(
        r"https://api.darksky.net/forecast",
        latitude=28.45,
        longitude=-81.34,
        database="alerts",
        time=None,
    )

    as_df = odo(r, pd.DataFrame)
    print("darksky.net alerts")
    print(as_df.head())

    r = resource(
        r"https://api.darksky.net/forecast",
        latitude=28.45,
        longitude=-81.34,
        database="flags",
        time=None,
    )

    as_df = odo(r, pd.DataFrame)
    print("darksky.net flags")
    print(as_df.head())

    r = resource(
        r"https://api.darksky.net/forecast",
        latitude=28.45,
        longitude=-81.34,
        database="currently",
        time="yesterday",
    )

    as_df = odo(r, pd.DataFrame)
    print("darksky.net flags")
    print(as_df.head())
