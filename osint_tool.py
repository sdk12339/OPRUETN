"""
Termux OSINT Tool
도메인 또는 IP 주소에 대한 공개 출처 정보(OSINT)를 수집하는 도구입니다.

기능:
- WHOIS 정보 조회
- DNS 정보 조회 (도메인 -> IP)
- IP 지리적 위치 조회
- 통합 OSINT 스캔

사용법:
Termux에서 `python osint_tool.py`를 실행한 후 메뉴를 통해 원하는 기능을 선택합니다.
"""

import os
import socket
import requests
import json
import subprocess
import sys
import time

# ANSI 색상 코드 정의
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def print_banner():
    clear_screen()
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
   ___ ____  ____  _   _ _____ _____ _   _ 
  / _ \___ \|  _ \| | | | ____|_   _| \ | |
 | | | |__) | |_) | | | |  _|   | | |  \| |
 | |_| / __/|  _ <| |_| | |___  | | | |\  |
  \___/_____|_| \_\\___/|_____| |_| |_| \_|

{Colors.YELLOW}        - Termux OSINT Tool -{Colors.RESET}
"""
    print(banner)
    print(f"{Colors.MAGENTA}{Colors.BOLD}====================================================={Colors.RESET}")
    print(f"{Colors.WHITE}  도메인 또는 IP 주소에 대한 공개 정보를 수집합니다.{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}====================================================={Colors.RESET}\n")

def get_whois_info(target):
    try:
        result = subprocess.run(['whois', target], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"WHOIS 정보 조회 실패: {e.stderr}"
    except FileNotFoundError:
        return "WHOIS 명령어를 찾을 수 없습니다. 'pkg install whois'로 설치해주세요."
    except Exception as e:
        return f"WHOIS 정보 조회 실패: {e}"

def get_dns_info(target):
    try:
        # IP 주소인 경우 바로 반환
        if is_ip_address(target):
            return {'IP Address': target}
        
        # 도메인인 경우 IP 주소 조회
        ip_address = socket.gethostbyname(target)
        return {'Domain': target, 'IP Address': ip_address}
    except socket.gaierror:
        return f"DNS 정보 조회 실패: {target}에 대한 IP 주소를 찾을 수 없습니다."
    except Exception as e:
        return f"DNS 정보 조회 실패: {e}"

def get_ip_geolocation(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        response.raise_for_status() # HTTP 오류 발생 시 예외 발생
        data = response.json()
        if data and data.get('status') == 'success':
            return {
                'IP': data.get('query'),
                'Country': data.get('country'),
                'City': data.get('city'),
                'RegionName': data.get('regionName'),
                'ISP': data.get('isp'),
                'Org': data.get('org'),
                'Lat': data.get('lat'),
                'Lon': data.get('lon')
            }
        else:
            return f"IP 위치 정보 조회 실패: {data.get('message', '알 수 없는 오류')}"
    except requests.exceptions.RequestException as e:
        return f"IP 위치 정보 조회 실패 (네트워크 오류): {e}"
    except json.JSONDecodeError:
        return "IP 위치 정보 조회 실패 (JSON 디코딩 오류)"
    except Exception as e:
        return f"IP 위치 정보 조회 실패: {e}"

def is_ip_address(target):
    try:
        socket.inet_aton(target)
        return True
    except socket.error:
        return False

def print_result(title, result):
    print(f"{Colors.BLUE}\n[+] {title}:{Colors.RESET}")
    if isinstance(result, dict):
        for key, value in result.items():
            print(f"  {key}: {value}")
    else:
        print(f"  {result}")

def run_whois_scan(target):
    print(f"{Colors.GREEN}[+] 대상: {target}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}=============================={Colors.RESET}")
    print_result("WHOIS 정보", get_whois_info(target))
    print(f"{Colors.MAGENTA}{Colors.BOLD}=============================={Colors.RESET}")

def run_dns_scan(target):
    print(f"{Colors.GREEN}[+] 대상: {target}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}=============================={Colors.RESET}")
    dns_info = get_dns_info(target)
    print_result("DNS 정보", dns_info)
    print(f"{Colors.MAGENTA}{Colors.BOLD}=============================={Colors.RESET}")

def run_geolocation_scan(target):
    print(f"{Colors.GREEN}[+] 대상: {target}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}=============================={Colors.RESET}")
    ip_for_geo = target if is_ip_address(target) else get_dns_info(target).get('IP Address')
    if ip_for_geo:
        print_result("IP 위치 정보", get_ip_geolocation(ip_for_geo))
    else:
        print("\n[+] IP 위치 정보를 조회할 수 없습니다 (유효한 IP 주소 없음).")
    print(f"{Colors.MAGENTA}{Colors.BOLD}=============================={Colors.RESET}")

def run_full_osint_scan(target):
    print(f"{Colors.GREEN}[+] 대상: {target}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}=============================={Colors.RESET}")

    # WHOIS 정보
    print_result("WHOIS 정보", get_whois_info(target))

    # DNS 정보
    dns_info = get_dns_info(target)
    print_result("DNS 정보", dns_info)
    ip_for_geo = dns_info.get('IP Address')

    # IP 위치 정보 (IP 주소가 있는 경우에만)
    if ip_for_geo:
        print_result("IP 위치 정보", get_ip_geolocation(ip_for_geo))
    else:
        print("\n[+] IP 위치 정보를 조회할 수 없습니다 (유효한 IP 주소 없음).")

    print(f"{Colors.MAGENTA}{Colors.BOLD}=============================={Colors.RESET}")

def display_main_menu():
    print_banner()
    print(f"{Colors.YELLOW}{Colors.BOLD}메인 메뉴:{Colors.RESET}")
    print(f"{Colors.GREEN}  1. 통합 OSINT 스캔 (WHOIS, DNS, IP 위치){Colors.RESET}")
    print(f"{Colors.GREEN}  2. WHOIS 정보 조회{Colors.RESET}")
    print(f"{Colors.GREEN}  3. DNS 정보 조회 (도메인 -> IP){Colors.RESET}")
    print(f"{Colors.GREEN}  4. IP 지리적 위치 조회{Colors.RESET}")
    print(f"{Colors.GREEN}  5. 도움말{Colors.RESET}")
    print(f"{Colors.RED}  0. 종료{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}====================================================={Colors.RESET}")

def show_help():
    clear_screen()
    print_banner()
    print(f"{Colors.YELLOW}{Colors.BOLD}도움말:{Colors.RESET}\n")
    print(f"{Colors.WHITE}이 도구는 도메인 또는 IP 주소에 대한 공개 정보를 수집합니다.\n")
    print(f"{Colors.WHITE}각 메뉴 항목은 특정 유형의 정보를 조회하는 기능을 제공합니다.\n")
    print(f"{Colors.WHITE}  - 통합 OSINT 스캔: WHOIS, DNS, IP 위치 정보를 모두 조회합니다.\n")
    print(f"{Colors.WHITE}  - WHOIS 정보 조회: 도메인 등록 정보를 조회합니다.\n")
    print(f"{Colors.WHITE}  - DNS 정보 조회: 도메인에 연결된 IP 주소를 확인합니다.\n")
    print(f"{Colors.WHITE}  - IP 지리적 위치 조회: IP 주소의 지리적 위치를 파악합니다.\n")
    print(f"{Colors.WHITE}사용 방법:\n")
    print(f"{Colors.WHITE}  1. 메인 메뉴에서 원하는 기능의 번호를 입력합니다.\n")
    print(f"{Colors.WHITE}  2. 프롬프트에 조회할 도메인(예: google.com) 또는 IP 주소(예: 8.8.8.8)를 입력합니다.\n")
    print(f"{Colors.WHITE}  3. 결과가 화면에 표시됩니다.\n")
    print(f"{Colors.WHITE}  4. '0'을 입력하여 도구를 종료할 수 있습니다.\n")
    print(f"{Colors.RED}주의: 이 도구는 교육 및 보안 학습 목적으로 제작되었습니다. 타인의 동의 없이 무단으로 정보를 수집하거나 악용하는 행위는 법적 문제를 야기할 수 있습니다. 항상 윤리적이고 합법적인 범위 내에서 사용하십시오.{Colors.RESET}\n")
    input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")

def main():
    while True:
        display_main_menu()
        choice = input(f"{Colors.YELLOW}선택하세요 (0-5): {Colors.RESET}").strip()

        if choice == '1':
            target = input(f"{Colors.CYAN}조회할 도메인 또는 IP 주소를 입력하세요: {Colors.RESET}").strip()
            if target:
                run_full_osint_scan(target)
            else:
                print(f"{Colors.RED}유효한 대상을 입력해주세요.{Colors.RESET}")
            input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")
        elif choice == '2':
            target = input(f"{Colors.CYAN}WHOIS 정보를 조회할 도메인 또는 IP 주소를 입력하세요: {Colors.RESET}").strip()
            if target:
                run_whois_scan(target)
            else:
                print(f"{Colors.RED}유효한 대상을 입력해주세요.{Colors.RESET}")
            input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")
        elif choice == '3':
            target = input(f"{Colors.CYAN}DNS 정보를 조회할 도메인 또는 IP 주소를 입력하세요: {Colors.RESET}").strip()
            if target:
                run_dns_scan(target)
            else:
                print(f"{Colors.RED}유효한 대상을 입력해주세요.{Colors.RESET}")
            input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")
        elif choice == '4':
            target = input(f"{Colors.CYAN}IP 위치를 조회할 도메인 또는 IP 주소를 입력하세요: {Colors.RESET}").strip()
            if target:
                run_geolocation_scan(target)
            else:
                print(f"{Colors.RED}유효한 대상을 입력해주세요.{Colors.RESET}")
            input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")
        elif choice == '5':
            show_help()
        elif choice == '0':
            print(f"{Colors.RED}도구를 종료합니다. 안녕히 계세요!{Colors.RESET}")
            sys.exit(0)
        else:
            print(f"{Colors.RED}잘못된 선택입니다. 다시 시도해주세요.{Colors.RESET}")
            input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")

if __name__ == "__main__":
    main()

