
import argparse
import os

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


import socket
import requests
import json
import subprocess

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

def main():
    print_banner()

    parser = argparse.ArgumentParser(description="OSINT 정보 수집 도구 (도메인/IP)")
    parser.add_argument("target", help="조회할 도메인 또는 IP 주소")
    args = parser.parse_args()

    target = args.target

    print(f"{Colors.GREEN}[+] 대상: {target}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}=============================={Colors.RESET}")

    # WHOIS 정보
    print(f"{Colors.BLUE}\n[+] WHOIS 정보:{Colors.RESET}")
    whois_info = get_whois_info(target)
    if isinstance(whois_info, dict):
        for key, value in whois_info.items():
            print(f"  {key}: {value}")
    else:
        print(f"  {whois_info}")

    # DNS 정보
    print(f"{Colors.BLUE}\n[+] DNS 정보:{Colors.RESET}")
    dns_info = get_dns_info(target)
    if isinstance(dns_info, dict):
        for key, value in dns_info.items():
            print(f"  {key}: {value}")
        ip_for_geo = dns_info.get('IP Address')
    else:
        print(f"  {dns_info}")
        ip_for_geo = target if is_ip_address(target) else None

    # IP 위치 정보 (IP 주소가 있는 경우에만)
    if ip_for_geo:
        print(f"{Colors.BLUE}\n[+] IP 위치 정보:{Colors.RESET}")
        geolocation_info = get_ip_geolocation(ip_for_geo)
        if isinstance(geolocation_info, dict):
            for key, value in geolocation_info.items():
                print(f"  {key}: {value}")
        else:
            print(f"  {geolocation_info}")
    else:
        print("\n[+] IP 위치 정보를 조회할 수 없습니다 (유효한 IP 주소 없음).")

    print(f"{Colors.MAGENTA}{Colors.BOLD}=============================={Colors.RESET}")

if __name__ == "__main__":
    main()
