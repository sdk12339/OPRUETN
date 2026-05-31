"""
Termux OSINT Tool - Comprehensive Security Framework
도메인 또는 IP 주소에 대한 광범위한 공개 출처 정보(OSINT) 및 보안 분석을 수행하는 도구입니다.

기능:
- WHOIS 정보 조회
- DNS 정보 조회 (도메인 -> IP)
- IP 지리적 위치 조회
- 웹 기술 스택 분석
- 포트 스캔 (기본 및 사용자 지정)
- 서브도메인 스캔
- 웹 취약점 분석 (WAF, 보안 헤더, Clickjacking, Open Redirect, CORS, Robots.txt, Sitemap)
- 심층 정보 수집 (이메일 수집, CMS 상세 분석, SSL 인증서, Reverse IP, Shared Hosting, Google Dorking)
- 네트워크 보안 (서비스 배너 그래빙, FTP 익명 로그인, Traceroute, Ping Sweep, Latency)
- 암호학 및 유틸리티 (해시 생성/식별, Base64/URL 인코딩/디코딩, 패스워드 생성, IP 계산기, Epoch 변환)
- 통합 스캔 및 HTML/JSON/Text 보고서 생성

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
import re
import hashlib
import base64
import urllib.parse
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
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
   ___ ____  ____  _   _ _____ _____ _   _ 
  / _ \___ \|  _ \| | | | ____|_   _| \ | |
 | | | |__) | |_) | | | |  _|   | | |  \| |
 | |_| / __/|  _ <| |_| | |___  | | | |\  |
  \___/_____|_| \_\\___/|_____| |_| |_| \_|

{Colors.YELLOW}        - Termux OSINT & Security Framework -{Colors.RESET}
"""
    print(banner)
    print(f"{Colors.MAGENTA}{Colors.BOLD}====================================================={Colors.RESET}")
    print(f"{Colors.WHITE}  도메인/IP 정보 수집 및 다양한 보안 분석을 수행합니다.{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}====================================================={Colors.RESET}\n")

def is_ip_address(target):
    try:
        socket.inet_aton(target)
        return True
    except: return False

def print_result(title, result, color=Colors.BLUE):
    print(f"{color}\n[+] {title}:{Colors.RESET}")
    if isinstance(result, dict):
        for key, value in result.items():
            print(f"  {key}: {value}")
    elif isinstance(result, list):
        for item in result:
            print(f"  - {item}")
    else:
        print(f"  {result}")

# --- 1. Information Gathering Functions (정보 수집 기능) ---

def get_whois_info(target):
    try:
        result = subprocess.run(["whois", target], capture_output=True, text=True, check=True, timeout=10)
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        return f"WHOIS 정보 조회 실패: {e}"
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
    common = ["www", "blog", "mail", "ftp", "dev", "admin", "api", "test", "webmail", "cpanel", "ns1", "ns2"]
    found = []
    for sub in common:
        try:
            target = f"{sub}.{domain}"
            ip = socket.gethostbyname(target)
            found.append(f"{target} ({ip})")
        except: pass
    return {"Found Subdomains": found} if found else "서브도메인 없음"

def email_harvester(url):
    emails = set()
    try:
        response = requests.get(url, timeout=10)
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
            s.connect((host, 443))
            cert = s.getpeercert()
            return cert
    except Exception as e:
        return f"SSL 인증서 정보 조회 실패: {e}"

def reverse_ip_lookup(ip_address):
    try:
        # This is a simplified example. Real reverse IP lookup often requires external services.
        # For educational purposes, we'll just try to resolve the IP back to a hostname.
        hostname = socket.gethostbyaddr(ip_address)[0]
        return {"Hostname": hostname}
    except socket.herror:
        return "역방향 IP 조회 실패: 호스트 이름을 찾을 수 없습니다."
    except Exception as e:
        return f"역방향 IP 조회 실패: {e}"

