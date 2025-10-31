import platform
import psutil
import socket
import subprocess
import os
import re


def get_system_info():
    """Собирает общую информацию о системе."""
    print("=" * 60)
    print("🔍 СКАНЕР ВИРТУАЛЬНЫХ МАШИН И LINUX СИСТЕМ")
    print("=" * 60)

    print("\n--- Информация о Системе ---")
    print(f"💻 Операционная система: {platform.system()} {platform.release()}")
    print(f"🏗️  Архитектура: {platform.architecture()[0]}")
    print(f"🏷️  Имя Компьютера: {platform.node()}")
    print(f"⚙️  Процессор: {platform.processor()}")
    print(f"🐍 Версия Python: {platform.python_version()}")


def detect_linux_mint():
    """Специальный поиск Linux Mint и других дистрибутивов."""
    print("\n" + "=" * 60)
    print("🐧 ПОИСК LINUX MINT И ДРУГИХ ДИСТРИБУТИВОВ")
    print("=" * 60)

    linux_found = False

    # Метод 1: Поиск в процессах признаков Linux Mint
    print("\n🔍 Метод 1: Анализ процессов Linux...")
    linux_processes = {
        'mint': 'Linux Mint',
        'ubuntu': 'Ubuntu',
        'debian': 'Debian',
        'kali': 'Kali Linux',
        'fedora': 'Fedora',
        'centos': 'CentOS',
        'arch': 'Arch Linux',
        'gnome': 'GNOME (Linux)',
        'kde': 'KDE (Linux)',
        'xfce': 'XFCE (Linux)',
        'cinnamon': 'Cinnamon (Linux Mint)',
    }

    for proc in psutil.process_iter(['name', 'exe', 'cmdline']):
        try:
            proc_name = proc.info['name'].lower() if proc.info['name'] else ''
            cmdline = ' '.join(proc.info['cmdline'] or []).lower()

            for key, distro in linux_processes.items():
                if key in proc_name or key in cmdline:
                    print(f"   ✅ ОБНАРУЖЕН: {distro}")
                    print(f"      Процесс: {proc.info['name']} (PID: {proc.pid})")
                    if proc.info['cmdline']:
                        print(f"      Команда: {' '.join(proc.info['cmdline'][:3])}...")
                    linux_found = True

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Метод 2: Поиск файлов и папок Linux Mint
    print("\n🔍 Метод 2: Поиск файловых признаков Linux...")
    linux_paths = [
        r"C:\Program Files\VirtualBox\HardDisks",
        r"C:\Users\{}\VirtualBox VMs".format(os.getenv('USERNAME')),
        r"C:\Users\{}\vmware".format(os.getenv('USERNAME')),
        r"C:\linux",
        r"C:\mint",
        r"C:\ubuntu",
    ]

    for path in linux_paths:
        if os.path.exists(path):
            print(f"   ✅ Обнаружен путь Linux/VM: {path}")
            # Ищем .vdi, .vmdk файлы
            try:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if any(keyword in file.lower() for keyword in ['mint', 'linux', 'ubuntu', 'debian']):
                            print(f"      Файл: {os.path.join(root, file)}")
                            linux_found = True
            except:
                pass

    # Метод 3: Поиск через VirtualBox
    print("\n🔍 Метод 3: Поиск Linux в VirtualBox...")
    try:
        # Получаем список всех ВМ
        result = subprocess.run([
            'VBoxManage', 'list', 'vms'
        ], capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            linux_vms = []
            for line in result.stdout.split('\n'):
                if any(keyword in line.lower() for keyword in ['mint', 'linux', 'ubuntu', 'debian', 'kali']):
                    linux_vms.append(line.strip())
                    linux_found = True

            if linux_vms:
                print("   ✅ Linux ВМ в VirtualBox:")
                for vm in linux_vms:
                    print(f"      🖥️  {vm}")
            else:
                print("   ❌ Linux ВМ не найдены в VirtualBox")

    except Exception as e:
        print(f"   ❌ Ошибка VirtualBox: {e}")

    # Метод 4: Поиск запущенных Linux ВМ
    print("\n🔍 Метод 4: Поиск запущенных Linux ВМ...")
    try:
        result = subprocess.run([
            'VBoxManage', 'list', 'runningvms'
        ], capture_output=True, text=True, timeout=10)

        if result.returncode == 0 and result.stdout.strip():
            running_vms = []
            for line in result.stdout.split('\n'):
                if any(keyword in line.lower() for keyword in ['mint', 'linux', 'ubuntu', 'debian']):
                    running_vms.append(line.strip())
                    linux_found = True

            if running_vms:
                print("   ✅ ЗАПУЩЕННЫЕ Linux ВМ:")
                for vm in running_vms:
                    print(f"      🚀 {vm}")

                    # Получаем подробности о запущенной ВМ
                    vm_name = vm.split('{')[0].strip().strip('"')
                    try:
                        result = subprocess.run([
                            'VBoxManage', 'guestproperty', 'enumerate', vm_name
                        ], capture_output=True, text=True, timeout=10)

                        if result.returncode == 0:
                            for prop_line in result.stdout.split('\n'):
                                if 'OSType' in prop_line:
                                    print(f"         {prop_line.strip()}")
                                    break
                    except:
                        pass
            else:
                print("   ❌ Запущенных Linux ВМ не найдено")

    except Exception as e:
        print(f"   ❌ Ошибка проверки запущенных ВМ: {e}")

    # Метод 5: Анализ сетевых подключений к Linux
    print("\n🔍 Метод 5: Анализ сетевых подключений...")
    try:
        # Проверяем сетевые подключения к стандартным Linux портам
        linux_ports = [22,  # SSH
                       80,  # HTTP
                       443,  # HTTPS
                       3306,  # MySQL
                       5432]  # PostgreSQL

        for conn in psutil.net_connections():
            if conn.status == 'ESTABLISHED' and conn.raddr:
                if conn.raddr.port in linux_ports:
                    print(f"   🔗 Подключение к Linux-порту {conn.raddr.port} на {conn.raddr.ip}")
                    linux_found = True

    except Exception as e:
        print(f"   ❌ Ошибка анализа сетевых подключений: {e}")

    # Метод 6: Поиск через реестр (для WSL2 с Linux Mint)
    print("\n🔍 Метод 6: Поиск в реестре...")
    try:
        result = subprocess.run([
            'reg', 'query', 'HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Lxss', '/s'
        ], capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if any(keyword in line.lower() for keyword in ['mint', 'ubuntu', 'debian']):
                    print(f"   ✅ Обнаружен в реестре: {line.strip()}")
                    linux_found = True

    except Exception as e:
        print(f"   ❌ Ошибка поиска в реестре: {e}")

    # Итог поиска Linux Mint
    print("\n" + "=" * 60)
    if linux_found:
        print("🎯 LINUX СИСТЕМЫ ОБНАРУЖЕНЫ!")
    else:
        print("❌ Linux Mint не обнаружен")
        print("\n💡 Возможные причины:")
        print("   - Linux Mint не установлен")
        print("   - ВМ с Linux Mint не запущена")
        print("   - Linux Mint установлен в другой системе")
        print("   - Используется другое имя для ВМ")


def get_linux_mint_details():
    """Получение детальной информации о Linux Mint если он найден"""
    print("\n" + "=" * 60)
    print("🍃 ДЕТАЛЬНАЯ ИНФОРМАЦИЯ О LINUX MINT")
    print("=" * 60)

    try:
        # Пытаемся найти ВМ с Linux Mint в VirtualBox
        result = subprocess.run([
            'VBoxManage', 'list', 'vms'
        ], capture_output=True, text=True, timeout=10)

        mint_vms = []
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'mint' in line.lower():
                    mint_vms.append(line.strip())

        if mint_vms:
            print("✅ ВИРТУАЛЬНЫЕ МАШИНЫ LINUX MINT:")
            for vm_info in mint_vms:
                print(f"   🖥️  {vm_info}")

                # Извлекаем имя ВМ
                vm_name = vm_info.split('{')[0].strip().strip('"')

                # Получаем подробную информацию о ВМ
                print(f"\n   📊 Информация о ВМ '{vm_name}':")

                # Информация о ОС
                try:
                    result = subprocess.run([
                        'VBoxManage', 'showvminfo', vm_name, '--machinereadable'
                    ], capture_output=True, text=True, timeout=10)

                    if result.returncode == 0:
                        for line in result.stdout.split('\n'):
                            if 'ostype=' in line:
                                print(f"      ОС: {line.split('=')[1].strip('\"')}")
                            elif 'memory=' in line:
                                memory_mb = line.split('=')[1].strip('\"')
                                print(f"      Память: {memory_mb} MB")
                            elif 'cpus=' in line:
                                cpus = line.split('=')[1].strip('\"')
                                print(f"      Процессоры: {cpus}")
                except Exception as e:
                    print(f"      ❌ Ошибка получения информации: {e}")

                # Проверяем запущена ли ВМ
                try:
                    result = subprocess.run([
                        'VBoxManage', 'list', 'runningvms'
                    ], capture_output=True, text=True, timeout=10)

                    if vm_name in result.stdout:
                        print("      🟢 Статус: ЗАПУЩЕНА")

                        # Пытаемся получить IP адрес запущенной ВМ
                        try:
                            result = subprocess.run([
                                'VBoxManage', 'guestproperty', 'get', vm_name, '/VirtualBox/GuestInfo/Net/0/V4/IP'
                            ], capture_output=True, text=True, timeout=10)

                            if result.returncode == 0 and 'Value:' in result.stdout:
                                ip = result.stdout.split('Value:')[1].strip()
                                if ip and ip != 'No value set!':
                                    print(f"      🌐 IP адрес: {ip}")
                        except:
                            pass
                    else:
                        print("      🔴 Статус: ОСТАНОВЛЕНА")
                except:
                    pass

        else:
            print("❌ Виртуальные машины Linux Mint не найдены в VirtualBox")

    except Exception as e:
        print(f"❌ Ошибка получения деталей: {e}")


def detect_virtualization():
    """Обнаружение виртуальных машин различными методами."""
    print("\n" + "=" * 60)
    print("🖥️  ПОИСК ВИРТУАЛЬНЫХ МАШИН")
    print("=" * 60)

    # ... (остальной код detect_virtualization остается без изменений)
    # Тот же код что был раньше


def main():
    """Главная функция."""
    try:
        get_system_info()
        detect_virtualization()

        # ДОБАВЛЯЕМ ПОИСК LINUX MINT
        detect_linux_mint()
        get_linux_mint_details()

        print("\n" + "=" * 60)
        print("✅ СКАНИРОВАНИЕ ЗАВЕРШЕНО")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Ошибка при сканировании: {e}")


if __name__ == "__main__":
    main()