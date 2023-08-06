# Developed by Aptus Engineering, Inc. <https://aptus.aero>
# See LICENSE.md file in project root directory

import time
import requests
from datetime import datetime
from dataclasses import dataclass

# Response Class
@dataclass
class Response:
    status: str
    stdout: str
    stderr: str
    duration: float
    metrics: dict


# StratumRun Class
class StratumRun:
    '''
    A StratumRun object is used to send commands to execute on the Stratum cloud. See https://stratumcloud.io for more information.
    '''
    def __init__(self, key):
        '''
        Class Constructor
        '''
        self.key = key


    def run(self, script, requirements=[], language="python3", timeout=30):
        job = self.start(script, requirements, language, timeout)

        # Wait for response
        fails = 0
        for _ in range(timeout):
            try:
                res = self.get(job)
                if res.status == "Queued" or res.status == "Processing":
                    time.sleep(1)
                    continue

                return res
            except:
                fails += 1
                if fails > 3:
                    self.kill(job)
                    raise Exception("Too many failed attempts")

        self.kill(job)
        raise Exception("Timed out")

    
    def start(self, script, requirements=[], language="python3", timeout=30):
        res = requests.post("https://stratum-run-" + language + ".stratum-app.io/stratum/jobs", json={
            "requirements": requirements,
            "script": script
        }, headers={
            "X-STRATUM-AUTH": self.key
        })
        return "https://stratum-run-" + language + ".stratum-app.io/stratum/jobs/" + res.json()["jobId"]


    def get(self, job):
        res = requests.get(job, headers={
            "X-STRATUM-AUTH": self.key
        }).json()

        # Compute duration
        duration = 0
        if res["status"] == "Completed" or res["status"] == "Failed":
            t0 = datetime.strptime(res["startTime"][:26], "%Y-%m-%dT%H:%M:%S.%f")
            t1 = datetime.strptime(res["endTime"][:26], "%Y-%m-%dT%H:%M:%S.%f")
            duration = (t1-t0).total_seconds()

        return Response(res["status"], res["stdout"], res["stderr"], duration, res["metrics"])


    def kill(self, job):
        requests.delete(job, headers={
            "X-STRATUM-AUTH": self.key
        })