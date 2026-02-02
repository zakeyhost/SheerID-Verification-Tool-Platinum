"""
Anti-Detection Module for SheerID Verification Tools
Shared module for better anti-fraud bypass

Features:
- Random User-Agent rotation (Chrome, Firefox, Edge, Safari)
- Browser-like headers with proper ordering
- Random fingerprint generation
- Request delay randomization
- TLS fingerprint spoofing with Chrome impersonation (curl_cffi)
- NewRelic tracking headers (required for SheerID)
- Canvas/WebGL fingerprint simulation
- Proxy validation and formatting
"""

import random
import hashlib
import time
import uuid
import base64
import json
import sys

# ============ CHROME IMPERSONATION VERSIONS ============
CHROME_VERSIONS = ["chrome131", "chrome130", "chrome124", "chrome120"]
IMPERSONATE_OPTIONS = {
    "chrome": ["chrome131", "chrome130", "chrome124", "chrome120"],
    "edge": ["edge131", "edge127", "edge101"],
    "safari": ["safari18", "safari17_2_ios", "safari17_0"],
}
DEFAULT_IMPERSONATE = "chrome131"

USER_AGENTS_CHROME = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
]
USER_AGENTS = USER_AGENTS_CHROME

RESOLUTIONS = ["1920x1080", "1366x768", "1536x864", "1440x900", "1280x720"]
TIMEZONES = [-8, -7, -6, -5, -4, 0, 1, 2, 3, 5.5, 8, 9, 10]
LANGUAGES = ["en-US,en;q=0.9", "en-GB,en;q=0.9"]
PLATFORMS = [("Windows", '"Windows"', '"Chromium";v="131", "Google Chrome";v="131"')]

def get_random_user_agent(): return random.choice(USER_AGENTS)
def get_fingerprint(): return hashlib.md5(str(time.time()).encode()).hexdigest()
def generate_newrelic_headers():
    trace_id = uuid.uuid4().hex[:32]
    span_id = uuid.uuid4().hex[:16]
    timestamp = int(time.time() * 1000)
    payload = {"v": [0, 1], "d": {"ty": "Browser", "ac": "364029", "ap": "120719994", "id": span_id, "tr": trace_id, "ti": timestamp}}
    return {
        "newrelic": base64.b64encode(json.dumps(payload).encode()).decode(),
        "traceparent": f"00-{trace_id}-{span_id}-01",
        "tracestate": f"364029@nr=0-1-364029-120719994-{span_id}----{timestamp}",
    }

def get_headers(for_sheerid=True):
    headers = {"accept": "application/json", "user-agent": get_random_user_agent()}
    if for_sheerid:
        headers.update({"clientversion": "2.178.0", "clientname": "jslib", **generate_newrelic_headers()})
    return headers

def random_delay(min_ms=300, max_ms=1200): time.sleep(random.randint(min_ms, max_ms) / 1000)

def create_session(proxy=None, impersonate=None):
    from curl_cffi import requests as curl_requests
    imp = impersonate or DEFAULT_IMPERSONATE
    proxies = {"http": proxy, "https": proxy} if proxy else None
    session = curl_requests.Session(proxies=proxies, impersonate=imp)
    return session, "curl_cffi", imp

def warm_session(session, program_id=None):
    session.get("https://services.sheerid.com/rest/v2/config", headers=get_headers())
    return session

def handle_fraud_rejection(retry_count, error_payload, message=""):
    print(f"🚨 FRAUD REJECTION: {message}")
