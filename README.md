# 🔍 VM & Linux Scanner

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Мощный сканер для обнаружения виртуальных машин и Linux-систем в Windows-окружении. Инструмент предназначен для системных администраторов, специалистов по кибербезопасности и DevOps-инженеров.

## 🚀 Возможности

- **🔍 Обнаружение Linux систем**: Linux Mint, Ubuntu, Debian, Kali Linux и других дистрибутивов
- **🖥️ Детекция виртуальных машин**: VirtualBox, VMware и другие гипервизоры
- **📊 Системная информация**: Получение детальной информации о хост-системе
- **🌐 Сетевой анализ**: Обнаружение сетевых подключений к Linux-портам
- **⚡ Множественные методы обнаружения**:
  - Анализ запущенных процессов
  - Поиск файловых признаков
  - Проверка VirtualBox/VMware
  - Анализ сетевых подключений
  - Поиск в реестре Windows

## 📦 Установка

### Предварительные требования

- Windows 7/8/10/11
- Python 3.6 или выше
- VirtualBox (для полного функционала)

### Установка зависимостей

```bash
pip install psutil
