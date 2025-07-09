#!/usr/bin/env python3
"""
TechNova Website Test Script
Run this script to test your website before deployment
"""

import requests
import sys
import time
from urllib.parse import urljoin

def test_local_server(base_url="http://localhost:5000"):
    """Test the local Flask server"""
    tests = [
        {
            "name": "Homepage Load Test",
            "url": base_url,
            "expected_status": 200,
            "expected_content": ["TechNova", "Electronics"]
        },
        {
            "name": "Static CSS Test",
            "url": urljoin(base_url, "/static/style.css"),
            "expected_status": 200,
            "expected_content": ["gradient", "color"]
        },
        {
            "name": "Chatbot API Test",
            "url": urljoin(base_url, "/chat"),
            "method": "POST",
            "data": {"message": "Hello"},
            "expected_status": 200,
            "expected_content": ["response"]
        }
    ]
    
    print("🔍 Testing TechNova Website...")
    print("=" * 50)
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        print(f"⏳ {test['name']}...")
        
        try:
            if test.get("method") == "POST":
                response = requests.post(
                    test["url"], 
                    json=test.get("data", {}),
                    timeout=10
                )
            else:
                response = requests.get(test["url"], timeout=10)
            
            # Check status code
            if response.status_code == test["expected_status"]:
                print(f"✅ Status Code: {response.status_code}")
            else:
                print(f"❌ Status Code: {response.status_code} (expected {test['expected_status']})")
                continue
            
            # Check content
            content_found = True
            for expected in test.get("expected_content", []):
                if expected.lower() not in response.text.lower():
                    print(f"❌ Missing content: '{expected}'")
                    content_found = False
            
            if content_found:
                print(f"✅ Content validation passed")
                passed += 1
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        
        print("-" * 30)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your website is ready for deployment.")
        return True
    else:
        print("⚠️  Some tests failed. Please check your local server.")
        return False

def check_requirements():
    """Check if all required packages are installed"""
    print("📦 Checking Python packages...")
    
    required_packages = [
        "flask", "google-generativeai", "gunicorn"
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Install missing packages:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    print("✅ All required packages are installed!")
    return True

def deployment_checklist():
    """Show deployment checklist"""
    checklist = [
        "✅ Updated requirements.txt with gunicorn",
        "✅ Created Procfile for deployment",
        "✅ Updated app.py with environment variables",
        "✅ Tested locally",
        "📝 Upload to GitHub repository",
        "🚀 Deploy to chosen platform (Render/Heroku/PythonAnywhere)",
        "🔐 Set GOOGLE_API_KEY environment variable",
        "🌐 Configure custom domain (optional)",
        "📊 Set up analytics (optional)"
    ]
    
    print("\n📋 Deployment Checklist:")
    print("=" * 40)
    for item in checklist:
        print(item)

if __name__ == "__main__":
    print("🚀 TechNova Deployment Helper")
    print("=" * 50)
    
    # Check packages first
    if not check_requirements():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    
    # Test local server if running
    try:
        if test_local_server():
            deployment_checklist()
    except:
        print("🔔 Start your local server first:")
        print("python app.py")
        print("\nThen run this test script again.")
        deployment_checklist()
