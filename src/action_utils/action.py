import heapq

from src.config_utils.custom_logger import get_custom_logger

logger = get_custom_logger(__name__)


class PriorityQueue:
    """
    Stores actions in a queue, executing them in order of priority (typically the pets attack value)
    """
    def __init__(self):
        self.queue = []
        self.counter = 0

    def add_action(self, priority, action):
        logger.debug(f"Add priority {priority} Action to Queue {action}")
        count = self.counter / 10
        self.counter += 1
        heapq.heappush(self.queue, (-priority, count, action))

    def get_next_action(self):
        if not self.queue:
            return None
        priority, count, action = heapq.heappop(self.queue)
        return action

    def execute(self):
        self.get_next_action().execute()

    def execute_all(self):
        logger.debug("Queue Executing...")
        while len(self.queue):
            self.execute()
        logger.debug("Queue Empty")

    def clear_queue(self):
        self.queue = []

    def __repr__(self):
        return f"Queue: {[action for action in self.queue]}"

    def __len__(self):
        return len(self.queue)


class Action:
    """
    Stores information for an action_utils that is queued and executed by the PriorityQueue.
    The actual action_utils is executed as a method from the instance that initially created the action_utils.
    """
    def __init__(self, pet, method, **kwargs):
        self.pet = pet
        self.method = method
        self.kwargs = kwargs

    def execute(self):
        logger.debug(f"Executing Action {self}")
        return getattr(self.pet, self.method.name)(**self.kwargs)

    def __repr__(self):
        effect = self.method
        target = self.kwargs.get("target")
        kwargs = self.kwargs
        if target:
            target = target
            kwargs = {key: value for key, value in self.kwargs.items() if key != "target"}

        return f"Action:({self.pet}, {effect}, {target}, {kwargs})"
