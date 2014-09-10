#Not an event as in input event in PyGame's event queue
#Rather a "game event" - e.g. spawn enemies, play sounds etc

class GameEvent(object):
    def __init__(self, name):
        self.name = name

class SpawnEvent(GameEvent):
    def __init__(self, name, enemies, location):
        super(SpawnEvent, self).__init__(name)
        self.enemies = enemies
        self.location = location
    def spawn():
        pass

class SoundEvent(GameEvent):
    def __init__(self, name, sound):
        super(SoundEvent, self).__init__(name):
        self.sound = sound

class PhoneEvent(SoundEvent):
    def __init__(self, name, sound):
        super(PhoneEvent, self).__init__(name, sound)
        

class WaitEvent(GameEvent):
    def __init__(self, name, time):
        super(WaitEvent, self).__init__(name):
        self.time = time

class ConditionEvent(GameEvent):
    def __init(self, name, condition):
        super(ConditionEvent, self).__init__(name)
        self.condition = condition
