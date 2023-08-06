"""
weitersager.signals
~~~~~~~~~~~~~~~~~~~

Signals

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from blinker import signal


channel_joined = signal('channel-joined')
message_received = signal('message-received')
message_approved = signal('message-approved')
