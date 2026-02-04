"""
Curated High-Success University List
Selected based on SheerID frequent exploit targets (PSU Focused)
"""

# Pennsylvania State University Locations (Known Working IDs)
UNIVERSITIES = {
    "Pennsylvania State University-Main Campus": 2565,
    "Pennsylvania State University-World Campus": 651379,
    "Pennsylvania State University-Penn State Harrisburg": 8387,
    "Pennsylvania State University-Penn State Altoona": 8382,
    "Pennsylvania State University-Penn State Berks": 8396,
    "Pennsylvania State University-Penn State Brandywine": 8379,
    "Pennsylvania State University-College of Medicine": 2560,
    "Pennsylvania State University-Penn State Lehigh Valley": 650600,
    "Pennsylvania State University-Penn State Hazleton": 8388,
    "Pennsylvania State University-Penn State Worthington Scranton": 8394
}

def get_random_university():
    import random
    name = random.choice(list(UNIVERSITIES.keys()))
    organization_id = UNIVERSITIES[name]
    
    # PSU Extended ID logic (usually same as ID but string)
    return {
        "name": name, 
        "id": organization_id,
        "idExtended": str(organization_id)
    }
