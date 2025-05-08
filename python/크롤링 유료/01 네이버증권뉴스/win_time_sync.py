import subprocess
from datetime import datetime

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        return result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return "", str(e)

def log_to_file(content):
    with open("time_sync_log.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        f.write(f"{timestamp} {content}\n\n")

# 전체 작업 리스트
commands = [
    'net stop w32time',
    'w32tm /unregister',
    'w32tm /register',
    'net start w32time',
    'w32tm /config /manualpeerlist:"time.windows.com,0x1 pool.ntp.org,0x1 time.nist.gov,0x1" /syncfromflags:manual /reliable:NO /update',
    'net stop w32time',
    'net start w32time',
    #'w32tm /resync /rediscover'
]

log_to_file("=== Windows 시간 동기화 자동화 시작 ===")

for cmd in commands:
    out, err = run_command(cmd)
    log_to_file(f">>> 명령어: {cmd}\n[출력]\n{out}\n[에러]\n{err}")

log_to_file("=== 작업 완료 ===\n")
