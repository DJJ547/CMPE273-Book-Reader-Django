import redis

# Connect to Redis
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)

# Get all keys
keys = r.keys('*')
print("Keys:", keys)

# Retrieve data for a specific key
for key in keys:
    data = r.get(key)  # Use r.hgetall(key) for hashes
    print(f"Key: {key}, Value: {data}")
