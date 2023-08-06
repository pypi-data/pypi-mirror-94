import json

class Airplane:
  """Client for Airplane"""

  def __init__(self):
    return

  """Writes the value to the task's output."""
  def writeOutput(self, value):
    print("airplane_output %s" % json.dumps(value, separators=(',', ':')))

  """Writes the value to the task's output, tagged by the key."""
  def writeNamedOutput(self, key, value):
    print("airplane_output:%s %s" % key, json.dumps(value, separators=(',', ':')))

  """Triggers an Airplane task with the provided arguments."""
  def runTask(self, taskID, parameters):
    # Coming soon...
    return NotImplemented
