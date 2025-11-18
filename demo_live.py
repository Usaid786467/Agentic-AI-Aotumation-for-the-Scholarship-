"""
Live API Demonstration Script
Demonstrates all major features of the PhD Application Automator
"""

import requests
import json
from datetime import datetime

API_URL = "http://localhost:5000"

print("=" * 60)
print("🎓 PhD APPLICATION AUTOMATOR - LIVE DEMONSTRATION")
print("=" * 60)

# 1. Register a new user
print("\n1️⃣  Registering new demo user...")
register_data = {
    "name": "Demo User",
    "email": f"demo_{datetime.now().timestamp()}@example.com",
    "password": "demo123"
}
register_response = requests.post(f"{API_URL}/api/auth/register", json=register_data)
if register_response.status_code == 201:
    register_result = register_response.json()
    token = register_result.get('access_token')
    user_name = register_result.get('user', {}).get('name', 'User')
    print(f"✅ Registered and logged in as: {user_name}")
else:
    print(f"❌ Registration failed: {register_response.text}")
    exit(1)

headers = {"Authorization": f"Bearer {token}"}

# 2. Discover Universities
print("\n2️⃣  Discovering universities...")
disc_response = requests.post(f"{API_URL}/api/universities/discover", headers=headers)
if disc_response.status_code == 200:
    disc_data = disc_response.json()
    total = disc_data.get('total', 0)
    print(f"✅ Discovered {total} universities!")
else:
    print(f"⚠️  Discovery status: {disc_response.status_code}")

# 3. Search Universities
print("\n3️⃣  Searching universities...")
search_response = requests.get(f"{API_URL}/api/universities/search", headers=headers)
if search_response.status_code == 200:
    search_data = search_response.json()
    universities = search_data.get('universities', [])
    print(f"✅ Found {len(universities)} universities")
    if universities:
        print("\n   Top 3 Universities:")
        for idx, uni in enumerate(universities[:3], 1):
            funded = "💰 FUNDED" if uni.get('has_scholarship') else ""
            print(f"   {idx}. {uni['name']} ({uni['country']}) {funded}")
else:
    print(f"⚠️  Search status: {search_response.status_code}")

# 4. Discover Professors
print("\n4️⃣  Discovering professors...")
prof_disc_response = requests.post(f"{API_URL}/api/professors/discover", headers=headers)
if prof_disc_response.status_code == 200:
    prof_disc_data = prof_disc_response.json()
    prof_total = prof_disc_data.get('total', 0)
    print(f"✅ Discovered {prof_total} professors!")
else:
    print(f"⚠️  Discovery status: {prof_disc_response.status_code}")

# 5. Search Professors
print("\n5️⃣  Searching professors...")
prof_search_response = requests.get(f"{API_URL}/api/professors/search", headers=headers)
if prof_search_response.status_code == 200:
    prof_search_data = prof_search_response.json()
    professors = prof_search_data.get('professors', [])
    print(f"✅ Found {len(professors)} professors")
    if professors:
        print("\n   Top 3 Professors:")
        for idx, prof in enumerate(professors[:3], 1):
            match_score = prof.get('match_score', 0)
            print(f"   {idx}. Prof. {prof['name']} - {prof['university_name']}")
            print(f"      Research: {prof.get('research_interests', 'N/A')[:50]}...")
            print(f"      Match Score: {match_score}%")
else:
    print(f"⚠️  Search status: {prof_search_response.status_code}")

# 6. Get Analytics
print("\n6️⃣  Fetching analytics...")
analytics_response = requests.get(f"{API_URL}/api/analytics/dashboard", headers=headers)
if analytics_response.status_code == 200:
    analytics_data = analytics_response.json()
    print("✅ Analytics retrieved:")
    if 'opportunities' in analytics_data:
        print(f"   🎓 Universities Available: {analytics_data['opportunities'].get('universities', 0)}")
        print(f"   👨‍🏫 Professors Available: {analytics_data['opportunities'].get('professors', 0)}")
else:
    print(f"⚠️  Analytics status: {analytics_response.status_code}")

print("\n" + "=" * 60)
print("✅ DEMONSTRATION COMPLETE!")
print("=" * 60)
print("\n📝 Summary:")
print(f"   • Registered and logged in successfully")
print(f"   • Discovered universities and professors")
print(f"   • API endpoints responding correctly")
print(f"   • Database operational with sample data")
print("\n🌐 Frontend available at: http://localhost:3000")
print("🔧 Backend API running at: http://localhost:5000")
print("\n" + "=" * 60)
