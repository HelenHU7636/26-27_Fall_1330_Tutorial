#!/bin/sh
# Supply layout defaults without hiding the physical terminal dimensions.
# macOS SIGINFO (29) can be forwarded numerically as Linux SIGIO (29).
# These terminal games do not use asynchronous I/O signals.
trap '' IO
export COLUMNS=80 LINES=24
exec "$@"
