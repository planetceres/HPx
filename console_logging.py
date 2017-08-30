import time

def print_blank(n):
    print(" "*n, end="\r")

def message_step(n):
    message = 'Training Step: {}'.format(n)
    return message

def tabbed_string(s, sep='\t'):
    message = ''
    if hasattr(s, '__class__') and not isinstance(s, list):
        obj = s
        for t in s.all_variables:
            h = getattr(obj, str(t))
            action_key = '  |{}| '.format(h['action'])
            message = message + '{}{}: {}'.format(action_key, t, h['value'])
    elif isinstance(s,dict):
        for k, v in s.items():
            message = message + '{}{}: {}'.format(sep, k, v)
    elif isinstance(s,list):
        for v in s:
            message = message + '{}{}'.format(sep, v)
    return message + '\t'

def print_iter(n, HPx):
    step_print = message_step(n)
    setting_string = tabbed_string(HPx, sep=' | ')
    message_str = tabbed_string([HPx.message])
    print_line = tabbed_string([step_print, setting_string, message_str], sep='')
    return print_line

def create_message(obj, n):
    direction = '+' if n >= 0 else '-'
    incrementer = ' {} {}(x{})'.format(direction, obj['increment'], abs(n))
    message = '[{}: {}]'.format(obj['name'], obj['value']-obj['increment']) + incrementer
    return message

# Countdown timer for training
def countdown(t):
    for i in list(range(t))[::-1]:
        print(i+1)
        time.sleep(0.5)
