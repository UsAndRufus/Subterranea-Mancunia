#Not an event as in input event in PyGame's event queue
#Rather a "game event" - e.g. spawn enemies, play sounds etc

class GameEvent(object):
    def __init__(self, name):
        self.name = name
        self.finished = False
        self.running = False

    def run(self):
        print(self.name)
        self.finished = True
        self.running = True
        
class SpawnEvent(GameEvent):
    def __init__(self, name, enemies):
        super(SpawnEvent, self).__init__(name)
        self.enemies = enemies
    def spawn():
        pass

class SoundEvent(GameEvent):
    def __init__(self, name, sound):
        super(SoundEvent, self).__init__(name)
        self.sound = sound

class PhoneEvent(SoundEvent):
    def __init__(self, name, sound):
        super(PhoneEvent, self).__init__(name, sound)
        

class WaitEvent(GameEvent):
    def __init__(self, name, time):
        super(WaitEvent, self).__init__(name)
        self.time = time

class ConditionEvent(GameEvent):
    def __init__(self, name, condition):
        super(ConditionEvent, self).__init__(name)
        self.condition = condition
