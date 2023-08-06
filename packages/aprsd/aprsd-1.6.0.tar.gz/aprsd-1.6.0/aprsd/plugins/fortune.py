import logging
import shutil
import subprocess

from aprsd import plugin, trace

LOG = logging.getLogger("APRSD")


class FortunePlugin(plugin.APRSDPluginBase):
    """Fortune."""

    version = "1.0"
    command_regex = "^[fF]"
    command_name = "fortune"

    @trace.trace
    def command(self, fromcall, message, ack):
        LOG.info("FortunePlugin")
        reply = None

        fortune_path = shutil.which("fortune")
        if not fortune_path:
            reply = "Fortune command not installed"
            return reply

        try:
            cmnd = [fortune_path, "-s", "-n 60"]
            command = " ".join(cmnd)
            output = subprocess.check_output(
                command,
                shell=True,
                timeout=3,
                universal_newlines=True,
            )
            output = (
                output.replace("\r", "")
                .replace("\n", "")
                .replace("  ", "")
                .replace("\t", " ")
            )
        except subprocess.CalledProcessError as ex:
            reply = "Fortune command failed '{}'".format(ex.output)
        else:
            reply = output

        return reply
