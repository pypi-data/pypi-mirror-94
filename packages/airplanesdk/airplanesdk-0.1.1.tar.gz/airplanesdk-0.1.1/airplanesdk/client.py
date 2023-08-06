import json
import os
import requests
import backoff

from .exceptions import RunFailedException, RunPendingException


class Airplane:
    """Client SDK for Airplane tasks."""

    __apiHost = os.getenv("AP_TASK_RUNTIME_API_HOST")
    __apiToken = os.getenv("AP_TASK_RUNTIME_TOKEN")

    def __init__(self):
        return

    """Writes the value to the task's output."""

    def writeOutput(self, value):
        print("airplane_output %s" % json.dumps(value, separators=(",", ":")))

    """Writes the value to the task's output, tagged by the key."""

    def writeNamedOutput(self, name, value):
        print("airplane_output:%s %s" % name, json.dumps(value, separators=(",", ":")))

    """Triggers an Airplane task with the provided arguments."""

    def run(self, taskID, parameters):
        # Boot the new task:
        resp = requests.post(
            "%s/taskRuntime/runTask" % (self.__apiHost),
            json={
                "taskID": taskID,
                "params": parameters,
            },
            headers={
                "X-Airplane-Token": self.__apiToken,
            },
        )
        body = resp.json()
        runId = body["runID"]

        return self.__getOutput(runId)

    def __backoff():
        yield from backoff.expo(factor=0.1, max_value=5)

    @backoff.on_exception(
        __backoff,
        (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            RunFailedException,
            RunPendingException,
        ),
        max_tries=1000,
    )
    def __getOutput(self, runId):
        resp = requests.get(
            "%s/taskRuntime/getOutput/%s" % (self.__apiHost, runId),
            headers={
                "X-Airplane-Token": self.__apiToken,
            },
        )
        body = resp.json()
        runStatus, output = body["runStatus"], body["output"]
        if runStatus == "Failed":
            raise RunFailedException()
        elif runStatus == "Succeeded":
            return output
        else:
            raise RunPendingException()
