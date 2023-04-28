
class ActionHandler:
    def __init__(self):
        self.action_list = []

    def execute_actions(self):
        for action in self.action_list:
            self.execute(action)

    @staticmethod
    def execute(action):
        print(action)
