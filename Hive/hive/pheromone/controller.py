import json
from ..common.controller import Controller as Parent
from ..common.simplepublisher import SimplePublisher
from worker import Worker
from alerter import Alerter
from hive.common.longrunningproc import ProcHandler
from hive.common.rpcsender import RPCSender


class Controller(Parent):

    def models(self):
        self.workers = Worker(self.config)

    # BELOW THIS LINE ARE ALL CONTROLLER ACTIONS

    def new(self, msg, resp):
        worker = self.workers.new()

        sender = RPCSender(self.config)
        r = sender.channel.queue_declare()
        q = r.method.queue

        machine = ProcHandler(
            self.config,
            Alerter(
                self.config,
                msg['data']['query'],
                msg['data']['time'],
                msg['data']['quantity'],
                msg['data']['message'],
                msg['data']['user']),
            q)
        machine.start()

        req = json.loads(sender.send_request(
            'GET',
            'hive',
            {'variables':['uuid']},
            '',
            '',
            key=q))

        print req

        worker.UUID = req['uuid']
        worker.CONTROLQUEUE = q
        worker.QUERY = msg['data']['query']
        worker.TIME = msg['data']['time']
        worker.QUANTITY = msg['data']['quantity']
        worker.MESSAGE = msg['data']['message']

        self.workers.save(worker)

        resp.respond({'UUID': worker.UUID})

    def delete(self, body, resp):
        worker = self.workers.find(body.data)
        pub = SimplePublisher(
            ''. self.config['Rabbit']['host'],
            self.config['Rabbit']['username'],
            self.config['Rabbit']['passwords'])
        pub.publish_msg(self, 'STOP', work.CONTROLQUEUE)

        resp.respond('DELETED')
