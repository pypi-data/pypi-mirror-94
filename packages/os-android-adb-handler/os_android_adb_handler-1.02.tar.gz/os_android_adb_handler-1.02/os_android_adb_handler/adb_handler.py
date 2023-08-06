from os_tools import tools
from os_android_adb_handler import key_events


###################################################
# This module aims to provide ADB general actions #
###################################################

def start_app(package_name, path_to_first_activity):
    """
    Will start an already installed App in the device.

    Args:
        package_name: The app's package name
        path_to_first_activity: The relative path to the first activity (like main.MainActivity)
    """
    send_shell(f'am start -n {package_name}/{package_name}.{path_to_first_activity}')


def take_ss(ss_file_path):
    """
    Will take a screen shot.

    Args:
        ss_file_path: The destination path of the screen shot (file name, incl extension)
    """
    adb(f'exec-out screencap -p >"{ss_file_path}"')


def install_apk(apk_path):
    """
    Will install an APK file.

    Args:
        apk_path: The path to your APK file.
    """
    adb(f'install "{apk_path}"')


def uninstall_app(package_name):
    """
    Will uninstall an app.

    Args:
        package_name: The app's package name
    """
    adb(f'uninstall "{package_name}"')


def go_back():
    """
    Will navigate back
    """
    key_event(key_events.KEYCODE_BACK)


def enter():
    """
    Will click the Enter key
    """
    key_event(key_events.KEYCODE_ENTER)


def dpad_right():
    """
    Will click the Right key
    """
    key_event(key_events.KEYCODE_DPAD_RIGHT)


def dpad_left():
    """
    Will click the Left key
    """
    key_event(key_events.KEYCODE_DPAD_LEFT)


def dpad_up():
    """
    Will click the Up key
    """
    key_event(key_events.KEYCODE_DPAD_UP)


def dpad_down():
    """
    Will click the Down key
    """
    key_event(key_events.KEYCODE_DPAD_DOWN)


def key_event(key):
    """
    Will send a key event.
    
    Args:
        key: The key you want to send. You can use of the key_events keys
    """
    send_input(f'keyevent {key}')


def send_input(event):
    """
    Will send an input event
    """
    send_shell(f'input {event}')


def send_shell(command):
    """
    Will send a shell command
    """
    adb(f'shell {command}')


def adb(command):
    """
    Will send an adb command
    """
    tools.run_command(f'adb {command}')


def swipe(from_x, to_x, from_y, to_y, duration=500):
    """
    Will send a swipe event (this can also be used to scroll).

    Examples:
        For horizontal swipe right you can set the :param from_x to be somehow hight, like 1000 and the :param to_x to be at the start
        of the screen, like 200. The :param from_y and :param to_y would be the pivots in this case, with the same value
        (lower values for swiping horizontally on screen top and high values for swiping horizontally on bottom).

    Args:
        from_x: The starting point in the X axis
        to_x: The ending point in the X axis
        from_y: The starting point in the Y axis
        to_y: The ending point in the Y axis
        duration: The time it will take to perform the swipe
    """
    send_input(f'swipe {from_x} {from_y} {to_x} {to_y} {duration}')


def clear_app_cache(package_name):
    """
    Will clear an app's cache

    Args:
        package_name: the package name of the app you wish to clear it's cache
    """
    send_shell(f'pm clear {package_name}')
