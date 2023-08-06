import logging
import time

from aprsd import fuzzyclock, plugin, plugin_utils, trace, utils
from opencage.geocoder import OpenCageGeocode
import pytz

LOG = logging.getLogger("APRSD")


class TimePlugin(plugin.APRSDPluginBase):
    """Time command."""

    version = "1.0"
    command_regex = "^[tT]"
    command_name = "time"

    def _get_local_tz(self):
        return pytz.timezone(time.strftime("%Z"))

    def _get_utcnow(self):
        return pytz.datetime.datetime.utcnow()

    def build_date_str(self, localzone):
        utcnow = self._get_utcnow()
        gmt_t = pytz.utc.localize(utcnow)
        local_t = gmt_t.astimezone(localzone)

        local_short_str = local_t.strftime("%H:%M %Z")
        local_hour = local_t.strftime("%H")
        local_min = local_t.strftime("%M")
        cur_time = fuzzyclock.fuzzy(int(local_hour), int(local_min), 1)

        reply = "{} ({})".format(
            cur_time,
            local_short_str,
        )

        return reply

    @trace.trace
    def command(self, fromcall, message, ack):
        LOG.info("TIME COMMAND")
        # So we can mock this in unit tests
        localzone = self._get_local_tz()
        return self.build_date_str(localzone)


class TimeOpenCageDataPlugin(TimePlugin):
    """geocage based timezone fetching."""

    version = "1.0"
    command_regex = "^[tT]"
    command_name = "Time"

    @trace.trace
    def command(self, fromcall, message, ack):
        api_key = self.config["services"]["aprs.fi"]["apiKey"]
        try:
            aprs_data = plugin_utils.get_aprs_fi(api_key, fromcall)
        except Exception as ex:
            LOG.error("Failed to fetch aprs.fi data {}".format(ex))
            return "Failed to fetch location"

        # LOG.debug("LocationPlugin: aprs_data = {}".format(aprs_data))
        lat = aprs_data["entries"][0]["lat"]
        lon = aprs_data["entries"][0]["lng"]

        try:
            utils.check_config_option(self.config, "opencagedata", "apiKey")
        except Exception as ex:
            LOG.error("Failed to find config opencage:apiKey {}".format(ex))
            return "No opencage apiKey found"

        try:
            opencage_key = self.config["opencagedata"]["apiKey"]
            geocoder = OpenCageGeocode(opencage_key)
            results = geocoder.reverse_geocode(lat, lon)
        except Exception as ex:
            LOG.error("Couldn't fetch opencagedata api '{}'".format(ex))
            # Default to UTC instead
            localzone = pytz.timezone("UTC")
        else:
            tzone = results[0]["annotations"]["timezone"]["name"]
            localzone = pytz.timezone(tzone)

        return self.build_date_str(localzone)


class TimeOWMPlugin(TimePlugin):
    """OpenWeatherMap based timezone fetching."""

    version = "1.0"
    command_regex = "^[tT]"
    command_name = "Time"

    @trace.trace
    def command(self, fromcall, message, ack):
        api_key = self.config["services"]["aprs.fi"]["apiKey"]
        try:
            aprs_data = plugin_utils.get_aprs_fi(api_key, fromcall)
        except Exception as ex:
            LOG.error("Failed to fetch aprs.fi data {}".format(ex))
            return "Failed to fetch location"

        # LOG.debug("LocationPlugin: aprs_data = {}".format(aprs_data))
        lat = aprs_data["entries"][0]["lat"]
        lon = aprs_data["entries"][0]["lng"]

        try:
            utils.check_config_option(
                self.config,
                ["services", "openweathermap", "apiKey"],
            )
        except Exception as ex:
            LOG.error("Failed to find config openweathermap:apiKey {}".format(ex))
            return "No openweathermap apiKey found"

        api_key = self.config["services"]["openweathermap"]["apiKey"]
        try:
            results = plugin_utils.fetch_openweathermap(api_key, lat, lon)
        except Exception as ex:
            LOG.error("Couldn't fetch openweathermap api '{}'".format(ex))
            # default to UTC
            localzone = pytz.timezone("UTC")
        else:
            tzone = results["timezone"]
            localzone = pytz.timezone(tzone)

        return self.build_date_str(localzone)
