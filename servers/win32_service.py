import os
import sys
import pickle

import win32serviceutil
import win32api
import winerror
import win32service


def service_install(cls, name, display_name, server_key, config, stay_alive=True):
    ''' Install and  Start (auto) a Service
        cls : the class (derived from Service) that implement the Service
        name : Service name
        display_name : the name displayed in the service manager
        stay_alive : Service will stop on logout if False
    '''
    cls._svc_name_ = name
    cls._svc_display_name_ = display_name or name
    module_path = sys.modules[cls.__module__].__file__
    module_file = os.path.splitext(os.path.abspath(module_path))[0]
    cls._svc_reg_class_ = '%s.%s' % (module_file, cls.__name__)
    if stay_alive:
        win32api.SetConsoleCtrlHandler(lambda x: True, True)
    try:
        win32serviceutil.InstallService(
            cls._svc_reg_class_,
            cls._svc_name_,
            cls._svc_display_name_,
            exeArgs=cls._svc_name_
        )
    except win32service.error, exc:
        if exc.winerror == winerror.ERROR_SERVICE_EXISTS:
            print("Service exists")
            try:
                win32serviceutil.ChangeServiceConfig(
                    cls._svc_reg_class_,
                    cls._svc_name_,
                    displayName=cls._svc_display_name_,
                    exeArgs=cls._svc_name_
                )
            except win32service.error, exc:
                raise
        else:
            raise

    print("Finished init")

    win32serviceutil.SetServiceCustomOption(cls._svc_name_, "server_key", pickle.dumps(server_key))
    win32serviceutil.SetServiceCustomOption(cls._svc_name_, "config", pickle.dumps(config))


def service_start(name):
    try:
        win32serviceutil.StartService(name)
    except win32service.error, exc:
        if exc.winerror == winerror.ERROR_SERVICE_ALREADY_RUNNING:
            print("Reattaching")
        else:
            raise


def service_stop(name):
    try:
        win32serviceutil.StopService(name)
    except Exception, x:
        print str(x)
