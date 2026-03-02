"""
Simple API test script
"""
import requests
import json

# Test health endpoint
print("Testing /health endpoint...")
response = requests.get('http://localhost:8000/health')
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}\n")

# Test recommend endpoint
print("Testing /recommend endpoint...")
data = {
    "query": "Java developer with collaboration skills",
    "top_k": 5
}

response = requests.post(
    'http://localhost:8000/recommend',
    json=data
)

print(f"Status: {response.status_code}")
result = response.json()

print(f"\nQuery: {result['query_used'][:50]}...")
print(f"K-type: {result['k_count']}, P-type: {result['p_count']}")
print(f"\nTop {len(result['recommendations'])} Recommendations:")

for i, rec in enumerate(result['recommendations'], 1):
    print(f"\n{i}. [{rec['test_type']}] {rec['assessment_name']}")
    print(f"   {rec['description'][:80]}...")
    print(f"   Skills: {rec['skills']}")
