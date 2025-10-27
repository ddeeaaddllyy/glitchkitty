import platform
import subprocess
import logging


def get_system_info(full_dict: bool = False) -> dict[str, str]:
    """для любой ос ваще похуй"""
    system_info = {
        'OS': platform.system()
    }

    if full_dict:
        system_info['OS Version'] = platform.version()
        system_info['Platform'] = platform.platform()
        system_info['Processor'] = platform.processor()

    try:
        if platform.system() == "Windows":
            import winreg
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\BIOS")
                system_info['Manufacturer'] = winreg.QueryValueEx(key, "SystemManufacturer")[0]

                if full_dict:
                    system_info['System Model'] = winreg.QueryValueEx(key, "SystemProductName")[0]
                winreg.CloseKey(key)
            except Exception as e:
                system_info['System Model'] = f"Не удалось получить: {e}"

        elif platform.system() == "Darwin":

            result = subprocess.check_output(['sysctl', '-n', 'hw.model'])
            system_info['Mac Model'] = result

        if platform.system() == "Linux":

            try:
                with open('/sys/class/dmi/id/sys_vendor', 'r') as f:
                    system_info['System Vendor'] = f.read().strip()

                if full_dict:
                    with open('/sys/class/dmi/id/product_name', 'r') as f:
                        system_info['Product Name'] = f.read().strip()

            except: # alt way
                result = subprocess.check_output(['lshw', '-json'], stderr=subprocess.DEVNULL).decode()
                system_info['Hardware Info'] = result[:500] + "..." if len(result) > 500 else result

    except Exception as e:
        system_info['Error'] = f"Ошибка при получении информации: \n{e}"

    return system_info
