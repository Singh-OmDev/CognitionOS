import redis
import json
from src.core.config import settings
from datetime import datetime, timezone

class ToolMemory:
    def __init__(self):
        self.redis = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.prefix = "tool_stats:"

    def update_tool_stats(self, tool_name: str, success_score: float, duration_ms: float):
        """
        Update usage statistics for a tool using Alpha-Beta (Bayesian) updates.
        success_score: 0.0 to 1.0 (1.0 = perfect success, 0.0 = total failure)
        """
        key = f"{self.prefix}{tool_name}"
        
        stats = self.get_tool_stats(tool_name)
        
        stats["total_uses"] += 1
        
        # Bayesian update:
        # Success adds to alpha (successes)
        # Failure adds to beta (failures) based on score
        stats["successes"] += success_score
        stats["failures"] += (1.0 - success_score)
            
        # Update moving average latency
        current_avg = stats["avg_latency_ms"]
        stats["avg_latency_ms"] = (current_avg * (stats["total_uses"] - 1) + duration_ms) / stats["total_uses"]
        
        stats["last_used"] = datetime.now(timezone.utc).isoformat()
        
        self.redis.set(key, json.dumps(stats))

    def get_tool_stats(self, tool_name: str) -> dict:
        """Get statistics for a tool."""
        key = f"{self.prefix}{tool_name}"
        data = self.redis.get(key)
        
        if data:
            return json.loads(data)
        
        return {
            "total_uses": 0,
            "successes": 0,
            "failures": 0,
            "avg_latency_ms": 0.0,
            "last_used": None
        }
