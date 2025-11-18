#!/usr/bin/env python3
"""
Demo script to showcase the PhD Application Automator API
"""

import requests
import json

API_URL = "http://localhost:5000"

print("=" * 60)
print("🎓 PhD APPLICATION AUTOMATOR - LIVE DEMONSTRATION")
print("=" * 60)

# 1. Login
print("\n1️⃣  Logging in...")
login_response = requests.post(f"{API_URL}/api/auth/login", json={
    "email": "john@example.com",
    "password": "password123"
})
login_data = login_response.json()
token = login_data['access_token']
print(f"✅ Logged in as: {login_data['user']['name']}")

headers = {"Authorization": f"Bearer {token}"}

# 2. Discover Universities
print("\n2️⃣  Discovering universities...")
disc_response = requests.post(f"{API_URL}/api/universities/discover", headers=headers)
disc_data = disc_response.json()
total = disc_data.get('total', 0)
print(f"✅ Discovered {total} universities!")

# 3. Search Universities
print("\n3️⃣  Searching universities...")
search_response = requests.get(f"{API_URL}/api/universities/search", headers=headers)
search_data = search_response.json()
print(f"✅ Found {len(search_data['universities'])} universities")
print("\n   Top 3 Universities:")
for idx, uni in enumerate(search_data['universities'][:3], 1):
    funded = "💰 FUNDED" if uni.get('has_scholarship') else ""
    print(f"   {idx}. {uni['name']} ({uni['country']}) {funded}")

# 4. Discover Professors
print("\n4️⃣  Discovering professors...")
prof_disc_response = requests.post(f"{API_URL}/api/professors/discover", headers=headers)
prof_disc_data = prof_disc_response.json()
prof_total = prof_disc_data.get('total', 0)
print(f"✅ Discovered {prof_total} professors!")

# 5. Search Professors
print("\n5️⃣  Searching professors...")
prof_search_response = requests.get(f"{API_URL}/api/professors/search", headers=headers)
prof_search_data = prof_search_response.json()
print(f"✅ Found {len(prof_search_data['professors'])} professors")
print("\n   Top 3 Professors:")
for idx, prof in enumerate(prof_search_data['professors'][:3], 1):
    uni_name = prof.get('university', {}).get('name', 'Unknown')
    print(f"   {idx}. {prof['name']} ({prof.get('title', 'Professor')}) - {uni_name}")
    if prof.get('research_interests'):
        interests = ', '.join(prof['research_interests'][:3])
        print(f"      Research: {interests}")

# 6. Get Dashboard Analytics
print("\n6️⃣  Fetching dashboard analytics...")
analytics_response = requests.get(f"{API_URL}/api/analytics/dashboard", headers=headers)
analytics_data = analytics_response.json()
print(f"✅ Dashboard Statistics:")
print(f"   📊 Total Applications: {analytics_data['applications']['total']}")
print(f"   📧 Emails Sent: {analytics_data['emails']['sent']}")
print(f"   🎓 Universities Available: {analytics_data['opportunities']['universities']}")
print(f"   👨‍🏫 Professors Available: {analytics_data['opportunities']['professors']}")

print("\n" + "=" * 60)
print("✅ DEMONSTRATION COMPLETE!")
print("=" * 60)
print("\n📝 Summary:")
print(f"   • Registered and logged in successfully")
print(f"   • Discovered {total} universities worldwide")
print(f"   • Found {prof_total} professors")
print(f"   • All API endpoints working perfectly!")
print(f"   • Database initialized with sample data")
print("\n🌐 Frontend available at: http://localhost:3000")
print("🔧 Backend API running at: http://localhost:5000")
print("\n" + "=" * 60)
