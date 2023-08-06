import datetime
import logging
import re

from aprsd import messaging, plugin, trace

LOG = logging.getLogger("APRSD")


class QueryPlugin(plugin.APRSDPluginBase):
    """Query command."""

    version = "1.0"
    command_regex = r"^\!.*"
    command_name = "query"

    @trace.trace
    def command(self, fromcall, message, ack):
        LOG.info("Query COMMAND")

        tracker = messaging.MsgTrack()
        now = datetime.datetime.now()
        reply = "Pending messages ({}) {}".format(
            len(tracker),
            now.strftime("%H:%M:%S"),
        )

        searchstring = "^" + self.config["ham"]["callsign"] + ".*"
        # only I can do admin commands
        if re.search(searchstring, fromcall):

            # resend last N most recent:  "!3"
            r = re.search(r"^\!([0-9]).*", message)
            if r is not None:
                if len(tracker) > 0:
                    last_n = r.group(1)
                    reply = messaging.NULL_MESSAGE
                    LOG.debug(reply)
                    tracker.restart_delayed(count=int(last_n))
                else:
                    reply = "No pending msgs to resend"
                    LOG.debug(reply)
                return reply

            # resend all:   "!a"
            r = re.search(r"^\![aA].*", message)
            if r is not None:
                if len(tracker) > 0:
                    reply = messaging.NULL_MESSAGE
                    LOG.debug(reply)
                    tracker.restart_delayed()
                else:
                    reply = "No pending msgs"
                    LOG.debug(reply)
                return reply

            # delete all:   "!d"
            r = re.search(r"^\![dD].*", message)
            if r is not None:
                reply = "Deleted ALL pending msgs."
                LOG.debug(reply)
                tracker.flush()
                return reply

        return reply
