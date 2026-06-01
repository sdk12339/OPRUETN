#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Termux OSINT & Security Framework v4.0 - 통합 설치 스크립트
# =============================================================================
# 이 스크립트는 Termux 환경에서 OSINT 툴 실행에 필요한 모든 패키지와
# Python 라이브러리를 자동으로 설치합니다.
# =============================================================================

# ANSI 색상 코드
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CYAN='\033[96m'
BOLD='\033[1m'
RESET='\033[0m'

# 배너 출력
echo ""
echo -e "${CYAN}${BOLD}"
echo "  ___  ____  ___ _   _ _____   _____ ___   ___  _     "
echo " / _ \/ ___||_ _| \ | |_   _| |_   _/ _ \ / _ \| |    "
echo "| | | \___ \ | ||  \| | | |     | || | | | | | | |    "
echo "| |_| |___) || || |\  | | |     | || |_| | |_| | |___ "
echo " \___/|____/___|_| \_| |_|     |_| \___/ \___/|_____|"
echo ""
echo -e "${YELLOW}  Termux OSINT & Security Framework v4.0 - 자동 설치 스크립트${RESET}"
echo -e "${CYAN}${BOLD}======================================================${RESET}"
echo ""

# 운영 환경 확인 (Termux 여부)
if [ ! -d "/data/data/com.termux" ]; then
    echo -e "${YELLOW}[!] Termux 환경이 아닌 것 같습니다. 일반 Linux 환경으로 설치를 진행합니다.${RESET}"
    IS_TERMUX=false
else
    echo -e "${GREEN}[+] Termux 환경 감지됨.${RESET}"
    IS_TERMUX=true
fi

# 오류 발생 시 중단 (선택적)
set -e

# =============================================================================
# 1. 시스템 패키지 업데이트
# =============================================================================
echo ""
echo -e "${CYAN}${BOLD}[1/4] 시스템 패키지 업데이트 중...${RESET}"
echo -e "${YELLOW}[*] 패키지 목록을 업데이트합니다...${RESET}"

if $IS_TERMUX; then
    pkg update -y && pkg upgrade -y
else
    sudo apt update -y && sudo apt upgrade -y
fi

echo -e "${GREEN}[+] 시스템 패키지 업데이트 완료.${RESET}"

# =============================================================================
# 2. 필수 시스템 패키지 설치
# =============================================================================
echo ""
echo -e "${CYAN}${BOLD}[2/4] 필수 시스템 패키지 설치 중...${RESET}"

SYSTEM_PACKAGES=(
    "python"
    "python-pip"
    "curl"
    "wget"
    "git"
    "whois"
    "traceroute"
    "nmap"
    "openssl"
    "net-tools"
    "dnsutils"
)

for pkg_name in "${SYSTEM_PACKAGES[@]}"; do
    echo -e "${YELLOW}[*] 설치 중: ${pkg_name}${RESET}"
    if $IS_TERMUX; then
        pkg install "$pkg_name" -y 2>/dev/null || echo -e "${RED}[-] ${pkg_name} 설치 실패 (건너뜀)${RESET}"
    else
        sudo apt install "$pkg_name" -y 2>/dev/null || echo -e "${RED}[-] ${pkg_name} 설치 실패 (건너뜀)${RESET}"
    fi
done

echo -e "${GREEN}[+] 시스템 패키지 설치 완료.${RESET}"

# =============================================================================
# 3. Python 라이브러리 설치
# =============================================================================
echo ""
echo -e "${CYAN}${BOLD}[3/4] Python 라이브러리 설치 중...${RESET}"

# pip 최신 버전으로 업그레이드
echo -e "${YELLOW}[*] pip 업그레이드 중...${RESET}"
pip install --upgrade pip 2>/dev/null || pip3 install --upgrade pip 2>/dev/null

PYTHON_PACKAGES=(
    "requests"
    "beautifulsoup4"
    "lxml"
    "colorama"
    "dnspython"
    "python-whois"
    "urllib3"
    "certifi"
)

for py_pkg in "${PYTHON_PACKAGES[@]}"; do
    echo -e "${YELLOW}[*] pip 설치 중: ${py_pkg}${RESET}"
    pip install "$py_pkg" 2>/dev/null || pip3 install "$py_pkg" 2>/dev/null || echo -e "${RED}[-] ${py_pkg} 설치 실패 (건너뜀)${RESET}"
done

echo -e "${GREEN}[+] Python 라이브러리 설치 완료.${RESET}"

# =============================================================================
# 4. 설치 검증 및 실행 권한 부여
# =============================================================================
echo ""
echo -e "${CYAN}${BOLD}[4/4] 설치 검증 및 실행 권한 설정 중...${RESET}"

# Python 버전 확인
PYTHON_VERSION=$(python --version 2>&1 || python3 --version 2>&1)
echo -e "${GREEN}[+] Python 버전: ${PYTHON_VERSION}${RESET}"

# 필수 모듈 임포트 테스트
echo -e "${YELLOW}[*] 핵심 Python 모듈 임포트 테스트 중...${RESET}"
python -c "import requests; print('[+] requests: OK')" 2>/dev/null || \
    python3 -c "import requests; print('[+] requests: OK')" 2>/dev/null || \
    echo -e "${RED}[-] requests 모듈 임포트 실패${RESET}"

python -c "from bs4 import BeautifulSoup; print('[+] beautifulsoup4: OK')" 2>/dev/null || \
    python3 -c "from bs4 import BeautifulSoup; print('[+] beautifulsoup4: OK')" 2>/dev/null || \
    echo -e "${RED}[-] beautifulsoup4 모듈 임포트 실패${RESET}"

# 스크립트 실행 권한 부여
if [ -f "osint_tool_v4.py" ]; then
    chmod +x osint_tool_v4.py
    echo -e "${GREEN}[+] osint_tool_v4.py 실행 권한 설정 완료.${RESET}"
fi

# =============================================================================
# 설치 완료 안내
# =============================================================================
echo ""
echo -e "${CYAN}${BOLD}======================================================"
echo -e "  설치가 완료되었습니다! (V4.0 Advanced)"
echo -e "======================================================${RESET}"
echo ""
echo -e "${GREEN}[+] 실행 방법:${RESET}"
echo -e "    ${YELLOW}python osint_tool_v4.py${RESET}"
echo -e "    또는"
echo -e "    ${YELLOW}python3 osint_tool_v4.py${RESET}"
echo ""
echo -e "${YELLOW}[!] V4.0 주요 업데이트:${RESET}"
echo -e "    - [NEW] 이메일 / 전화번호 검증 모듈"
echo -e "    - [NEW] 소셜 미디어 사용자명(Username) 검색 (30+ 플랫폼)"
echo -e "    - [NEW] 웹사이트 종합 스캐닝 (WHOIS, 서브도메인, 기술스택 통합)"
echo -e "    - 기존 v3.0의 모든 페이로드 라이브러리 및 스캔 기능 포함"
echo ""
echo -e "${RED}[!] 주의사항: 이 도구는 교육 및 보안 학습 목적으로만 사용하십시오."
echo -e "    인가되지 않은 시스템에 대한 공격은 법적 처벌을 받을 수 있습니다.${RESET}"
echo ""
