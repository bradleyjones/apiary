import json
from ..common.controller import Controller as Parent
from ..common.simplepublisher import SimplePublisher
from worker import Worker
from alerter import Alerter
from hive.common.longrunningproc import ProcHandler


class Controller(Parent):

    def models(self):
        self.workers = Worker(self.config)

    # BELOW THIS LINE ARE ALL CONTROLLER ACTIONS

    def new(self, body, resp):
        searcher = self.searchers.new()

        sender = RPCSender(self.config, channel=self.channel)
        r = sender.channel.queue_declare()
        q = r.method.queue

        machine = ProcHandler(
            self.config,
            Alerter(
                self.config,
                msg['data']['query'],
                msg['data']['time'],
                msg['data']['quantity']),
            q)
        machine.start()

        searcher.OUTPUTQUEUE = sender.send_request(
            'QUEUE',
            'hive',
            '',
            '',
            '',
            key=q)
        searcher.CONTROLQUEUE = q
        searcher.QUERY = msg['data']['query']
        searcher.TIME = msg['data']['time']
        searcher.QUANTITY = msg['data']['quantity']

        self.searchers.save(searcher)

        resp.respond(searcher.OUTPUTQUEUE)

    def delete(self, body, resp):
        worker = self.workers.find(body.data)
        pub = SimplePublisher(
            ''. self.config['Rabbit']['host'],
            self.config['Rabbit']['username'],
            self.config['Rabbit']['passwords'])
        pub.publish_msg(self, 'STOP', work.CONTROLQUEUE)

        resp.respond('DELETED')
