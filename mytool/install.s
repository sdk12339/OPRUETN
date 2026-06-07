#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Termux OSINT & Security Framework v17.0 - Ghost-Mirror Edition (Final)
# =============================================================================

RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CYAN='\033[96m'
BOLD='\033[1m'
RESET='\033[0m'

echo -e "${CYAN}${BOLD}[*] v18.0 Ghost-Mirror 패키지 및 터널링 엔진 설치 시작...${RESET}"

# Termux 여부 확인
IS_TERMUX=false
if [ -d "/data/data/com.termux" ]; then IS_TERMUX=true; fi

# 1. 필수 시스템 패키지 설치 (SSH -> openssh 수정)
SYSTEM_PACKAGES=("python" "python-pip" "curl" "wget" "git" "whois" "nmap" "openssh" "dnsutils")

for pkg_name in "${SYSTEM_PACKAGES[@]}"; do
    echo -e "${YELLOW}[*] 설치 중: ${pkg_name}${RESET}"
    if $IS_TERMUX; then
        pkg install "$pkg_name" -y || pkg install "openssh" -y
    else
        sudo apt install "$pkg_name" -y
    fi
done

# 2. Cloudflared 설치 로직 강화
echo -e "${CYAN}${BOLD}[*] Cloudflared 터널링 엔진 설치/확인 중...${RESET}"
ARCH=$(uname -m)
if [[ "$ARCH" == "aarch64" || "$ARCH" == "arm64" ]]; then
    URL="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64"
elif [[ "$ARCH" == "x86_64" ]]; then
    URL="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
else
    URL="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm"
fi

# 설치 경로 설정
if $IS_TERMUX; then BIN_PATH="$PREFIX/bin/cloudflared"; else BIN_PATH="/usr/local/bin/cloudflared"; fi

echo -e "${YELLOW}[*] Cloudflared 다운로드: ${URL}${RESET}"
if $IS_TERMUX; then
    curl -L "$URL" -o "$BIN_PATH" && chmod +x "$BIN_PATH"
else
    sudo curl -L "$URL" -o "$BIN_PATH" && sudo chmod +x "$BIN_PATH"
fi

if [ -f "$BIN_PATH" ]; then
    echo -e "${GREEN}[+] Cloudflared 설치 성공: $BIN_PATH${RESET}"
else
    echo -e "${RED}[-] Cloudflared 설치 실패! 네트워크 연결을 확인하세요.${RESET}"
fi

# 3. Python 라이브러리
pip install requests beautifulsoup4 colorama dnspython python-whois --upgrade

echo -e "${GREEN}${BOLD}[!] 모든 설정이 완료되었습니다. python osint_tool_v17.py 를 실행하세요.${RESET}"
