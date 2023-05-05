from src.pet_data_utils.enums.trigger_event import TriggerEvent


class Dummy_AbilityBase:
    def __init__(self, owner, trigger_event=None):
        self.owner = owner
        self.trigger_event = trigger_event

    def apply(self, **kwargs):
        if self.trigger_event:
            return self.trigger_event.name, kwargs

        return "None", kwargs

    def trigger(self, event, **kwargs):
        if event == self.trigger_event:
            return self.apply(**kwargs)


def generate_dummy_ability(owner, trigger_event=None):
    trigger_event_dict = {item.name.lower(): item for item in TriggerEvent}

    if trigger_event and trigger_event.lower() in trigger_event_dict:
        trigger_event = trigger_event_dict[trigger_event.lower()]
    else:
        trigger_event = None

    return Dummy_AbilityBase(owner, trigger_event)
