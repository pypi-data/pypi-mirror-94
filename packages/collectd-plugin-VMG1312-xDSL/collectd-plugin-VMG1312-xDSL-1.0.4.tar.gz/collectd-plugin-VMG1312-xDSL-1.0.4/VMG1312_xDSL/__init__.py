try:
    # This is only availabe "inside" collectd
    import collectd
except ImportError:
    # Outside collectd we need to mock this class, since the linter will complain etc.
    import collectd_mock as collectd

import requests
import sys, time, os
from bs4 import BeautifulSoup
import re
import datetime

PLUGIN_NAME = 'VMG1312_xDSL'

loginpath = "/login/login-page.cgi"
dslpath = "/pages/systemMonitoring/xdslStatistics/xdslStatistics.html"
params = {}


class XdslInfo:
    raw: str

    vdsl_trainingstatus: str
    vdsl_mode: str
    vdsl_profile: str
    vdsl_gvector: bool
    vdsl_traffictype: str
    vdsl_linkuptime_str: str
    vdsl_linkuptime_timedelta: datetime.timedelta

    vdsl_upstream_linerateMbps: float
    vdsl_upstream_netdatarateMbps: float
    vdsl_upstream_trelliscoding: bool
    vdsl_upstream_snrmarginDB: float
    vdsl_upstream_actualdelayMS: float
    vdsl_upstream_transmitPowerDBm: float
    vdsl_upstream_receivePowerDBm: float
    vdsl_upstream_actualInpSymbols: float
    vdsl_upstream_totalAttenuationDB: float
    vdsl_upstream_attainableNetDataRateMbps: float

    vdsl_downstream_linerateMbps: float
    vdsl_downstream_netdatarateMbps: float
    vdsl_downstream_trelliscoding: bool
    vdsl_downstream_snrmarginDB: float
    vdsl_downstream_actualdelayMS: float
    vdsl_downstream_transmitPowerDBm: float
    vdsl_downstream_receivePowerDBm: float
    vdsl_downstream_actualInpSymbols: float
    vdsl_downstream_totalAttenuationDB: float
    vdsl_downstream_attainableNetDataRateMbps: float

    vdsl_band_lineattenuationDB_U0: float = None
    vdsl_band_signalattenuationDB_U0: float = None
    vdsl_band_snrMargin_U0: float = None
    vdsl_band_txPower_U0: float = None

    vdsl_band_lineattenuationDB_U1: float = None
    vdsl_band_signalattenuationDB_U1: float = None
    vdsl_band_snrMargin_U1: float = None
    vdsl_band_txPower_U1: float = None

    vdsl_band_lineattenuationDB_U2: float = None
    vdsl_band_signalattenuationDB_U2: float = None
    vdsl_band_snrMargin_U2: float = None
    vdsl_band_txPower_U2: float = None

    vdsl_band_lineattenuationDB_U3: float = None
    vdsl_band_signalattenuationDB_U3: float = None
    vdsl_band_snrMargin_U3: float = None
    vdsl_band_txPower_U3: float = None

    vdsl_band_lineattenuationDB_U4: float = None
    vdsl_band_signalattenuationDB_U4: float = None
    vdsl_band_snrMargin_U4: float = None
    vdsl_band_txPower_U4: float = None

    vdsl_band_lineattenuationDB_D1: float = None
    vdsl_band_signalattenuationDB_D1: float = None
    vdsl_band_snrMargin_D1: float = None
    vdsl_band_txPower_D1: float = None

    vdsl_band_lineattenuationDB_D2: float = None
    vdsl_band_signalattenuationDB_D2: float = None
    vdsl_band_snrMargin_D2: float = None
    vdsl_band_txPower_D2: float = None

    vdsl_band_lineattenuationDB_D3: float = None
    vdsl_band_signalattenuationDB_D3: float = None
    vdsl_band_snrMargin_D3: float = None
    vdsl_band_txPower_D3: float = None

    def xstr(self, s):
        if s is None:
            return 'N/A '
        else:
            return str(s)

    def __str__(self):
        out = "VDSL Training Status:       " + self.vdsl_trainingstatus
        out += "\nVDSL Mode:                  " + self.vdsl_mode
        out += "\nTraffic Type:               " + self.vdsl_traffictype
        if self.vdsl_trainingstatus == "Showtime":
            out += "\nVDSL Profile:               " + self.vdsl_profile
            out += "\nG.Vector:                   " + str(self.vdsl_gvector)
            out += "\nLink Uptime:                " + str(self.vdsl_linkuptime_timedelta) + " (" + str(
                self.vdsl_linkuptime_timedelta.total_seconds()) + "s)"
        out += "\n========================================================="
        out += "\nVDSL Port Details           Upstream         Downstream"
        out += "\nLine Rate:                  " + str(self.vdsl_upstream_linerateMbps) \
               + " Mbps      " + str(self.vdsl_downstream_linerateMbps) + " Mbps"
        out += "\nActual Net Data Rate:       " + str(self.vdsl_upstream_netdatarateMbps) \
               + " Mbps      " + str(self.vdsl_downstream_netdatarateMbps) + " Mbps"
        out += "\nTrellis Coding:             " + str(self.vdsl_upstream_trelliscoding) \
               + "             " + str(self.vdsl_downstream_trelliscoding)
        out += "\nSNR Margin:                 " + str(self.vdsl_upstream_snrmarginDB) \
               + " dB           " + str(self.vdsl_downstream_snrmarginDB) + " dB"
        out += "\nActual Delay:               " + str(self.vdsl_upstream_actualdelayMS) \
               + " ms           " + str(self.vdsl_downstream_actualdelayMS) + " ms"
        out += "\nTransmit Power:             " + str(self.vdsl_upstream_transmitPowerDBm) \
               + " dBm          " + str(self.vdsl_downstream_transmitPowerDBm) + " dBm"
        out += "\nReceive Power:              " + str(self.vdsl_upstream_receivePowerDBm) \
               + " dBm         " + str(self.vdsl_downstream_receivePowerDBm) + " dBm"
        out += "\nActual INP:                 " + str(self.vdsl_upstream_actualInpSymbols) \
               + " symbols     " + str(self.vdsl_downstream_actualInpSymbols) + " symbols"
        out += "\nTotal Attenuation:          " + str(self.vdsl_upstream_totalAttenuationDB) \
               + " dB           " + str(self.vdsl_downstream_totalAttenuationDB) + " dB"
        out += "\nAttainable Net Data Rate:   " + str(self.vdsl_upstream_attainableNetDataRateMbps) \
               + " Mbps      " + str(self.vdsl_downstream_attainableNetDataRateMbps) + " Mbps"
        if self.vdsl_trainingstatus == "Showtime":
            out += "\n========================================================="
            out += "\nVDSL Band Status        U0      U1      U2      U3      U4      D1      D2      D3"
            out += "\nLine Attenuation(dB):   " + self.xstr(self.vdsl_band_lineattenuationDB_U0) + "     " \
                   + self.xstr(self.vdsl_band_lineattenuationDB_U1) + "    " \
                   + self.xstr(self.vdsl_band_lineattenuationDB_U2) + "    " \
                   + self.xstr(self.vdsl_band_lineattenuationDB_U3) + "    " \
                   + self.xstr(self.vdsl_band_lineattenuationDB_U4) + "    " \
                   + self.xstr(self.vdsl_band_lineattenuationDB_D1) + "    " \
                   + self.xstr(self.vdsl_band_lineattenuationDB_D2) + "    " \
                   + self.xstr(self.vdsl_band_lineattenuationDB_D3) + "    "
            out += "\nSignal Attenuation(dB): " + self.xstr(self.vdsl_band_signalattenuationDB_U0) + "     " \
                   + self.xstr(self.vdsl_band_signalattenuationDB_U1) + "    " \
                   + self.xstr(self.vdsl_band_signalattenuationDB_U2) + "    " \
                   + self.xstr(self.vdsl_band_signalattenuationDB_U3) + "    " \
                   + self.xstr(self.vdsl_band_signalattenuationDB_U4) + "    " \
                   + self.xstr(self.vdsl_band_signalattenuationDB_D1) + "    " \
                   + self.xstr(self.vdsl_band_signalattenuationDB_D2) + "    " \
                   + self.xstr(self.vdsl_band_signalattenuationDB_D3) + "    "
            out += "\nSNR Margin(dB):         " + self.xstr(self.vdsl_band_snrMargin_U0) + "     " \
                   + self.xstr(self.vdsl_band_snrMargin_U1) + "      " \
                   + self.xstr(self.vdsl_band_snrMargin_U2) + "     " \
                   + self.xstr(self.vdsl_band_snrMargin_U3) + "     " \
                   + self.xstr(self.vdsl_band_snrMargin_U4) + "    " \
                   + self.xstr(self.vdsl_band_snrMargin_D1) + "    " \
                   + self.xstr(self.vdsl_band_snrMargin_D2) + "    " \
                   + self.xstr(self.vdsl_band_snrMargin_D3) + "    "
            out += "\nTX Power(dBm):         " + self.xstr(self.vdsl_band_txPower_U0) + "     " \
                   + self.xstr(self.vdsl_band_txPower_U1) + "    " \
                   + self.xstr(self.vdsl_band_txPower_U2) + "    " \
                   + self.xstr(self.vdsl_band_txPower_U3) + "    " \
                   + self.xstr(self.vdsl_band_txPower_U4) + "    " \
                   + self.xstr(self.vdsl_band_txPower_D1) + "    " \
                   + self.xstr(self.vdsl_band_txPower_D2) + "    " \
                   + self.xstr(self.vdsl_band_txPower_D3) + "    "
        return out

    def parse(self, input_str: str):
        self.raw = input_str

        # https://regex101.com/r/ar6kj3/1
        self.vdsl_trainingstatus = re.search(r".DSL Training Status: (.*)\n", input_str).group(1).strip()
        self.vdsl_mode = re.search(r"Mode: (.*)\n", input_str).group(1).strip()
        if self.vdsl_trainingstatus == "Showtime":
            self.vdsl_profile = re.search(r"VDSL Profile: (.*)\n", input_str).group(1).strip()
            gvector = re.search(r"G.Vector: (.*)\n", input_str).group(1).strip()
            if gvector == "Enable":
                self.vdsl_gvector = True
            else:
                self.vdsl_gvector = False
        else:
            self.vdsl_profile = None
        self.vdsl_traffictype = re.search(r"Traffic Type: (.*)\n", input_str).group(1).strip()
        self.vdsl_linkuptime_str = re.search(r"Link Uptime: (.*)\n", input_str).group(1).strip()
        td = re.search(r"Link Uptime: (.*) day.*: (.*) hour.*: (.*) minute.*\n", input_str)
        if td is not None:
            self.vdsl_linkuptime_timedelta = datetime.timedelta(
                days=int(td.group(1).strip()),
                hours=int(td.group(2).strip()),
                minutes=int(td.group(3).strip())
            )
        self.vdsl_upstream_linerateMbps = float(re.search(r"Line Rate: (.*) Mbps (.*) Mbps\n", input_str).group(1))
        self.vdsl_downstream_linerateMbps = float(re.search(r"Line Rate: (.*) Mbps (.*) Mbps\n", input_str).group(2))
        self.vdsl_upstream_netdatarateMbps = float(
            re.search(r"Actual Net Data Rate: (.*) Mbps (.*) Mbps\n", input_str).group(1))
        self.vdsl_downstream_netdatarateMbps = float(
            re.search(r"Actual Net Data Rate: (.*) Mbps (.*) Mbps\n", input_str).group(2))
        trellis = re.search(r"Trellis Coding:.*(\S{2}).*(\S{2})\n", input_str)
        if trellis.group(1) == "ON":
            self.vdsl_upstream_trelliscoding = True
        else:
            self.vdsl_upstream_trelliscoding = False
        if trellis.group(2) == "ON":
            self.vdsl_downstream_trelliscoding = True
        else:
            self.vdsl_downstream_trelliscoding = False
        self.vdsl_upstream_snrmarginDB = float(re.search(r"SNR Margin: (.*) dB (.*) dB\n", input_str).group(1))
        self.vdsl_downstream_snrmarginDB = float(re.search(r"SNR Margin: (.*) dB (.*) dB\n", input_str).group(2))
        self.vdsl_upstream_actualdelayMS = float(re.search(r"Actual Delay: (.*) ms (.*) ms\n", input_str).group(1))
        self.vdsl_downstream_actualdelayMS = float(re.search(r"Actual Delay: (.*) ms (.*) ms\n", input_str).group(2))
        self.vdsl_upstream_transmitPowerDBm = float(
            re.search(r"Transmit Power: (.*) dBm (.*) dBm\n", input_str).group(1))
        self.vdsl_downstream_transmitPowerDBm = float(
            re.search(r"Transmit Power: (.*) dBm (.*) dBm\n", input_str).group(2))
        self.vdsl_upstream_receivePowerDBm = float(re.search(r"Receive Power: (.*) dBm (.*) dBm\n", input_str).group(1))
        self.vdsl_downstream_receivePowerDBm = float(
            re.search(r"Receive Power: (.*) dBm (.*) dBm\n", input_str).group(2))
        self.vdsl_upstream_actualInpSymbols = float(
            re.search(r"Actual INP: (.*) symbols (.*) symbols\n", input_str).group(1))
        self.vdsl_downstream_actualInpSymbols = float(
            re.search(r"Actual INP: (.*) symbols (.*) symbols\n", input_str).group(2))
        self.vdsl_upstream_totalAttenuationDB = float(
            re.search(r"Total Attenuation: (.*) dB (.*) dB\n", input_str).group(1))
        self.vdsl_downstream_totalAttenuationDB = float(
            re.search(r"Total Attenuation: (.*) dB (.*) dB\n", input_str).group(2))
        self.vdsl_upstream_attainableNetDataRateMbps = float(
            re.search(r"Attainable Net Data Rate: (.*) Mbps (.*) Mbps\n", input_str).group(1))
        self.vdsl_downstream_attainableNetDataRateMbps = float(
            re.search(r"Attainable Net Data Rate: (.*) Mbps (.*) Mbps\n", input_str).group(2))

        if self.vdsl_trainingstatus == "Showtime":
            lineAttenuation = re.search(r"Line Attenuation\(dB\):\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t\n",
                                        input_str)
            if lineAttenuation.group(1).strip() != "N/A":
                self.vdsl_band_lineattenuationDB_U0 = float(lineAttenuation.group(1).strip())
            if lineAttenuation.group(2).strip() != "N/A":
                self.vdsl_band_lineattenuationDB_U1 = float(lineAttenuation.group(2).strip())
            if lineAttenuation.group(3).strip() != "N/A":
                self.vdsl_band_lineattenuationDB_U2 = float(lineAttenuation.group(3).strip())
            if lineAttenuation.group(4).strip() != "N/A":
                self.vdsl_band_lineattenuationDB_U3 = float(lineAttenuation.group(4).strip())
            if lineAttenuation.group(5).strip() != "N/A":
                self.vdsl_band_lineattenuationDB_U4 = float(lineAttenuation.group(5).strip())
            if lineAttenuation.group(6).strip() != "N/A":
                self.vdsl_band_lineattenuationDB_D1 = float(lineAttenuation.group(6).strip())
            if lineAttenuation.group(7).strip() != "N/A":
                self.vdsl_band_lineattenuationDB_D2 = float(lineAttenuation.group(7).strip())
            if lineAttenuation.group(8).strip() != "N/A":
                self.vdsl_band_lineattenuationDB_D3 = float(lineAttenuation.group(8).strip())

            signalAttenuation = re.search(
                r"Signal Attenuation\(dB\):\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t\n", input_str)
            if signalAttenuation.group(1).strip() != "N/A":
                self.vdsl_band_signalattenuationDB_U0 = float(signalAttenuation.group(1).strip())
            if signalAttenuation.group(2).strip() != "N/A":
                self.vdsl_band_signalattenuationDB_U1 = float(signalAttenuation.group(2).strip())
            if signalAttenuation.group(3).strip() != "N/A":
                self.vdsl_band_signalattenuationDB_U2 = float(signalAttenuation.group(3).strip())
            if signalAttenuation.group(4).strip() != "N/A":
                self.vdsl_band_signalattenuationDB_U3 = float(signalAttenuation.group(4).strip())
            if signalAttenuation.group(5).strip() != "N/A":
                self.vdsl_band_signalattenuationDB_U4 = float(signalAttenuation.group(5).strip())
            if signalAttenuation.group(6).strip() != "N/A":
                self.vdsl_band_signalattenuationDB_D1 = float(signalAttenuation.group(6).strip())
            if signalAttenuation.group(7).strip() != "N/A":
                self.vdsl_band_signalattenuationDB_D2 = float(signalAttenuation.group(7).strip())
            if signalAttenuation.group(8).strip() != "N/A":
                self.vdsl_band_signalattenuationDB_D3 = float(signalAttenuation.group(8).strip())

            snrMargin = re.search(
                r"SNR Margin\(dB\):\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t\n", input_str)
            if snrMargin.group(1).strip() != "N/A":
                self.vdsl_band_snrMargin_U0 = float(snrMargin.group(1).strip())
            if snrMargin.group(2).strip() != "N/A":
                self.vdsl_band_snrMargin_U1 = float(snrMargin.group(2).strip())
            if snrMargin.group(3).strip() != "N/A":
                self.vdsl_band_snrMargin_U2 = float(snrMargin.group(3).strip())
            if snrMargin.group(4).strip() != "N/A":
                self.vdsl_band_snrMargin_U3 = float(snrMargin.group(4).strip())
            if snrMargin.group(5).strip() != "N/A":
                self.vdsl_band_snrMargin_U4 = float(snrMargin.group(5).strip())
            if snrMargin.group(6).strip() != "N/A":
                self.vdsl_band_snrMargin_D1 = float(snrMargin.group(6).strip())
            if snrMargin.group(7).strip() != "N/A":
                self.vdsl_band_snrMargin_D2 = float(snrMargin.group(7).strip())
            if snrMargin.group(8).strip() != "N/A":
                self.vdsl_band_snrMargin_D3 = float(snrMargin.group(8).strip())

            txPower = re.search(
                r"TX Power\(dBm\):\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t\n", input_str)
            if txPower.group(1).strip() != "N/A":
                self.vdsl_band_txPower_U0 = float(txPower.group(1).strip())
            if txPower.group(2).strip() != "N/A":
                self.vdsl_band_txPower_U1 = float(txPower.group(2).strip())
            if txPower.group(3).strip() != "N/A":
                self.vdsl_band_txPower_U2 = float(txPower.group(3).strip())
            if txPower.group(4).strip() != "N/A":
                self.vdsl_band_txPower_U3 = float(txPower.group(4).strip())
            if txPower.group(5).strip() != "N/A":
                self.vdsl_band_txPower_U4 = float(txPower.group(5).strip())
            if txPower.group(6).strip() != "N/A":
                self.vdsl_band_txPower_D1 = float(txPower.group(6).strip())
            if txPower.group(7).strip() != "N/A":
                self.vdsl_band_txPower_D2 = float(txPower.group(7).strip())
            if txPower.group(8).strip() != "N/A":
                self.vdsl_band_txPower_D3 = float(txPower.group(8).strip())

