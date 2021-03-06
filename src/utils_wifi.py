"""Module that provides all wifi sensor functionality (i.e. returning scan)."""

import os
import re
import subprocess

import pandas as pd


def get_signals():
    """Get wifi signals."""
    operating_system = os.name
    if operating_system == 'nt':
        return get_signals_windows()
    if operating_system == 'posix':
        df = get_signals_linux()
        return df

    # when here: no matching operating system
    raise Exception('Your operating system ("%s") is not supported. \
                    Currently, windows is supported' % operating_system)


def get_signals_linux():
    """Get wifi signals on linux."""
    command = 'nmcli nm wifi off && sleep 5 && nmcli nm wifi on && \
               sleep 5 && nmcli dev wifi list'
    a = subprocess.check_output(command, shell=True)
    b = str(a)
    bssids = re.findall('[0-9A-Z]{2}:[\wA-Z\:]+', b)
    bssids = [bssid.lower() for bssid in bssids]
    signals = re.findall('MB/s\s+([0-9]+)', b)
    if len(bssids) != len(signals):
        print('bssid & signals of different length!')
        return pd.DataFrame(columns=['bssid', 'signal'])
    df = pd.DataFrame({'bssid': bssids, 'signal': signals})
    return df


def get_signals_windows():
    """Get wifi signals on windows."""
    command = 'netsh wlan show networks mode=bssid'
    a = subprocess.check_output(command.split(), shell=False)
    b = str(a)
    e = re.findall('[0-9a-z\:]+\:[0-9a-z\:]+', b)
    f = re.findall('(\w+)%', b)
    df = pd.DataFrame({'bssid': e, 'signal': f})
    return df


if __name__ == '__main__':
    print(get_signals())
