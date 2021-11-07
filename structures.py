class IdentifyRequest():
    shardID: int
    shardCount: int
    token: str
    tokenHash: str
    maxConcurrency: int

    def __init__(self):
        pass

    def from_data(self, data):
        self.shardID = data.get("shard_id")
        self.shardCount = data.get("shard_count")
        self.token = data.get("token")
        self.tokenHash = data.get("token_hash")
        self.maxConcurrency = data.get("max_concurrency")


class IdentifyResponse():
    success: bool

    # When success is false, wait represents
    # the time to wait in milliseconds to retry.
    wait: int
    message: str

    def __init__(self, success, wait, message):
        self.success = success
        self.wait = wait
        self.message = message

    def jsonify(self) -> dict:
        return {
            "success": self.success,
            "wait": self.wait,
            "message": self.message
        }


class IdentifyLock():
    limit: int
    available: int
    duration: float
    resetsAt: int

    def __init__(self, limit, available, duration, resetsAt):
        self.limit = limit
        self.available = available
        self.duration = duration
        self.resetsAt = resetsAt
