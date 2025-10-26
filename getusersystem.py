import platform
import subprocess
import logging


def get_system_info(abbreviated_dict: bool = True) -> dict[str, str]:
    """для любой ос ваще похуй"""
    system_info = {}

    system_info['OS'] = platform.system()
    system_info['OS Version'] = platform.version()  # в будущем это убрать
    system_info['Platform'] = platform.platform()   # это тоже

    system_info['Processor'] = platform.processor() # этого тоже на кол

    try:
        if platform.system() == "Windows":
            """for win"""
            import winreg
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\BIOS")
                system_info['System Model'] = winreg.QueryValueEx(key, "SystemProductName")[0]
                system_info['Manufacturer'] = winreg.QueryValueEx(key, "SystemManufacturer")[0]
                winreg.CloseKey(key)
            except Exception as e:
                system_info['System Model'] = f"Не удалось получить: {e}"

        elif platform.system() == "Darwin":
            """мак шифруется ниче больше мы не узнаем"""
            result = subprocess.check_output(['sysctl', '-n', 'hw.model'])
            system_info['Mac Model'] = result

        if platform.system() == "Linux":
            """Linux"""
            try:
                with open('/sys/class/dmi/id/product_name', 'r') as f:
                    system_info['Product Name'] = f.read().strip()
                with open('/sys/class/dmi/id/sys_vendor', 'r') as f:
                    system_info['System Vendor'] = f.read().strip()

            except: # alt way

                result = subprocess.check_output(['lshw', '-json'], stderr=subprocess.DEVNULL).decode()
                system_info['Hardware Info'] = result[:500] + "..." if len(result) > 500 else result

    except Exception as e:
        system_info['Error'] = f"Ошибка при получении информации: {e}"

    return system_info


def main():
    print("=" * 20)
    print("сбор инфы о системе дурачка")
    print("=" * 20)

    info = get_system_info()

    for key, value in info.items():
        print(f"{key}: {value}")

    print('\n')
    print("доп инфа")
    print("=" * 10)
    print(f"Компьютер: {platform.node()}")
    print(f"Архитектура: {platform.architecture()[0]}")
    print(f"Версия пайтона: {platform.python_version()}")


if __name__ == "__main__":
    main()
