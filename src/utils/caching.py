import redis
import json
import hashlib

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def hash_key(prefix: str, value: str) -> str:
    hashed = hashlib.sha256(value.encode()).hexdigest()
    return f"{prefix}:{hashed}"

# cache for search agent

def get_cached_search_results(query: str):
    key = hash_key("search", query)
    return redis_client.get(key)

def cache_search_results(query: str, results: dict, ttl=1800):
    key = hash_key("search", query)
    redis_client.setex(key, ttl, json.dumps(results))

# cache for memory agent

def get_cached_memory(user_id: str):
    key = f"memory:{user_id}"
    return redis_client.get(key)

def cache_memory(user_id: str, history: dict, ttl=900):
    key = f"memory:{user_id}"
    redis_client.setex(key, ttl, json.dumps(history))

# cache for intent, instruction and conversation agents

def get_cached_nlp_result(agent_name: str, message: str):
    key = hash_key(agent_name, message)
    result = redis_client.get(key)
    if result is not None:
        redis_client.incr(f"cache_hits:{agent_name}")
    else:
        redis_client.incr(f"cache_misses:{agent_name}")
    return result

def cache_nlp_result(agent_name: str, message: str, result: dict, ttl=1800):
    key = hash_key(agent_name, message)
    redis_client.setex(key, ttl, json.dumps(result))

# cache for response sythesis

def get_cached_synthesis_key(agent_outputs: dict):
    raw = json.dumps(agent_outputs, sort_keys=True)
    key = hash_key("synth", raw)
    result = redis_client.get(key)
    if result is not None:
        redis_client.incr("cache_hits:intent")
    else:
        redis_client.incr("cache_misses:intent")

    hits = redis_client.get("cache_hits:intent")
    misses = redis_client.get("cache_misses:intent")
    print(f"[CACHE] Intent Agent - Hits: {hits or 0}, Misses: {misses or 0}")

    return result

def cache_synthesis(agent_outputs: dict, response: str, ttl=600):
    raw = json.dumps(agent_outputs, sort_keys=True)
    key = hash_key("synth", raw)
    redis_client.setex(key, ttl, response)

