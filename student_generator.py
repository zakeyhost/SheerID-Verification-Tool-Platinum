"""
Student Data Generator for SheerID Verification
Generates realistic student profiles
"""
from faker import Faker
import random
from datetime import datetime, timedelta
import universities

fake = Faker('en_US')

DOMAIN_SUFFIXES = ["edu", "college.edu", "univ.edu", "student.edu"]

def generate_student_profile(university=None):
    """
    Generate a full student profile
    """
    if not university:
        university = universities.get_random_university()
        
    first_name = fake.first_name()
    last_name = fake.last_name()
    
    # Generate DOB (18-24 years old)
    age = random.randint(18, 24)
    dob_date = datetime.now() - timedelta(days=age*365 + random.randint(0, 364))
    birth_date = dob_date.strftime("%Y-%m-%d")
    
    # Clean university name for email
    school_slug = university["name"].lower().replace(",", "").replace(" ", "").replace("-", "")
    if "university" in school_slug:
        school_slug = school_slug.replace("university", "")
    elif "college" in school_slug:
        school_slug = school_slug.replace("college", "")
        
    # Generate email
    # Patterns: first.last@uni.edu, f.last@uni.edu, last.first@uni.edu
    email_pattern = random.choice([
        f"{first_name.lower()}.{last_name.lower()}",
        f"{first_name[0].lower()}{last_name.lower()}",
        f"{first_name.lower()}{last_name.lower()}{random.randint(10,99)}"
    ])
    
    domain_suffix = random.choice(DOMAIN_SUFFIXES)
    email = f"{email_pattern}@{school_slug}.{domain_suffix}"
    
    return {
        "firstName": first_name,
        "lastName": last_name,
        "birthDate": birth_date,
        "email": email,
        "organization": university,
        "metadata": {
            "locale": "en-US"
        },
        "display_info": {
            "full_name": f"{first_name} {last_name}",
            "age": age,
            "university": university["name"]
        }
    }

if __name__ == "__main__":
    # Test generator
    print(generate_student_profile())