def google_dork_generator(domain):
    dorks = [
        f"site:{domain} intitle:\"index of\"",
        f"site:{domain} inurl:admin",
        f"site:{domain} inurl:login",
        f"site:{domain} filetype:pdf confidential",
        f"site:{domain} intext:\"password\"",
        f"site:{domain} ext:log | ext:txt",
    ]
    return {"Google Dorks": dorks}

# --- 2. Web Analysis Functions (웹 분석 기능) ---

def web_tech_detector(target_url):
    tech_info = {}
    try:
        if not target_url.startswith("http"): target_url = "http://" + target_url
        response = requests.get(target_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        headers = response.headers
        if "Server" in headers: tech_info["Server"] = headers["Server"]
        if "X-Powered-By" in headers: tech_info["X-Powered-By"] = headers["X-Powered-By"]
        
        for meta in soup.find_all("meta"):
            if meta.get("name") == "generator": tech_info["Generator"] = meta.get("content")
            
        scripts = soup.find_all("script", src=True)
        for script in scripts:
            src = script["src"].lower()
            if "jquery" in src: tech_info["JS Library"] = "jQuery"
            elif "react" in src: tech_info["JS Framework"] = "React"
            elif "vue" in src: tech_info["JS Framework"] = "Vue.js"
            
        if soup.find(lambda tag: "wp-content" in str(tag) or "wp-json" in str(tag)): tech_info["CMS"] = "WordPress"
        elif soup.find(lambda tag: "joomla" in str(tag)): tech_info["CMS"] = "Joomla"
        elif soup.find(lambda tag: "drupal" in str(tag)): tech_info["CMS"] = "Drupal"
        
        return tech_info if tech_info else "웹 기술 정보를 찾을 수 없습니다."
    except Exception as e:
        return f"웹 기술 분석 실패: {e}"

def waf_detector(url):
    try:
        response = requests.get(url, timeout=5)
        waf_signatures = {
            "Cloudflare": ["cloudflare-nginx", "__cfduid"],
            "Incapsula": ["incapsula", "X-CDN"],
            "Sucuri": ["sucuri/cloudproxy"],
            "Akamai": ["akamai"],
            "ModSecurity": ["mod_security", "Mod_Security_Status"],
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
        response = requests.get(url, timeout=5)
        headers = response.headers
        security_headers = [
            "Strict-Transport-Security", "X-Frame-Options", "X-XSS-Protection",
            "Content-Security-Policy", "X-Content-Type-Options", "Referrer-Policy"
        ]
        for header in security_headers:
            headers_info[header] = headers.get(header, "Not Set")
        return headers_info
    except Exception as e:
        return f"보안 헤더 분석 실패: {e}"

def clickjacking_test(url):
    try:
        response = requests.get(url, timeout=5)
        x_frame_options = response.headers.get("X-Frame-Options", "Not Set").lower()
        if "deny" in x_frame_options or "sameorigin" in x_frame_options:
            return "Clickjacking 방어: X-Frame-Options 설정됨."
        else:
            return "Clickjacking 취약 가능: X-Frame-Options 설정되지 않음 또는 취약."
    except Exception as e:
        return f"Clickjacking 테스트 실패: {e}"

def open_redirect_check(url, test_payload="//google.com"):
    try:
        test_url = f"{url}?redirect={test_payload}"
        response = requests.get(test_url, allow_redirects=False, timeout=5)
        if response.status_code == 302 and test_payload in response.headers.get("Location", ""):
            return f"Open Redirect 취약 가능: {response.headers.get('Location')}"
        else:
            return "Open Redirect 취약점 없음 (또는 감지 실패)."
    except Exception as e:
        return f"Open Redirect 테스트 실패: {e}"

def cors_misconfiguration_check(url):
    try:
        headers = {"Origin": "http://evil.com"}
        response = requests.get(url, headers=headers, timeout=5)
        acao = response.headers.get("Access-Control-Allow-Origin")
        if acao == "*" or "http://evil.com" in str(acao):
            return f"CORS 취약 가능: Access-Control-Allow-Origin: {acao}"
        else:
            return "CORS 취약점 없음 (또는 감지 실패)."
    except Exception as e:
        return f"CORS 분석 실패: {e}"

def robots_txt_analyzer(url):
    try:
        if not url.startswith("http"): url = "http://" + url
        robots_url = urllib.parse.urljoin(url, "/robots.txt")
        response = requests.get(robots_url, timeout=5)
        if response.status_code == 200:
            disallowed = re.findall(r"Disallow: (.*)", response.text)
            return {"Disallowed Paths": disallowed} if disallowed else "robots.txt에 Disallow 규칙 없음."
        else:
            return "robots.txt 파일을 찾을 수 없습니다."
    except Exception as e:
        return f"robots.txt 분석 실패: {e}"

def sitemap_xml_finder(url):
    try:
        if not url.startswith("http"): url = "http://" + url
        sitemap_url = urllib.parse.urljoin(url, "/sitemap.xml")
        response = requests.get(sitemap_url, timeout=5)
        if response.status_code == 200:
            return {"Sitemap URL": sitemap_url}
        else:
            return "sitemap.xml 파일을 찾을 수 없습니다."
    except Exception as e:
        return f"sitemap.xml 찾기 실패: {e}"

# --- 3. Network Functions (네트워크 기능) ---

def port_scanner(target_host, ports):
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        if sock.connect_ex((target_host, port)) == 0:
            open_ports.append(port)
        sock.close()
    return {"Open Ports": open_ports} if open_ports else "열린 포트 없음"

def service_banner_grabbing(target_host, ports):
    banners = {}
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((target_host, port))
            banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
            banners[port] = banner.split("\n")[0] if banner else "No banner received"
            sock.close()
        except Exception as e:
            banners[port] = f"Error: {e}"
    return banners if banners else "배너를 찾을 수 없습니다."

def ftp_anonymous_login_check(target_host):
    try:
        from ftplib import FTP
        ftp = FTP(target_host, timeout=5)
        ftp.login("anonymous", "anonymous")
        ftp.quit()
        return "FTP 익명 로그인 가능!"
    except Exception as e:
        return f"FTP 익명 로그인 불가 또는 오류: {e}"

def traceroute(target):
    try:
        # Termux 환경에서는 `traceroute` 명령어가 필요할 수 있습니다.
        # pkg install traceroute -y
        result = subprocess.run(["traceroute", target], capture_output=True, text=True, timeout=30)
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        return f"Traceroute 실패: {e}"
    except Exception as e:
        return f"Traceroute 실패: {e}"

def ping_sweep(ip_range_start, ip_range_end):
    live_hosts = []
    # Simplified for demonstration. Real ping sweep involves more robust parsing.
    for i in range(int(ip_range_start.split(".")[-1]), int(ip_range_end.split(".")[-1]) + 1):
        ip = ".".join(ip_range_start.split(".")[:-1]) + f".{i}"
        try:
            result = subprocess.run(["ping", "-c", "1", "-W", "1", ip], capture_output=True, text=True, timeout=2)
            if "1 received" in result.stdout:
                live_hosts.append(ip)
        except Exception: pass
    return {"Live Hosts": live_hosts} if live_hosts else "활성 호스트 없음"

def network_latency_check(target):
    try:
        result = subprocess.run(["ping", "-c", "4", target], capture_output=True, text=True, timeout=10)
        match = re.search(r"min/avg/max/mdev = (\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+) ms", result.stdout)
        if match:
            return {"Min Latency": f"{match.group(1)} ms", "Avg Latency": f"{match.group(2)} ms", "Max Latency": f"{match.group(3)} ms"}
        else:
            return "지연 시간 측정 실패."
    except Exception as e:
        return f"지연 시간 측정 실패: {e}"

# --- 4. Cryptography & Utilities Functions (암호학 및 유틸리티 기능) ---

def hash_generator(text):
    return {
        "MD5": hashlib.md5(text.encode()).hexdigest(),
        "SHA1": hashlib.sha1(text.encode()).hexdigest(),
        "SHA256": hashlib.sha256(text.encode()).hexdigest()
    }

def hash_identifier(hash_value):
    if re.match(r"^[a-f0-9]{32}$", hash_value):
        return "MD5"
    elif re.match(r"^[a-f0-9]{40}$", hash_value):
        return "SHA1"
    elif re.match(r"^[a-f0-9]{64}$", hash_value):
        return "SHA256"
    elif re.match(r"^[a-f0-9]{128}$", hash_value):
        return "SHA512"
    else:
        return "알 수 없는 해시 유형"

def base64_encode_decode(text, mode="encode"):
    if mode == "encode":
        return base64.b64encode(text.encode()).decode()
    elif mode == "decode":
        try:
            return base64.b64decode(text.encode()).decode()
        except: return "디코딩 실패"
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
    if include_symbols: chars += string.punctuation
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

# --- Main Scan & Report Generation ---

def generate_html_report(target, data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"report_{target.replace('.', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
    
    # 웹 기술 정보를 사진처럼 시각화하기 위한 데이터 가공
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

    # Helper function to safe JSON dump
    def sj(val): return json.dumps(val, indent=4)

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
            <div class="subsection"><h3>Reverse IP Lookup</h3><pre>{sj(data.get('Reverse IP Lookup', {}))}</pre></div>
            <div class="subsection"><h3>Google Dorks</h3><pre>{sj(data.get('Google Dorks', {}))}</pre></div>
        </div>

        <div class="section">
            <h2>2. Web Analysis</h2>
            <div class="subsection"><h3>Web Technology Stack</h3>{tech_html}</div>
            <div class="subsection"><h3>WAF Detection</h3><pre>{sj(data.get('WAF Detection', {}))}</pre></div>
            <div class="subsection"><h3>Security Headers</h3><pre>{sj(data.get('Security Headers', {}))}</pre></div>
            <div class="subsection"><h3>Clickjacking Test</h3><p>{data.get('Clickjacking Test', 'No data')}</p></div>
            <div class="subsection"><h3>Open Redirect Check</h3><p>{data.get('Open Redirect Check', 'No data')}</p></div>
            <div class="subsection"><h3>CORS Misconfiguration Check</h3><p>{data.get('CORS Misconfiguration', 'No data')}</p></div>
            <div class="subsection"><h3>Robots.txt Analysis</h3><pre>{sj(data.get('Robots.txt Analysis', {}))}</pre></div>
            <div class="subsection"><h3>Sitemap.xml Finder</h3><pre>{sj(data.get('Sitemap.xml Finder', {}))}</pre></div>
        </div>

        <div class="section">
            <h2>3. Network Security</h2>
            <div class="subsection"><h3>Port Scan</h3><pre>{sj(data.get('Port Scan', {}))}</pre></div>
            <div class="subsection"><h3>Service Banner Grabbing</h3><pre>{sj(data.get('Service Banners', {}))}</pre></div>
            <div class="subsection"><h3>FTP Anonymous Login Check</h3><p>{data.get('FTP Anonymous Login', 'No data')}</p></div>
            <div class="subsection"><h3>Traceroute</h3><pre>{data.get('Traceroute', 'No data')}</pre></div>
            <div class="subsection"><h3>Ping Sweep</h3><pre>{sj(data.get('Ping Sweep', {}))}</pre></div>
            <div class="subsection"><h3>Network Latency Check</h3><pre>{sj(data.get('Network Latency', {}))}</pre></div>
        </div>

        <div class="footer">Generated by Termux OSINT & Security Framework</div>
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
    
    # Information Gathering
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
        data["Reverse IP Lookup"] = reverse_ip_lookup(ip)
    else:
        data["Geolocation"] = "IP 주소를 찾을 수 없어 건너뜁니다."
        data["Reverse IP Lookup"] = "IP 주소를 찾을 수 없어 건너뜁니다."

    # Web Analysis
    print(f"{Colors.YELLOW}[2/5] 웹 분석 중...{Colors.RESET}")
    data["Web Tech"] = web_tech_detector(target)
    data["WAF Detection"] = waf_detector(target)
    data["Security Headers"] = security_headers_check(target)
    data["Clickjacking Test"] = clickjacking_test(target)
    data["Open Redirect Check"] = open_redirect_check(target)
    data["CORS Misconfiguration"] = cors_misconfiguration_check(target)
    data["Robots.txt Analysis"] = robots_txt_analyzer(target)
    data["Sitemap.xml Finder"] = sitemap_xml_finder(target)
    data["SSL Certificate Info"] = get_ssl_info(target) if not is_ip_address(target) else "N/A"

    # Network Security
    print(f"{Colors.YELLOW}[3/5] 네트워크 보안 분석 중...{Colors.RESET}")
    if ip:
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3389, 8080]
        data["Port Scan"] = port_scanner(ip, common_ports)
        data["Service Banners"] = service_banner_grabbing(ip, [21, 22, 23, 80, 443])
        data["FTP Anonymous Login"] = ftp_anonymous_login_check(ip)
        data["Traceroute"] = traceroute(ip)
        data["Ping Sweep"] = ping_sweep(ip.rsplit('.', 1)[0] + '.1', ip.rsplit('.', 1)[0] + '.254') # Example range
        data["Network Latency"] = network_latency_check(ip)
    else:
        data["Port Scan"] = "IP 주소를 찾을 수 없어 건너뜁니다."
        data["Service Banners"] = "IP 주소를 찾을 수 없어 건너뜁니다."
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
    elif scan_type == "Port Scan":
        ports_input = input(f"{Colors.CYAN}스캔할 포트 (쉼표로 구분, 예: 80,443,22): {Colors.RESET}").strip()
        ports = [int(p.strip()) for p in ports_input.split(",")] if ports_input else [80, 443]
        ip = target if is_ip_address(target) else get_dns_info(target).get("IP Address")
        result = port_scanner(ip, ports) if ip else "IP 주소를 찾을 수 없습니다."
    elif scan_type == "Banner Grabbing":
        ports_input = input(f"{Colors.CYAN}배너를 가져올 포트 (쉼표로 구분, 예: 21,22,80): {Colors.RESET}").strip()
        ports = [int(p.strip()) for p in ports_input.split(",")] if ports_input else [21, 22, 80, 443]
        ip = target if is_ip_address(target) else get_dns_info(target).get("IP Address")
        result = service_banner_grabbing(ip, ports) if ip else "IP 주소를 찾을 수 없습니다."
    elif scan_type == "FTP Anon Login":
        ip = target if is_ip_address(target) else get_dns_info(target).get("IP Address")
        result = ftp_anonymous_login_check(ip) if ip else "IP 주소를 찾을 수 없습니다."
    elif scan_type == "Traceroute":
        result = traceroute(target)
    elif scan_type == "Ping Sweep":
        ip_range_start = input(f"{Colors.CYAN}시작 IP (예: 192.168.1.1): {Colors.RESET}").strip()
        ip_range_end = input(f"{Colors.CYAN}끝 IP (예: 192.168.1.254): {Colors.RESET}").strip()
        result = ping_sweep(ip_range_start, ip_range_end)
    elif scan_type == "Latency Check":
        result = network_latency_check(target)
    
    print_result(scan_type + " 결과", result)
    print(f"{Colors.MAGENTA}{Colors.BOLD}=============================={Colors.RESET}")

def display_main_menu():
    print_banner()
    print(f"{Colors.YELLOW}{Colors.BOLD}메인 메뉴:{Colors.RESET}")
    print(f"{Colors.GREEN}  1. 종합 OSINT & 보안 스캔 (HTML 보고서 생성){Colors.RESET}")
    print(f"{Colors.GREEN}  2. 정보 수집 도구{Colors.RESET}")
    print(f"{Colors.GREEN}  3. 웹 분석 도구{Colors.RESET}")
    print(f"{Colors.GREEN}  4. 네트워크 보안 도구{Colors.RESET}")
    print(f"{Colors.GREEN}  5. 암호학 & 유틸리티{Colors.RESET}")
    print(f"{Colors.GREEN}  6. 도움말{Colors.RESET}")
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
    print(f"{Colors.GREEN}  2.7. 역방향 IP 조회{Colors.RESET}")
    print(f"{Colors.GREEN}  2.8. Google Dork 생성기{Colors.RESET}")
    print(f"{Colors.BLUE}  B. 뒤로 가기{Colors.RESET}")
    print(f"{Colors.RED}  0. 종료{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}====================================================={Colors.RESET}")

def display_web_analysis_menu():
    print_banner()
    print(f"{Colors.YELLOW}{Colors.BOLD}웹 분석 도구:{Colors.RESET}")
    print(f"{Colors.GREEN}  3.1. 웹 기술 스택 분석{Colors.RESET}")
    print(f"{Colors.GREEN}  3.2. WAF 감지{Colors.RESET}")
    print(f"{Colors.GREEN}  3.3. 보안 헤더 체크{Colors.RESET}")
    print(f"{Colors.GREEN}  3.4. Clickjacking 테스트{Colors.RESET}")
    print(f"{Colors.GREEN}  3.5. Open Redirect 체크{Colors.RESET}")
    print(f"{Colors.GREEN}  3.6. CORS 취약점 체크{Colors.RESET}")
    print(f"{Colors.GREEN}  3.7. Robots.txt 분석{Colors.RESET}")
    print(f"{Colors.GREEN}  3.8. Sitemap.xml 찾기{Colors.RESET}")
    print(f"{Colors.BLUE}  B. 뒤로 가기{Colors.RESET}")
    print(f"{Colors.RED}  0. 종료{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}====================================================={Colors.RESET}")

def display_network_security_menu():
    print_banner()
    print(f"{Colors.YELLOW}{Colors.BOLD}네트워크 보안 도구:{Colors.RESET}")
    print(f"{Colors.GREEN}  4.1. 포트 스캔{Colors.RESET}")
    print(f"{Colors.GREEN}  4.2. 서비스 배너 그래빙{Colors.RESET}")
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
    print(f"{Colors.WHITE}  - 웹 분석 도구: 웹 기술 스택, WAF, 보안 헤더, Clickjacking, Open Redirect, CORS, Robots.txt, Sitemap 등을 분석합니다.\n")
    print(f"{Colors.WHITE}  - 네트워크 보안 도구: 포트 스캔, 배너 그래빙, FTP 익명 로그인, Traceroute, Ping Sweep, 네트워크 지연 시간 등을 확인합니다.\n")
    print(f"{Colors.WHITE}  - 암호학 & 유틸리티: 해시 생성/식별, 인코딩/디코딩, 패스워드 생성, IP 계산기, Epoch 변환 등을 제공합니다.\n")
    print(f"{Colors.WHITE}  - 'B' 또는 'b'를 입력하여 이전 메뉴로 돌아갈 수 있습니다.\n")
    print(f"{Colors.WHITE}  - '0'을 입력하여 도구를 종료할 수 있습니다.\n")
    print(f"{Colors.RED}주의: 이 도구는 교육 및 보안 학습 목적으로 제작되었습니다. 타인의 동의 없이 무단으로 정보를 수집하거나 악용하는 행위는 법적 문제를 야기할 수 있습니다. 항상 윤리적이고 합법적인 범위 내에서 사용하십시오.{Colors.RESET}\n")
    input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")

def main():
    while True:
        display_main_menu()
        main_choice = input(f"{Colors.YELLOW}선택하세요 (0-6): {Colors.RESET}").strip()

        if main_choice == '1':
            target = input(f"{Colors.CYAN}종합 스캔할 도메인 또는 IP 주소를 입력하세요: {Colors.RESET}").strip()
            if target:
                run_full_scan(target)
            else:
                print(f"{Colors.RED}유효한 대상을 입력해주세요.{Colors.RESET}")
            input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")
        
        elif main_choice == '2': # 정보 수집 도구
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

        elif main_choice == '3': # 웹 분석 도구
            while True:
                display_web_analysis_menu()
                sub_choice = input(f"{Colors.YELLOW}선택하세요 (0-8, B): {Colors.RESET}").strip().upper()
                if sub_choice == 'B': break
                if sub_choice == '0': sys.exit(0)

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
                else: print(f"{Colors.RED}잘못된 선택입니다. 다시 시도해주세요.{Colors.RESET}")
                input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")

        elif main_choice == '4': # 네트워크 보안 도구
            while True:
                display_network_security_menu()
                sub_choice = input(f"{Colors.YELLOW}선택하세요 (0-6, B): {Colors.RESET}").strip().upper()
                if sub_choice == 'B': break
                if sub_choice == '0': sys.exit(0)

                target = input(f"{Colors.CYAN}대상 도메인 또는 IP 주소를 입력하세요: {Colors.RESET}").strip()
                if not target: print(f"{Colors.RED}유효한 대상을 입력해주세요.{Colors.RESET}"); continue

                if sub_choice == '4.1': run_individual_scan("Port Scan", target)
                elif sub_choice == '4.2': run_individual_scan("Banner Grabbing", target)
                elif sub_choice == '4.3': run_individual_scan("FTP Anon Login", target)
                elif sub_choice == '4.4': run_individual_scan("Traceroute", target)
                elif sub_choice == '4.5': run_individual_scan("Ping Sweep", target)
                elif sub_choice == '4.6': run_individual_scan("Latency Check", target)
                else: print(f"{Colors.RED}잘못된 선택입니다. 다시 시도해주세요.{Colors.RESET}")
                input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")

        elif main_choice == '5': # 암호학 & 유틸리티
            while True:
                display_crypto_utilities_menu()
                sub_choice = input(f"{Colors.YELLOW}선택하세요 (0-7, B): {Colors.RESET}").strip().upper()
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
                        import random # random 모듈이 여기에 필요합니다.
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
                else: print(f"{Colors.RED}잘못된 선택입니다. 다시 시도해주세요.{Colors.RESET}")
                input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")

        elif main_choice == '6':
            show_help()
        elif main_choice == '0':
            print(f"{Colors.RED}도구를 종료합니다. 안녕히 계세요!{Colors.RESET}")
            sys.exit(0)
        else:
            print(f"{Colors.RED}잘못된 선택입니다. 다시 시도해주세요.{Colors.RESET}")
            input(f"{Colors.CYAN}계속하려면 Enter 키를 누르세요...{Colors.RESET}")

if __name__ == "__main__":
    # SSL 모듈 임포트 (get_ssl_info 함수에서 사용)
    try:
        import ssl
    except ImportError:
        print(f"{Colors.RED}오류: 'ssl' 모듈을 임포트할 수 없습니다. Python 설치를 확인해주세요.{Colors.RESET}")
        sys.exit(1)
    
    # random 모듈 임포트 (password_generator 함수에서 사용)
    try:
        import random
    except ImportError:
        print(f"{Colors.RED}오류: 'random' 모듈을 임포트할 수 없습니다. Python 설치를 확인해주세요.{Colors.RESET}")
        sys.exit(1)

    main()

