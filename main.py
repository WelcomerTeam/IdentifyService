import logging
import os
import time
from typing import Dict

from quart import Quart, request

import structures

app = Quart(__name__)


identify_locks: Dict[str, structures.IdentifyLock] = {}

logging.basicConfig(format="%(asctime)s %(message)s")
logger = logging.getLogger("identifyService")
logger.setLevel(logging.INFO)


@app.route("/identify", methods=["POST"])
async def identifyRoute():
    form = await request.get_json()

    now = time.time()

    identifyRequest = structures.IdentifyRequest()
    identifyRequest.from_data(form)

    key: str = "%s:%d" % (identifyRequest.tokenHash,
                          identifyRequest.shardID % identifyRequest.maxConcurrency)

    lock = identify_locks.get(key)
    if not lock:
        logger.info("Created new lock %s", key)

        lock = structures.IdentifyLock(
            limit=1, available=1, duration=5.5, resetsAt=0)

        identify_locks[key] = lock

    # Lock timer has reset, refill bucket
    if lock.resetsAt <= now:
        logger.info("Lock %s refreshed", key)

        lock.resetsAt = lock.duration + now
        lock.available = lock.limit

    # Lock is empty, return time to wait until it is refilled
    if lock.available <= 0:
        logger.info("Lock %s not available", key)

        identifyResponse = structures.IdentifyResponse(
            False, int((lock.resetsAt - now) * 1000), "")
        return identifyResponse.jsonify()

    lock.available -= 1

    logger.info("Successful lock on %s", key)

    identifyResponse = structures.IdentifyResponse(True, 0, "")
    return identifyResponse.jsonify()

if __name__ == "__main__":
    print(os.getenv("PORT"))
    app.run(
        host=os.getenv("HOST"),
        port=os.getenv("PORT")
    )
