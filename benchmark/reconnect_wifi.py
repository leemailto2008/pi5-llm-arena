import ctypes
from ctypes import wintypes
import time

class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", wintypes.BYTE * 8)
    ]

class WLAN_INTERFACE_INFO(ctypes.Structure):
    _fields_ = [
        ("InterfaceGuid", GUID),
        ("strInterfaceDescription", wintypes.WCHAR * 256),
        ("isState", wintypes.DWORD)
    ]

class WLAN_INTERFACE_INFO_LIST(ctypes.Structure):
    _fields_ = [
        ("dwNumberOfItems", wintypes.DWORD),
        ("dwIndex", wintypes.DWORD),
        ("InterfaceInfo", WLAN_INTERFACE_INFO * 1)
    ]

class WLAN_CONNECTION_PARAMETERS(ctypes.Structure):
    _fields_ = [
        ("wlanConnectionMode", wintypes.DWORD),
        ("strProfile", wintypes.LPCWSTR),
        ("pDot11Ssid", ctypes.c_void_p),
        ("pDesiredBssidList", ctypes.c_void_p),
        ("dot11BssType", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD)
    ]

def connect_wifi():
    wlanapi = ctypes.windll.wlanapi
    handle = wintypes.HANDLE()
    negotiated = wintypes.DWORD()
    ret = wlanapi.WlanOpenHandle(2, None, ctypes.byref(negotiated), ctypes.byref(handle))
    if ret != 0:
        print(f"Failed WlanOpenHandle: {ret}")
        return False

    pIfList = ctypes.c_void_p()
    ret = wlanapi.WlanEnumInterfaces(handle, None, ctypes.byref(pIfList))
    if ret != 0:
        print(f"Failed WlanEnumInterfaces: {ret}")
        return False

    ifList = WLAN_INTERFACE_INFO_LIST.from_address(pIfList.value)
    print(f"Found {ifList.dwNumberOfItems} interfaces.")

    if ifList.dwNumberOfItems > 0:
        guid = ifList.InterfaceInfo[0].InterfaceGuid
        conn_params = WLAN_CONNECTION_PARAMETERS()
        conn_params.wlanConnectionMode = 0 # wlan_connection_mode_profile
        conn_params.strProfile = "My_2G_Guest1"
        conn_params.pDot11Ssid = None
        conn_params.pDesiredBssidList = None
        conn_params.dot11BssType = 1 # dot11_BSS_type_infrastructure
        conn_params.dwFlags = 0

        print("Connecting to My_2G_Guest1...")
        ret = wlanapi.WlanConnect(handle, ctypes.byref(guid), ctypes.byref(conn_params), None)
        print(f"WlanConnect result: {ret}")

    wlanapi.WlanCloseHandle(handle, None)
    return True

if __name__ == "__main__":
    connect_wifi()
