import threading
from time import sleep

class Monitor():
    def __init__(self):
        self.condition = list()
    
    def start(self, philosophers):
        self.philosophers = philosophers 
        for idx in range(5):
            self.condition.append(threading.Condition())
            self.philosophers[idx].start()

    def pickup(self, id):
        with self.condition[id]:
            self.checkDisponibility(id)
            if (self.philosophers[id].state != "COMENDO" ):
                self.condition[id].wait()

    def putdown(self, id):
        self.philosophers[id].state = "PENSANDO"

        self.checkDisponibility((id + 1) % 5) # vizinho do lado direito
        self.checkDisponibility((id + 4) % 5) # vizinho do lado esquerdo

    def checkDisponibility(self, id):
        if (self.philosophers[id].state == "FOME" \
                and self.philosophers[(id + 1) % 5].state != "COMENDO" \
                    and self.philosophers[(id + 4) % 5].state != "COMENDO"):
            
            self.philosophers[id].state = "COMENDO" 

            with self.condition[id]:
                self.condition[id].notify()


class Filosofo(threading.Thread):
    def __init__(self, id, monitor):
        threading.Thread.__init__(self)
        self.id = id 
        self.monitor = monitor 
        self.state = 'PENSANDO'

    def run(self):
        print("Filósofo %i esta pensando"% self.id)
        sleep(1)
        self.makeHungry()
        print("Filósofo %i comeu"% self.id)

    def makeHungry(self):
        self.state = "FOME"
        self.monitor.pickup(self.id)
        print("Filósofo %i esta comendo"%self.id)
        sleep(1)
        self.monitor.putdown(self.id)


if __name__ == "__main__":
    monitor = Monitor()
    filosofos = []

    for idx in range(5):
        filosofos.append(Filosofo(id = idx, monitor = monitor))

    monitor.start(filosofos)
