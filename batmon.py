#!/usr/bin/env python

#Monitors battery status and displays a warning 

import os
import sys
import time
import argparse
from subprocess import Popen

import batinfo

from daemon import Daemon

WARNING_POPUP_CMD = ['zenity', '--warning', '--text=Battery critically low,\nconnect your charger!']
WARNING_SOUND_CMD = ['paplay', '/usr/share/sounds/ubuntu/stereo/dialog-question.ogg']
CRITICAL_SUSPEND_CMD = ['pm-suspend']
PID_PATH = os.path.expanduser('~/.batmon.pid')

class Status:
    charging = 'Charging'
    discharging = 'Discharging'

class Config:
    #TODO: allow user to config what commands to run when thresholds
    # are met.
    def __init__(
            self,
            warningThreshold,
            criticalThreshold,
            pollInterval,
            silent,
            ):
        self.warningThreshold = warningThreshold
        self.criticalThreshold = criticalThreshold
        self.pollInterval = pollInterval
        self.silent = silent

class Batmon(Daemon):

    def __init__(self, config):
        self.config = config
        #we need to do this here since daemonize redirects stdout and stderr
        if self.config.criticalThreshold != None:
            if os.geteuid() != 0:
                sys.stderr.write("You need to be root to run with a critical threshold.\nPlease try again using 'sudo'.\n")
                exit(0)
        super(Batmon, self).__init__(PID_PATH)

    def run(self):
        self.main()

    def main(self):
        bat = batinfo.Batteries()
        isWarningHandled = False
        if self.config.criticalThreshold == None:
            iscriticalHandled = True
        else:
            #check if root
            iscriticalHandled = False

        if len(bat.stat) <1:
            sys.stderr.write("No battery found")
            self.daemon_alive = False
            sys.exit(1)

        while(not isWarningHandled or not iscriticalHandled):
            bat.update()
            stat = bat.stat[0]

            if stat.status == Status.discharging:
                if (not isWarningHandled) and  stat.capacity < self.config.warningThreshold:
                    if not self.config.silent:
                        Popen(WARNING_SOUND_CMD)
                    Popen(WARNING_POPUP_CMD)
                    isWarningHandled = True

                if not iscriticalHandled and stat.capacity <= self.config.criticalThreshold:
                    #TODO: handle critical
                    Popen(CRITICAL_SUSPEND_CMD)
                    self.daemon_alive = False
                    sys.exit()

            time.sleep(self.config.pollInterval)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Monitors the battery status and displays a warning message along with sound when it goes below a given threshold")
    parser.add_argument('-t', '--terminate', action='store_true',
            help='stop the daemon')
    parser.add_argument('-s', '--start', action='store_true',
            help='start the daemon')
    parser.add_argument('-c', '--critical', default=None,
            help='(requires root) the battery percentage at which the computer is suspended. If not set Batmon will not suspend the computer on low battery.')
    parser.add_argument('-w', '--warning', default=10, type=int,
            help='the battery percentage at which a low battery warning is issued. If not set the default value of 10 is used.')
    parser.add_argument('-p', '--pollInterval', default=60, type=int,
            help='the interval in which the battery status is polled. Default = 60.')
    parser.add_argument('--silent', action='store_true', 
            help='disables the warning sound')
    parser.add_argument('--debug', action='store_true',
            help='run the code without daemon')
    args = parser.parse_args()

    config = Config(
                args.warning,
                args.critical,
                args.pollInterval,
                args.silent,
            )

    batmon = Batmon(config)

    if args.debug:
        batmon.main()
    else:
        if args.start:
            batmon.start()
        elif args.terminate:
            batmon.stop()
