

class Dummy_ActionHandler:
    def __init__(self):
        self.action_list = []

    def add_action(self, action):
        if action:
            self.action_list.append(action)

    def clear_actions(self):
        self.action_list = []


class Dummy_Action:
    def __init__(self, name, source, **kwargs):
        self.name = name
        self.source = source
        self.kwargs = kwargs


def generate_dummy_action(name="name", source=None, trigger_event=None, **kwargs):
    return Dummy_Action(name, source, trigger_event=trigger_event, **kwargs)