xdslinfo = XdslInfo()

def getXDSLStats(host, user, password):
    # Login first
    # Using session to store cookies:
    session = requests.session()
    session.post(host + loginpath, {
        'AuthName': user,
        'AuthPassword': password
    })
    # Get page with xDSL Stats
    xdslrequest = session.get(host + dslpath)
    # Parse page with BS
    soup = BeautifulSoup(xdslrequest.content, 'html.parser')
    # Extract text-object and parse with XdslInfo
    xdslinfo.parse(soup.find(id='VdslInfoDisplay').text)


def printDSLStats():
    log(xdslinfo)


def init():
    log("Plugin %s initializing..." % PLUGIN_NAME)


def shutdown():
    log("Plugin %s shutting down..." % PLUGIN_NAME)


def callback_configure(config):
    """ Configure callback """
    for node in config.children:
        if node.key == 'URL':
            if str(node.values[0]).endswith("/"):
                params['url'] = str(node.values[0]).rstrip("/")
            else:
                params['url'] = node.values[0]
            log("Plugin %s configured to get %s." % (PLUGIN_NAME, params['url']))
        elif node.key == 'User':
            params['user'] = node.values[0]
        elif node.key == 'Password':
            params['password'] = node.values[0]
        else:
            collectd.warning('fritzcollectd: Unknown config %s' % node.key)


