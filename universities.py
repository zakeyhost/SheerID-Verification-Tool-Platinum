"""
Database of Supported US Universities with SheerID Organization IDs
"""

# Format: "University Name": OrganizationID
# These IDs are examples and might need to be verified against live SheerID API
# Commonly supported major US universities
UNIVERSITIES = {
    "Arizona State University": 222,
    "Boston University": 321,
    "California State University, Long Beach": 427,
    "Columbia University": 567,
    "Cornell University": 589,
    "Florida State University": 709,
    "Georgia Institute of Technology": 758,
    "Harvard University": 833,
    "Indiana University Bloomington": 945,
    "Iowa State University": 966,
    "Kansas State University": 1002,
    "Louisiana State University": 1098,
    "Massachusetts Institute of Technology": 1184,
    "Michigan State University": 1225,
    "New York University": 1412,
    "North Carolina State University": 1436,
    "Ohio State University": 1506,
    "Oklahoma State University": 1515,
    "Oregon State University": 1534,
    "Pennsylvania State University": 1572,
    "Purdue University": 1629,
    "Rutgers University-New Brunswick": 1698,
    "San Diego State University": 1745,
    "San Jose State University": 1753,
    "Stanford University": 1856,
    "Texas A&M University": 1928,
    "Texas Tech University": 1947,
    "University of Alabama": 2012,
    "University of Arizona": 2034,
    "University of Arkansas": 2045,
    "University of California, Berkeley": 2067,
    "University of California, Davis": 2070,
    "University of California, Irvine": 2072,
    "University of California, Los Angeles": 2073,
    "University of California, San Diego": 2076,
    "University of Colorado Boulder": 2105,
    "University of Florida": 2134,
    "University of Georgia": 2145,
    "University of Houston": 2156,
    "University of Illinois Urbana-Champaign": 2178,
    "University of Maryland, College Park": 2245,
    "University of Michigan": 2267,
    "University of Minnesota Twin Cities": 2278,
    "University of North Carolina at Chapel Hill": 2312,
    "University of Oregon": 2345,
    "University of Pennsylvania": 2356,
    "University of Pittsburgh": 2367,
    "University of Southern California": 2389,
    "University of Texas at Austin": 2412,
    "University of Utah": 2434,
    "University of Virginia": 2445,
    "University of Washington": 2456,
    "University of Wisconsin-Madison": 2478,
    "Virginia Tech": 2512,
    "Washington State University": 2545,
    "Yale University": 2678
}

def get_random_university():
    import random
    name = random.choice(list(UNIVERSITIES.keys()))
    return {"name": name, "id": UNIVERSITIES[name]}

def search_university(query):
    results = []
    query = query.lower()
    for name, oid in UNIVERSITIES.items():
        if query in name.lower():
            results.append({"name": name, "id": oid})
    return results
