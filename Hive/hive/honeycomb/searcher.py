import pika
from hive.common.rpcsender import RPCSender
from hive.common.longrunningproc import Proc
import time
import json

import sys, os, lucene, threading, time
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexReader
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import QueryParser

class Searcher(Proc):

    def __init__(self, config, query):
        Proc.__init__(self, config)
        self.connection = None
        self.channel = None
        self.queue = None
        self.running = True
        self.query = query

    def getQueue(self):
      return self.queue

    def run(self):
        credentials = pika.PlainCredentials(
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config['Rabbit']['host'], credentials=credentials))
        self.channel = self.connection.channel()

        # Setup queue for outputing data
        result = self.channel.queue_declare()
        self.queue = result.method.queue

        lucene.initVM()
        self.indexdir = "IndexOfLogs"
        self.d = SimpleFSDirectory(File(self.indexdir))
        self.analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        dr = DirectoryReader.open(self.d)

        self.ready.set()

        while self.running:
            ndr = DirectoryReader.openIfChanged(dr)
            if ndr is not None:
              dr = ndr

            searcher = IndexSearcher(dr)
            pq = QueryParser(Version.LUCENE_30, "id", self.analyzer).parse(self.query)
            hits = searcher.search(pq, 1000)

            results = []
            for hit in hits.scoreDocs:
              doc = searcher.doc(hit.doc)
              record = doc.get("id")
              results.append(record)

            respon = json.dumps(results)

            self.channel.basic_publish(exchange='', routing_key=self.queue, body=respon)
            time.sleep(1)
        
        self.connection.close()

    def stop(self):
        running = False