def log(param):
    if __name__ != '__main__':
        collectd.info("%s: %s" % (PLUGIN_NAME, param))
    else:
        sys.stderr.write("%s\n" % param)


def read():
    getXDSLStats(params['url'], params['user'], params['password'])
    if __name__ != "__main__":
        if xdslinfo.vdsl_trainingstatus == "Showtime":
            vdsl_trainingstatus = 1
        else:
            vdsl_trainingstatus = 0
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="trainingstatus",
                        type="gauge",
                        values=[vdsl_trainingstatus]
                        ).dispatch()

        if xdslinfo.vdsl_gvector  == True:
            vdsl_gvector = 1
        else:
            vdsl_gvector = 0
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="gvector",
                        type="gauge",
                        values=[vdsl_gvector]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="uptime",
                        type="uptime",
                        values=[xdslinfo.vdsl_linkuptime_timedelta.total_seconds()]
                        ).dispatch()

        # VDSL Port Details
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="lineRate_upstream",
                        type="gauge",
                        values=[xdslinfo.vdsl_upstream_linerateMbps]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="lineRate_downstream",
                        type="gauge",
                        values=[xdslinfo.vdsl_downstream_linerateMbps]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="netDataRate_upstream",
                        type="gauge",
                        values=[xdslinfo.vdsl_upstream_netdatarateMbps]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="netDataRate_downstream",
                        type="gauge",
                        values=[xdslinfo.vdsl_downstream_netdatarateMbps]
                        ).dispatch()

        trellis = 0
        if xdslinfo.vdsl_upstream_trelliscoding:
            trellis = 1
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="trellisCoding_upstream",
                        type="gauge",
                        values=[trellis]
                        ).dispatch()

        trellis = 0
        if xdslinfo.vdsl_downstream_trelliscoding:
            trellis = 1
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="trellisCoding_downstream",
                        type="gauge",
                        values=[trellis]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="snrMargin_upstream",
                        type="gauge",
                        values=[xdslinfo.vdsl_upstream_snrmarginDB]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="snrMargin_downstream",
                        type="gauge",
                        values=[xdslinfo.vdsl_downstream_snrmarginDB]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="actualDelay_upstream",
                        type="gauge",
                        values=[xdslinfo.vdsl_upstream_actualdelayMS]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="actualDelay_downstream",
                        type="gauge",
                        values=[xdslinfo.vdsl_downstream_actualdelayMS]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="transmitPower_upstream",
                        type="gauge",
                        values=[xdslinfo.vdsl_upstream_transmitPowerDBm]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="transmitPower_downstream",
                        type="gauge",
                        values=[xdslinfo.vdsl_downstream_transmitPowerDBm]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="receivePower_upstream",
                        type="gauge",
                        values=[xdslinfo.vdsl_upstream_receivePowerDBm]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="receivePower_downstream",
                        type="gauge",
                        values=[xdslinfo.vdsl_downstream_receivePowerDBm]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="actualInpSymbols_upstream",
                        type="gauge",
                        values=[xdslinfo.vdsl_upstream_actualInpSymbols]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="actualInpSymbols_downstream",
                        type="gauge",
                        values=[xdslinfo.vdsl_downstream_actualInpSymbols]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="totalAttenuation_upstream",
                        type="gauge",
                        values=[xdslinfo.vdsl_upstream_totalAttenuationDB]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="totalAttenuation_downstream",
                        type="gauge",
                        values=[xdslinfo.vdsl_downstream_totalAttenuationDB]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="attainableNetDataRate_upstream",
                        type="gauge",
                        values=[xdslinfo.vdsl_upstream_attainableNetDataRateMbps]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="attainableNetDataRate_downstream",
                        type="gauge",
                        values=[xdslinfo.vdsl_downstream_attainableNetDataRateMbps]
                        ).dispatch()

        # VDSL Band Status
        # Line Attenuation(dB)
        if xdslinfo.vdsl_band_lineattenuationDB_U0 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U0_lineattenuation",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_lineattenuationDB_U0]
                            ).dispatch()
        if xdslinfo.vdsl_band_lineattenuationDB_U1 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U1_lineattenuation",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_lineattenuationDB_U1]
                            ).dispatch()
        if xdslinfo.vdsl_band_lineattenuationDB_U2 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U2_lineattenuation",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_lineattenuationDB_U2]
                            ).dispatch()
        if xdslinfo.vdsl_band_lineattenuationDB_U3 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U3_lineattenuation",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_lineattenuationDB_U3]
                            ).dispatch()
        if xdslinfo.vdsl_band_lineattenuationDB_U4 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U4_lineattenuation",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_lineattenuationDB_U4]
                            ).dispatch()
        if xdslinfo.vdsl_band_lineattenuationDB_D1 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="D1_lineattenuation",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_lineattenuationDB_D1]
                            ).dispatch()
        if xdslinfo.vdsl_band_lineattenuationDB_D2 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="D2_lineattenuation",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_lineattenuationDB_D2]
                            ).dispatch()
        if xdslinfo.vdsl_band_lineattenuationDB_D3 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="D3_lineattenuation",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_lineattenuationDB_D3]
                            ).dispatch()

        # Signal Attenuation(dB)
        if xdslinfo.vdsl_band_signalattenuationDB_U0 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U0_signalattenuation",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_signalattenuationDB_U0]
                            ).dispatch()
        if xdslinfo.vdsl_band_signalattenuationDB_U1 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U1_signalattenuation",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_signalattenuationDB_U1]
                            ).dispatch()
        if xdslinfo.vdsl_band_signalattenuationDB_U2 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U2_signalattenuation",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_signalattenuationDB_U2]
                            ).dispatch()
        if xdslinfo.vdsl_band_signalattenuationDB_U3 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U3_signalattenuation",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_signalattenuationDB_U3]
                            ).dispatch()
        if xdslinfo.vdsl_band_signalattenuationDB_U4 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U4_signalattenuation",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_signalattenuationDB_U4]
                            ).dispatch()
        if xdslinfo.vdsl_band_signalattenuationDB_D1 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="D1_signalattenuation",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_signalattenuationDB_D1]
                            ).dispatch()
        if xdslinfo.vdsl_band_signalattenuationDB_D2 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="D2_signalattenuation",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_signalattenuationDB_D2]
                            ).dispatch()
        if xdslinfo.vdsl_band_signalattenuationDB_D3 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="D3_signalattenuation",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_signalattenuationDB_D3]
                            ).dispatch()

        # SNR Margin(dB)
        if xdslinfo.vdsl_band_snrMargin_U0 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U0_snrMargin",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_snrMargin_U0]
                            ).dispatch()
        if xdslinfo.vdsl_band_snrMargin_U1 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U1_snrMargin",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_snrMargin_U1]
                            ).dispatch()
        if xdslinfo.vdsl_band_snrMargin_U2 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U2_snrMargin",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_snrMargin_U2]
                            ).dispatch()
        if xdslinfo.vdsl_band_snrMargin_U3 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U3_snrMargin",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_snrMargin_U3]
                            ).dispatch()
        if xdslinfo.vdsl_band_snrMargin_U4 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U4_snrMargin",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_snrMargin_U4]
                            ).dispatch()
        if xdslinfo.vdsl_band_snrMargin_D1 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="D1_snrMargin",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_snrMargin_D1]
                            ).dispatch()
        if xdslinfo.vdsl_band_snrMargin_D2 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="D2_snrMargin",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_snrMargin_D2]
                            ).dispatch()
        if xdslinfo.vdsl_band_snrMargin_D3 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="D3_snrMargin",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_snrMargin_D3]
                            ).dispatch()

        # TX Power(dBm)
        if xdslinfo.vdsl_band_txPower_U0 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U0_txPower",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_txPower_U0]
                            ).dispatch()
        if xdslinfo.vdsl_band_txPower_U1 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U1_txPower",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_txPower_U1]
                            ).dispatch()
        if xdslinfo.vdsl_band_txPower_U2 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U2_txPower",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_txPower_U2]
                            ).dispatch()
        if xdslinfo.vdsl_band_txPower_U3 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U3_txPower",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_txPower_U3]
                            ).dispatch()
        if xdslinfo.vdsl_band_txPower_U4 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="U4_txPower",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_txPower_U4]
                            ).dispatch()
        if xdslinfo.vdsl_band_txPower_D1 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="D1_txPower",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_txPower_D1]
                            ).dispatch()
        if xdslinfo.vdsl_band_txPower_D2 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="D2_txPower",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_txPower_D2]
                            ).dispatch()
        if xdslinfo.vdsl_band_txPower_D3 is not None:
            collectd.Values(plugin=PLUGIN_NAME,
                            type_instance="D3_txPower",
                            type="gauge",
                            values=[xdslinfo.vdsl_band_txPower_D3]
                            ).dispatch()
    else:
        print(xdslinfo)


if __name__ != "__main__":
    # when running inside plugin register each callback
    collectd.register_config(callback_configure)
    collectd.register_init(init)
    collectd.register_shutdown(shutdown)
    collectd.register_read(read)
else:
    # outside plugin just collect the info
    if os.environ.get('URL').endswith("/"):
        params['url'] = os.environ.get('URL').rstrip("/")
    else:
        params['url'] = os.environ.get('URL')
    params['user'] = os.environ.get('USER')
    params['password'] = os.environ.get('PASSWORD')
    read()
    if len(sys.argv) < 2:
        while True:
            time.sleep(10)
            read()
