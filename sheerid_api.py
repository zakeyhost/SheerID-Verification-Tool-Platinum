"""
SheerID API Integration Module
Core verification logic
"""
import re
import json
import time
import base64
from urllib.parse import urlparse, parse_qs
from curl_cffi import requests
import anti_detect

class SheerIDClient:
    def __init__(self, proxy=None):
        self.session, _, _ = anti_detect.create_session(proxy=proxy)
        self.base_url = "https://services.sheerid.com/rest/v2"
        
    def extract_verification_id_from_url(self, url):
        """Extracts verificationId from a SheerID URL"""
        # Supports URLs like: https://verify.sheerid.com/verify/VERIFICATION_ID/
        match = re.search(r'/verify/([a-zA-Z0-9]{24})', url)
        if match:
            return match.group(1)
        return None

    def get_verification_details(self, verification_id):
        """Get current status of verification"""
        url = f"{self.base_url}/verification/{verification_id}"
        resp = self.session.get(url, headers=anti_detect.get_headers())
        return resp.json()

    def submit_student_info(self, verification_id, student_data):
        """Step 1: Submit personal info"""
        url = f"{self.base_url}/verification/{verification_id}/step/collectStudentPersonalInfo"
        
        payload = {
            "firstName": student_data["firstName"],
            "lastName": student_data["lastName"],
            "birthDate": student_data["birthDate"],
            "email": student_data["email"],
            "organization": {
                "id": student_data["organization"]["id"],
                "name": student_data["organization"]["name"]
            },
            "deviceFingerprint": anti_detect.get_fingerprint(),
            "metadata": {
                "locale": "en-US"
            }
        }
        
        # Add delay for realism
        anti_detect.random_delay(1000, 3000)
        
        resp = self.session.post(
            url, 
            json=payload, 
            headers=anti_detect.get_headers()
        )
        return resp.json()

    def upload_document(self, verification_id, doc_bytes, doc_type="student_id"):
        """Step 2: Upload document if required"""
        url = f"{self.base_url}/verification/{verification_id}/step/docUpload"
        
        # Prepare multipart upload
        # SheerID expects 'file' parameter
        files = {
            'file': (f'{doc_type}.png', doc_bytes, 'image/png')
        }
        
        # Add delay
        anti_detect.random_delay(2000, 5000)
        
        # Note: curl_cffi handles multipart boundaries automatically
        # We need headers WITHOUT Content-Type (requests adds it with boundary)
        headers = anti_detect.get_headers()
        if "Content-Type" in headers:
            del headers["Content-Type"]
            
        resp = self.session.post(
            url,
            files=files,
            headers=headers
        )
        return resp.json()

    def check_status(self, verification_id):
        """Poll for final status"""
        # Poll a few times
        for _ in range(5):
            details = self.get_verification_details(verification_id)
            step = details.get("currentStep")
            
            if step == "success":
                return {
                    "status": "SUCCESS", 
                    "reward_code": details.get("rewardCode"),
                    "redirect_url": details.get("redirectUrl")
                }
            elif step == "error" or details.get("errorIds"):
                return {
                    "status": "FAILED",
                    "reason": details.get("errorIds", ["Unknown error"])
                }
            elif step == "docUpload":
                 return {
                    "status": "DOC_UPLOAD_REQUIRED",
                    "details": details
                }
            elif step == "pending":
                time.sleep(2)
                continue
                
            time.sleep(1)
            
        return {"status": "TIMEOUT", "last_details": details}

    def process_verification(self, verification_id, student_data, doc_generator_func=None):
        """Full automated flow"""
        print(f"[*] Processing verification: {verification_id}")
        
        # 1. Submit Info
        print(f"[*] Submitting info for {student_data['display_info']['full_name']} at {student_data['display_info']['university']}")
        result = self.submit_student_info(verification_id, student_data)
        
        current_step = result.get("currentStep")
        print(f"[*] Step 1 Result: {current_step}")
        
        if current_step == "success":
            return self.check_status(verification_id)
            
        elif current_step == "docUpload":
            print("[*] Document upload required. Generating fake doc...")
            if doc_generator_func:
                doc_bytes = doc_generator_func(
                    student_data["firstName"],
                    student_data["lastName"],
                    student_data["organization"]["name"]
                )
                
                print("[*] Uploading document...")
                upload_res = self.upload_document(verification_id, doc_bytes)
                print(f"[*] Upload Result: {upload_res.get('currentStep')}")
                
                return self.check_status(verification_id)
            else:
                 return {"status": "DOC_REQUIRED_NO_GENERATOR"}
                 
        elif current_step == "reject": 
             return {"status": "REJECTED", "errors": result.get("errorIds")}
             
        return self.check_status(verification_id)
