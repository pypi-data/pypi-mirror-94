"""
android constants and helper functions
======================================

For to include this ae namespace portion into your project add the following import statement into your main
module (main.py) of your application project::

    import ae.droid

This import will ensure that all your permissions will be requested on app startup. On other platforms than Android
it will have no effect.
"""
import os
from ae.base import os_platform                                         # type: ignore


__version__ = '0.1.1'


if os_platform == 'android':
    # noinspection PyUnresolvedReferences
    from android.permissions import request_permissions, Permission     # type: ignore # pylint: disable=import-error
    from jnius import autoclass                                         # type: ignore

    def log(log_level: str, message: str, file_path: str = ""):
        """ print log message. """
        if not file_path:
            file_path = f"ae_droid_{log_level}.log"
        with open(file_path, 'a') as log_file:
            log_file.write(message + "\n")

    PACKAGE_NAME = 'package'
    PACKAGE_DOMAIN = 'org.test'
    PERMISSIONS = "INTERNET, VIBRATE, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE"

    BUILD_CONFIG_FILE = 'buildozer.spec'
    if os.path.exists(BUILD_CONFIG_FILE):
        from configparser import ConfigParser

        config = ConfigParser(allow_no_value=True)
        # silly mypy does not allow: config.optionxform = lambda value: value  -nor-  str
        setattr(config, 'optionxform', str)
        config.read(BUILD_CONFIG_FILE, "utf-8")
        PACKAGE_NAME = config.get('app', 'package.name', fallback=PACKAGE_NAME)
        PACKAGE_DOMAIN = config.get('app', 'package.domain', fallback=PACKAGE_DOMAIN)
        PERMISSIONS = config.get('app', 'android.permissions', fallback=PERMISSIONS)
    else:
        log('debug', f"{BUILD_CONFIG_FILE} is not bundled into the APK - using defaults")

    # request app/service permissions
    permissions = list()
    for permission_str in PERMISSIONS.split(','):
        permission = getattr(Permission, permission_str.strip(), None)
        if permission:
            permissions.append(permission)
    request_permissions(permissions)

    def start_service(service_arg: str = ""):
        """ start service.

        :param service_arg:     string value to be assigned to environment variable PYTHON_SERVICE_ARGUMENT on start.

        see https://github.com/tshirtman/kivy_service_osc/blob/master/src/main.py
        and https://python-for-android.readthedocs.io/en/latest/services/#arbitrary-scripts-services
        """
        service_instance = autoclass(f"{PACKAGE_DOMAIN}.{PACKAGE_NAME}.Service{PACKAGE_NAME.capitalize()}")
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        service_instance.start(activity, service_arg)        # service_arg will be in env var PYTHON_SERVICE_ARGUMENT

        return service_instance
