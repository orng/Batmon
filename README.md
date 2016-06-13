# Batmon
A simple battery monitor for unix.

Batmon runs as a daemon and monitors the charge percentage of the battery while it is discharging and takes two actions depending on two user provided thresholds: `warning` and `critical`. 

When the `warning` threshold is triggered a popup is displayed along with sound, warning the user that the battery is running low.

When the `critical`threhold is triggered the computer is suspended.

##Usage
```
usage: batmon.py [-h] [-t] [-s] [-c CRITICALTHRESHOLD] [-w WARNINGTHRESHOLD]
                 [-p POLLINTERVAL] [--silent] [--debug]

Monitors the battery status and displays a warning message along with sound
when it goes below a given threshold

optional arguments:
  -h, --help            show this help message and exit
  -t, --terminate       stop the daemon
  -s, --start           start the daemon
  -c CRITICALTHRESHOLD, --criticalThreshold CRITICALTHRESHOLD
                        (requires root) the battery percentage at which the computer is
                        suspended.  If not set Batmon will not suspend the
                        computer on low battery.
  -w WARNINGTHRESHOLD, --warningThreshold WARNINGTHRESHOLD
                        the battery percentage at which a low battery warning
                        is issued. If not set the default value of 10 is used.
  -p POLLINTERVAL, --pollInterval POLLINTERVAL
                        the interval in which the battery status is polled. Default = 60.
  --silent              disables the warning sound
  --debug               run the code without daemon

```

###Example
Start the Batmon daemon, set to display a warning at 14% battery and to suspend the computer at 5%, with a poll interval of 45s.
```
python Batmon.py --start -w 14 -c 5 -p 45
```

##Dependencies
Batmon depends on the following shell commands
* zenity
* paplay
* pm-suspend
* [python-daemon](https://github.com/serverdensity/python-daemon) (included in this repo)

##TODO
* Allow the user to configure the commands run after hitting the thresholds
* Perhaps with support for config files
