import redis
import random
import datetime
from .amplitude import Amplitude

class Choixpeau:

    def __init__(
        self, 
        redis_config, 
        ab_test_ids=[], 
        buckets=["A", "B"], 
        amplitude_api_key=None
    ):
        self._r = redis.Redis(**redis_config, decode_responses=True)
        self.ab_test_ids = ab_test_ids
        self.buckets = buckets
        
        if amplitude_api_key:
            self.amplitude = Amplitude(api_key=amplitude_api_key) 

    def _draw(self):
        return {
            "created_at": datetime.datetime.today().strftime("%Y-%m-%d"), 
            "ab_test_group": random.choice(self.buckets)
        }      

    def _get(self, ab_test_id, user_id):
        
        key = f"ab:{ab_test_id}:{user_id}"
        value = self._r.hgetall(key)

        if value:
            return None, value, ab_test_id 
        else:
            return key, self._draw(), ab_test_id
    
    def get(self, user_id):
        return [self._get(ab_test_id, user_id) for ab_test_id in self.ab_test_ids]

    def store(self, key, value):
        self._r.hset(key, mapping=value)
        if hasattr(self, "amplitude"):
            self.amplitude.post(key, value)