import platform as _platform
import keyboard
from console_logging import create_message

if _platform.system() == 'Windows':
    print("Windows OS detected")
    PLATFORM = "win"
    #from key_mapping.keystate_win import key_state
    #from. import _winmouse as _os_mouse
elif _platform.system() == 'Linux':
    print("Linux OS detected")
    PLATFORM = "linux"
    #from key_mapping.keystate_linux import key_state
    #from. import _nixmouse as _os_mouse
elif _platform.system() == 'Darwin':
    print("Darwin OS detected")
    PLATFORM = "darwin"
    #from key_mapping.keystate_mac import key_state
    #from. import _darwinmouse as _os_mouse
else:
    PLATFORM = None
    raise OSError("Unsupported platform '{}'".format(_platform.system()))

kevent = []

def valid_keys():
    validKeys = ["\b"]
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'-=£$/\\":
        validKeys.append(c)
    return validKeys

class Hyperparams(object):
    def __init__(self, hyperparams):

        active_keys = []
        for (k, v) in hyperparams.items():
            self.__dict__[k] = v
            required = ['action', 'value', 'increment', 'name']
            if not set(required).issubset(set(self.__dict__[k].keys())):
                raise KeyError("Missing hyperparameter values. Must include all fields: {}".format(required))
            active_keys.append(v['action'])
        self.all_variables = [k for (k, v) in self.__dict__.items()]
        self.all_keys = active_keys
        self.message = ''
        self.keys_state = {
            'keys': [],
            'kevent': [],
            'inc_minus': [],
            'inc_plus': [],
            'inc_n': 0
            }

    def update(self, param, attr, v):
        self.__dict__[param][attr] = v

    def _append(self, param, attr, v):
        self.__dict__[param][attr].append(v)


def platform_type(self):
    if _platform.system() == 'Windows':
        PLATFORM = "win"
    elif _platform.system() == 'Linux':
        PLATFORM = "linux"
    elif _platform.system() == 'Darwin':
        PLATFORM = "darwin"
    else:
        PLATFORM = None

    return self.PLATFORM

def hyperparam_change(HPx):
    '''
    Change hyperparameters based on input
    '''
    global kevent
    if len(kevent) > 0:
        HPx = get_event_keys(HPx)
        # kevent = []
        HPx.update('keys_state', 'kevent', [])
    key_action = HPx.keys_state['keys']
    # reset key state
    HPx.update('keys_state', 'keys', [])
    keys = [k.upper() for k in set(key_action)]
    # get increment/decrement counts for variable
    HPx.update('keys_state', 'inc_n', 0)
    HPx = get_increment_n(HPx)

    signs = ['=', '-']
    HPx.message = ''

    if any(a in keys for a in HPx.all_keys):
        for k in HPx.all_keys:
            if (k in keys) and any(x in keys for x in signs):
                for key, value in HPx.__dict__.items():
                    if isinstance(value, dict):
                        try:
                            if ('action' in value.keys()) and value['action'] == k:
                                t = key
                        except TypeError as e:
                            pass
                param = getattr(HPx, t)
                param['value'] = param['value'] + param['increment']*HPx.keys_state['inc_n']
                HPx.update(t, 'value', param['value'])
                HPx.message = create_message(param, HPx.keys_state['inc_n'])

    return HPx

def get_increment_n(HPx):
    '''
        capture how many times the `-` or `=` keys were pressed since last loop:
        'down' = pressed
        `up` = released
        we have to do it this way since the keypress is captured at (t)
        microintervals of time within an epoch and we just end up with a list
        where the change between `up` and `down` is what matters
    '''
    plus = HPx.keys_state['inc_plus']
    minus = HPx.keys_state['inc_minus']
    n = HPx.keys_state['inc_n']

    # count keypress events for increments (+)
    if len(plus) > 0:
        if plus[0] == 'up': n += 1
        for i in range(len(plus)):
            if (plus[i-1] != 'down') and (plus[i] == 'down'):
                n+=1
    # count keypress events for decrements (-)
    if len(minus) > 0:
        if minus[0] == 'up': n -= 1
        for i in range(len(minus)):
            if (minus[i-1] != 'down') and (minus[i] == 'down'): n-=1

    # update number of increments and reset increment up/down caches
    HPx.update('keys_state', 'inc_n', n)
    HPx.update('keys_state', 'inc_plus', [])
    HPx.update('keys_state', 'inc_minus', [])

    return HPx

def get_event(event):
    global kevent
    kevent.append(event)
    return kevent

def get_event_keys(HPx):
    '''
    values
    ---------------------
    event.event_type: up or down (key state)
    event.name: key name
    event.scan_code: key scan code
    event.time: time of event
    '''
    global kevent
    validKeys = valid_keys()
    signs = ['-', '=']
    for event in kevent:
        if event.name:
            key = event.name
            if key and key.upper() in validKeys:
                #keys.append(key) if key not in keys else None
                HPx._append('keys_state', 'keys', key) if key not in HPx.keys_state['keys'] else None
            if key in signs and key == '-': HPx._append('keys_state', 'inc_minus', event.event_type)
            if key in signs and key == '=': HPx._append('keys_state', 'inc_plus', event.event_type)

    # reset keypress event cache
    kevent = []

    #sys.stdout.flush()

    return HPx


def hyperstate(HPx):
    HPx = hyperparam_change(HPx)
    # mac os
    if PLATFORM == 'darwin':
        keyboard.hook(get_event)
    # Windows
    elif PLATFORM == 'win':
        keys = key_check()
    return HPx
