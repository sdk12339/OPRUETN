#!/bin/bash
# =============================================================================
# v18.0 All-In-One Hacking Framework - Termux Ultimate Fix
# =============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

clear
echo -e "${CYAN}${BOLD}=====================================================${RESET}"
echo -e "${CYAN}${BOLD}   v18.0 All-In-One Framework - Termux Ultimate Fix${RESET}"
echo -e "${CYAN}${BOLD}=====================================================${RESET}"

# Termux 여부 확인 및 홈 디렉토리 설정
IS_TERMUX=false
if [ -d "/data/data/com.termux" ]; then 
    IS_TERMUX=true
    BASE_DIR="$HOME"
else 
    BASE_DIR="/home/ubuntu"
fi

echo -e "${YELLOW}[*] 시스템 패키지 업데이트 및 필수 도구 설치 중...${RESET}"
if $IS_TERMUX; then
    pkg update -y && pkg upgrade -y
    # 패키지명이 다를 수 있으므로 개별적으로 시도하며 에러 무시
    pkg install -y python git php curl openssh wget nmap dnsutils 2>/dev/null
    pkg install -y python-cryptography 2>/dev/null
    pkg install -y python-openssl 2>/dev/null || pkg install -y python-pyopenssl 2>/dev/null
else
    sudo apt update -y && sudo apt upgrade -y
    sudo apt install -y python3 python3-pip git php curl openssh-client wget nmap dnsutils
fi

echo -e "${YELLOW}[*] 파이썬 라이브러리 설치 중...${RESET}"
# pkg로 설치되지 않은 나머지 라이브러리들을 pip로 설치
# cryptography 에러를 피하기 위해 이미 설치된 것은 건너뜀
pip3 install requests beautifulsoup4 colorama whois dnspython ipwhois scapy pyOpenSSL --break-system-packages 2>/dev/null || pip3 install requests beautifulsoup4 colorama whois dnspython ipwhois scapy pyOpenSSL

echo -e "${YELLOW}[*] 외부 도구 저장소 구성 중 (경로: $BASE_DIR)...${RESET}"
# AllHackingTools
if [ ! -d "$BASE_DIR/AllHackingTools" ]; then
    echo -e "${YELLOW}[*] AllHackingTools 클론 중...${RESET}"
    git clone https://github.com/mishakorzik/AllHackingTools.git "$BASE_DIR/AllHackingTools"
else
    echo -e "${GREEN}[+] AllHackingTools 이미 존재함.${RESET}"
fi

# zphisher
if [ ! -d "$BASE_DIR/zphisher" ]; then
    echo -e "${YELLOW}[*] zphisher 클론 중...${RESET}"
    git clone https://github.com/htr-tech/zphisher.git "$BASE_DIR/zphisher"
else
    echo -e "${GREEN}[+] zphisher 이미 존재함.${RESET}"
fi

# Cloudflared 설치
echo -e "${CYAN}${BOLD}[*] Cloudflared 터널링 엔진 설치 확인...${RESET}"
ARCH=$(uname -m)
if [[ "$ARCH" == "aarch64" || "$ARCH" == "arm64" ]]; then
    URL="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64"
elif [[ "$ARCH" == "x86_64" ]]; then
    URL="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
else
    URL="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm"
fi

if $IS_TERMUX; then BIN_PATH="$PREFIX/bin/cloudflared"; else BIN_PATH="/usr/local/bin/cloudflared"; fi

if [ ! -f "$BIN_PATH" ]; then
    echo -e "${YELLOW}[*] Cloudflared 다운로드 중...${RESET}"
    if $IS_TERMUX; then
        curl -L "$URL" -o "$BIN_PATH" && chmod +x "$BIN_PATH"
    else
        sudo curl -L "$URL" -o "$BIN_PATH" && sudo chmod +x "$BIN_PATH"
    fi
fi

echo -e "${GREEN}${BOLD}[+] 모든 설치가 완료되었습니다!${RESET}"
echo -e "${CYAN}${BOLD}명령어: python osint_tool.py${RESET}"
