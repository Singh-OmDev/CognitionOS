import redis
import json
from src.core.config import settings
from datetime import datetime

class ToolMemory:
    def __init__(self):
        self.redis = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.prefix = "tool_stats:"

    def update_tool_stats(self, tool_name: str, success: bool, duration_ms: float):
        """Update usage statistics for a tool."""
        key = f"{self.prefix}{tool_name}"
        
        # Use a Lua script or transaction for atomicity in production, 
        # but simple GET/SET is fine for prototype
        stats = self.get_tool_stats(tool_name)
        
        stats["total_uses"] += 1
        if success:
            stats["successes"] += 1
        else:
            stats["failures"] += 1
            
        # Update moving average latency
        current_avg = stats["avg_latency_ms"]
        stats["avg_latency_ms"] = (current_avg * (stats["total_uses"] - 1) + duration_ms) / stats["total_uses"]
        
        stats["last_used"] = datetime.utcnow().isoformat()
        
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
