#!/bin/bash

# Termux OSINT & Security Framework 설치 스크립트

echo -e "\033[96m\033[1m"
echo "   ___ ____  ____  _   _ _____ _____ _____ _   _ "
echo "  / _ \___ \|  _ \| | | | ____|_   _|_   _| \ | |"
echo " | | | |__) | |_) | | | |  _|   | |   | | |  \| |"
echo " | |_| / __/|  _ <| |_| | |___  | |   | | | |\  |"
echo "  \___/_____|_| \_\\___/|_____| |_|   |_| |_| \_|"
echo "\n        - Termux OSINT & Security Framework Installer -"
echo -e "\033[0m"
echo -e "\033[95m\033[1m=====================================================\033[0m"
echo -e "\033[97m  필요한 패키지 및 라이브러리를 설치합니다.\033[0m"
echo -e "\033[95m\033[1m=====================================================\033[0m\n"

# 1. Termux 기본 패키지 업데이트 및 업그레이드
echo -e "\033[93m[+] Termux 기본 패키지 업데이트 및 업그레이드...\033[0m"
pkg update -y && pkg upgrade -y

# 2. 필요한 시스템 도구 설치
echo -e "\033[93m[+] 필요한 시스템 도구 설치 (git, python, whois, traceroute)...\033[0m"
pkg install git python whois traceroute -y

# 3. Python 라이브러리 설치
echo -e "\033[93m[+] 필요한 Python 라이브러리 설치 (requests, beautifulsoup4, Pillow, ipaddress, scapy)...\033[0m"
pip install requests beautifulsoup4 Pillow ipaddress scapy

# Scapy 설치 시 경고 메시지 처리 (루트 권한 관련)
echo -e "\033[92m\n[!] Scapy는 일부 기능(예: ARP 스캔)에 루트 권한이 필요할 수 있습니다.\033[0m"
echo -e "\033[92m    Termux 환경에서는 제한적일 수 있으며, 개념 증명용으로 사용됩니다.\033[0m\n"

echo -e "\033[92m\033[1m[+] 모든 설치가 완료되었습니다!\033[0m"
echo -e "\033[97m이제 'python osint_tool.py' 명령어로 도구를 실행할 수 있습니다.\033[0m"
echo -e "\033[97m도움말을 보려면 도구 실행 후 '11'을 선택하세요.\033[0m\n"
