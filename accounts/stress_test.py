import requests
import threading
import time

# The endpoint we want to "Stress"
API_URL = "http://127.0.0.1:8000/accounts/register/"

def register_user(user_id):
    data = {
        "username": f"stress_user_{user_id}_{time.time()}",
        "email": f"stress_{user_id}@test.com",
        "password": "password123"
    }
    try:
        start_time = time.time()
        response = requests.post(API_URL, json=data)
        duration = time.time() - start_time
        print(f"User {user_id}: Status {response.status_code} in {duration:.2f}s")
    except Exception as e:
        print(f"User {user_id} failed: {e}")

# MAIN STRESS LOGIC: Launch 100 threads 
threads = []
print("Starting Stress Test on PostgreSQL")
for i in range(100):
    t = threading.Thread(target=register_user, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
print("Stress Test Complete")