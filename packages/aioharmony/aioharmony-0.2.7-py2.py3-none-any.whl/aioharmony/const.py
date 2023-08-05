# -*- coding: utf-8 -*-

"""
Constants used throughout the modules
"""

import asyncio
from typing import Any, Callable, List, NamedTuple, Optional, Union

#
# DEFAULT values
#
DEFAULT_CMD = 'vnd.logitech.connect'
DEFAULT_DISCOVER_STRING = '_logitech-reverse-bonjour._tcp.local.'
DEFAULT_XMPP_HUB_PORT = '5222'
DEFAULT_WS_HUB_PORT = '8088'
DEFAULT_HARMONY_MIME = 'vnd.logitech.harmony/vnd.logitech.harmony.engine'

WEBSOCKETS = 'WEBSOCKETS'
XMPP = 'XMPP'

PROTOCOL = Union[WEBSOCKETS, XMPP]

#
# The HUB commands that can be send
#
HUB_COMMANDS = {
    'change_channel': {
        'mime': 'harmony.engine',
        'command': 'changeChannel'
    },
    'get_current_state': {
        'mime': 'vnd.logitech.connect/vnd.logitech.statedigest',
        'command': 'get'
    },
    'get_config': {
        'mime': DEFAULT_HARMONY_MIME,
        'command': 'config'
    },
    'get_current_activity': {
        'mime': DEFAULT_HARMONY_MIME,
        'command': 'getCurrentActivity'
    },
    'send_command': {
        'mime': DEFAULT_HARMONY_MIME,
        'command': 'holdAction'
    },
    'start_activity': {
        'mime': 'harmony.activityengine',
        'command': 'runactivity'
    },
    'sync': {
        'mime': 'setup.sync',
        'command': None
    },
    'provision_info': {
        'mime': 'setup.account',
        'command': 'getProvisionInfo'
    },
    'discovery': {
        'mime': 'connect.discoveryinfo',
        'command': 'get'
    },
}

#
# Different types used within aioharmony
#

# Type for callback parameters
CallbackType = Union[
    asyncio.Future,
    asyncio.Event,
    Callable[[object, Optional[Any]], Any]
]

ClientCallbackType = NamedTuple('ClientCallbackType',
                                [('connect', Optional[CallbackType]),
                                 ('disconnect', Optional[CallbackType]),
                                 ('new_activity_starting', Optional[CallbackType]),
                                 ('new_activity', Optional[CallbackType]),
                                 ('config_updated', Optional[CallbackType])
                                 ])

ConnectorCallbackType = NamedTuple('ConnectorCallbackType',
                                   [('connect', Optional[CallbackType]),
                                    ('disconnect', Optional[CallbackType])
                                    ])

ClientConfigType = NamedTuple('ClientConfigType',
                              [('config', dict),
                               ('info', dict),
                               ('discover_info', dict),
                               ('hub_state', dict),
                               ('config_version', Optional[int]),
                               ('activities', List[dict]),
                               ('devices', List[dict])
                               ])

# Type for a command to send to the HUB
SendCommandDevice = NamedTuple('SendCommandDevice',
                               [('device', int),
                                ('command', str),
                                ('delay', float)
                                ])

# Type for send command to aioharmony,
SendCommand = Union[SendCommandDevice, Union[float, int]]
SendCommandArg = Union[SendCommand, List[SendCommand]]

# Response from send commands.
SendCommandResponse = NamedTuple('SendCommandResponse',
                                 [('command', SendCommandDevice),
                                  ('code', str),
                                  ('msg', str)
                                  ])
