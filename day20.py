from collections import deque
from functools import reduce

def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)


def multi_lcm(*args):
    """Return lcm of args."""
    return reduce(lcm, args)

class Module():
    def __init__(self, name) -> None:
        self.name = name
        self.mode = None
        self.destinations = []
        self.inputs = []
        self.on_off_state = ""
        self.memory = {}

    def config(self, mode, destinations):
        self.mode = mode
        self.destinations = destinations[:]
        if self.mode == "%":
            self.on_off_state = "off"
        if self.mode == "&":
            self.memory = {}
    
    def plug(self, input):
        self.inputs.append(input)
        if self.mode == "&":
            self.memory[input] = "L"

    def process(self, input, signal):
        if self.mode == "%":  # Flip flop
            if signal == "L":
                if self.on_off_state == "off":
                    self.on_off_state = "on "
                    return [("H", dest, self.name) for dest in self.destinations]
                else:
                    self.on_off_state = "off"
                    return [("L", dest, self.name) for dest in self.destinations]
            else:
                return []
        if self.mode == "&":
            self.memory[input] = signal
            if any([self.memory[i] == "L" for i in self.memory.keys()]):
                return [("H", dest, self.name) for dest in self.destinations]
            return [("L", dest, self.name) for dest in self.destinations]
        if self.mode == "b":
            return [(signal, dest, self.name) for dest in self.destinations]
        return []
    
    def state(self):
        return self.name + ":" + self.on_off_state + "|" + str(self.memory)
    
    def compact_state(self):
        if self.on_off_state != "":
            return "1" if self.on_off_state == "on " else "0"
        else:
            return "".join([ "1" if v == "H" else "0" for v in self.memory.values()])
    


class Machine():
    def __init__(self) -> None:
        self.configuration = {}
        self.history = []
        self.queue = deque()
        self.score = {"H": 0, "L": 0}
        self.has_looped = False

    def add(self, module: Module):
        self.configuration[module.name] = module

    def state(self):
        return ",".join([self.configuration[m].state() for m in self.configuration.keys()])
    
    def compact_state(self):
        return "".join([self.configuration[m].compact_state() for m in self.configuration.keys()])
    
    def initialize(self):
        for m in self.configuration.keys():
            for d in self.configuration[m].destinations:
                if d in self.configuration:
                    self.configuration[d].plug(m)

    def save_history(self):
        if (not self.has_looped) and self.state() in self.history:
            print("History repeats itself after:", len(self.history))
            self.has_looped = True
        self.history.append(self.state())

    def process(self, debug = False, part2 = False):
        self.queue.append(("L", "broadcaster", "button"))
        #self.score["L"] += 1
        while len(self.queue) > 0:
            (signal, dest, src) = self.queue.popleft()
            if debug:
                print(src, "-", signal, "->", dest)
            self.score[signal] += 1
            if dest in self.configuration:
                result = self.configuration[dest].process(src, signal)
                for r in result:
                    self.queue.append(r)
            elif part2:  # output or rx
                if signal == "L":
                    return False
        return True


    def total_score(self):
        return self.score["L"] * self.score["H"]


with open('input/input20.txt', 'r') as f:
    data = f.read().splitlines()

machine = Machine()
modules = {"broadcaster":Module("broadcaster")}
for row in data:
    current = row.split(" -> ")
    a = current[0]
    mode = None
    if a[0] in ["%", "&"]:
        mode = a[0]
        a = a[1:]
    else:
        mode = "b"
    if a not in modules:
        modules[a] = Module(a)
    destinations = []
    for dest in current[1].split(", "):
        destinations.append(dest)

    modules[a].config(mode, destinations)

for m in modules.values():
    machine.add(m)

machine.initialize()
print(machine.state())
machine.save_history()
for i in range(1000):
    machine.process()
    machine.save_history()
    #print(machine.state())

print("Partie 1:", machine.total_score())

machine = Machine()
modules = {"broadcaster":Module("broadcaster")}
for row in data:
    current = row.split(" -> ")
    a = current[0]
    mode = None
    if a[0] in ["%", "&"]:
        mode = a[0]
        a = a[1:]
    else:
        mode = "b"
    if a not in modules:
        modules[a] = Module(a)
    destinations = []
    for dest in current[1].split(", "):
        destinations.append(dest)

    modules[a].config(mode, destinations)

for m in modules.values():
    machine.add(m)

machine.initialize()
i = 0
state = []

# Find parent of rx:

for m in machine.configuration:
    if "rx" in machine.configuration[m].destinations:
        parent = m

# Find the parents of that one, then the big node above
nodes = [machine.configuration[k].inputs[0] for k in machine.configuration[parent].inputs]
values = []
for node in nodes:
    memory = [node]
    for output in machine.configuration[node].destinations:
        memory.append(output)
    for input in machine.configuration[node].inputs:
        if input not in memory:
            memory.append(input)
    machine = Machine()
    modules = {"broadcaster":Module("broadcaster")}
    for row in data:
        current = row.split(" -> ")
        a = current[0]
        mode = None
        if a[0] in ["%", "&"]:
            mode = a[0]
            a = a[1:]
        else:
            mode = "b"
        if a not in modules:
            modules[a] = Module(a)
        destinations = []
        for dest in current[1].split(", "):
            destinations.append(dest)

        modules[a].config(mode, destinations)

    for m in modules.values():
        machine.add(m)

    machine.initialize()

    i = 0
    state = []

    while machine.process(part2=True):
        i += 1
        st = "".join([machine.configuration[x].compact_state() for x in memory])
        if st not in state:
            state.append(st)    
        else:
            break
    values.append(i-1)
    
print("Partie 2", multi_lcm(*values))

