

class Dummy_ActionHandler:
    def __init__(self):
        self.action_list = []

    def add_action(self, action):
        if action:
            self.action_list.append(action)

    def clear_actions(self):
        self.action_list = []
