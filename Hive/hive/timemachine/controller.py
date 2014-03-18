import json
from ..common.controller import Controller as Parent
from ..common.simplepublisher import SimplePublisher
from worker import Worker
from machine import Writer
from hive.common.longrunningproc import ProcHandler


class Controller(Parent):

    def models(self):
        self.workers = Worker(self.config)

    # BELOW THIS LINE ARE ALL CONTROLLER ACTIONS

    def new(self, body, resp):
        worker = self.workers.new()

        machine = ProcHandler(self.config, Writer(self.config))
        machine.start()

        worker.CONTROLQUEUE = machine.stopqueue
        worker.OUTPUTQUEUE = machine.subproc.queue

        self.workers.save(worker)

        resp.respond(worker.OUTPUTQUEUE)

    def delete(self, body, resp):
        worker = self.workers.find(body.data)
        pub = SimplePublisher(
            ''. self.config['Rabbit']['host'],
            self.config['Rabbit']['username'],
            self.config['Rabbit']['passwords'])
        pub.publish_msg(self, 'STOP', work.CONTROLQUEUE)

        resp.respond('DELETED')
