import pika
from hive.common.rpcsender import RPCSender
from hive.common.longrunningproc import Proc
import time

import sys, os, lucene, threading, time
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexReader
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version


class Searcher(Proc):

    def __init__(self, config, query):
        super(Proc).__init__(config)
        self.connection = None
        self.channel = None
        self.queue = None
        self.running = True
        self.query = query

    def run(self):
        credentials = pika.PlainCredentials(
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config['Rabbit']['host'], credentials=credentials))
        self.channel = self.connection.channel()

        # Setup queue for outputing data
        result = channel.queue_declare(exclusive=true)
        self.queue = result.method.queue
        
        lucene.initVM()
        self.indexdir = "IndexOfLogs"
        self.d = SimpleFSDirectory(File(self.indexdir))
        self.analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        dr = DirectoryReader.open(self.d)

        self.ready.set()

        while self.running:
            dr = DirectoryReader.openIfChanged(dr)
            searcher = IndexSearcher(dr)
            query = QueryParser(Version.LUCENE_30, "id", self.analyzer).parse(query)
            hits = searcher.search(query, 1000)

            results = []
            for hit in hits.scoreDocs:
              doc = searcher.doc(hit.doc)
              record = doc.get("id")
              results.append(record)

            self.channel.basic_publish(exchange='', routing_key=self.queue, body=results)
            time.sleep(1)
        
        self.connection.close()

    def stop(self):
        running = False
