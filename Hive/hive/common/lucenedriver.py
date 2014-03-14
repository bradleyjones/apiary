import sys, os, lucene, threading, time
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader

from multiprocessing import Process 
import pika
from hive.common.rpcsender import RPCSender
import json

def setup(config, workers=4):
    for x in range(0, workers):
        worker = Worker(config)
        worker.start()

class Worker(Process):

    def __init__(self, config): 
        Process.__init__(self)
        self.config = config
        self.connection = None
        self.channel = None

    def run(self):
        print "Booting lucene driver worker...."
        lucene.initVM()
        
        self.fieldType1 = FieldType()
        self.fieldType1.setIndexed(True)
        self.fieldType1.setStored(False)
        self.fieldType1.setTokenized(True)

        self.fieldType2 = FieldType()
        self.fieldType2.setIndexed(True)
        self.fieldType2.setStored(True)
        self.fieldType2.setTokenized(False)

        credentials = pika.PlainCredentials(
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config['Rabbit']['host'], credentials=credentials))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='lucene-worker')    

        self.channel.basic_consume(self.on_message, queue='lucene-worker')
        self.channel.start_consuming()


    def on_message(self, channel, method, props, body): 
        da = json.loads(body)

        self.d = SimpleFSDirectory(File(da['data']['indexdir']))
        self.analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        self.conf = IndexWriterConfig(Version.LUCENE_CURRENT, self.analyzer)

        response = getattr(self, da['action'])(da['data'])
        if response is None:
            response = {}
        channel.basic_publish(exchange='',
                               routing_key=props.reply_to,
                               properties=pika.BasicProperties(
                                   correlation_id=props.correlation_id,
                               ),  
                               body=json.dumps(response))
        channel.basic_ack(delivery_tag=method.delivery_tag)
    
    def rebuildIndex(self, data):
        writer = IndexWriter(
            self.d, self.conf.setOpenMode(IndexWriterConfig.OpenMode.CREATE))

        for record in data['records']:
          doc = self.buildDocument(data['fields'], record)
          writer.addDocument(doc)

        writer.optimize()
        writer.close()

    def buildDocument(self, fields, record):
        doc = Document()
        doc.add(
            Field("id",
                  record["_id"],
                  self.fieldType2))
        for field in fields:
          if type(record[field]) is dict:
            self.dictToFields(doc, record[field])
          else: 
            doc.add(
                Field(field,
                      record[field],
                      self.fieldType1))

        return doc

    def dictToFields(self, doc, record):
        for key in record:
          if type(record[key]) is dict:
            self.dictToFields(doc, record[key])
          else: 
            doc.add(
                Field(key,
                      record[key],
                      self.fieldType1))

    def index(self, data):
        writer = IndexWriter(
            self.d, self.conf)

        doc = self.buildDocument(data['fields'], data['record'])
        writer.addDocument(doc)

        writer.commit()
        writer.close()

    def updateindex(self, data):
        writer = IndexWriter(
            self.d, self.conf)

        doc = self.buildDocument(data['fields'], data['record'])
        writer.updateDocument(lucene.Term("_id", data['record']['_id']), doc)

        writer.optimize()
        writer.close()

    def removeindex(self, data):
        writer = IndexWriter(
            self.d, self.conf)

        writer.deleteDocuments(lucene.Term("_id", data['record']['_id']))

        writer.optimize()
        writer.close()

    def query(self, data):
        searcher = IndexSearcher(DirectoryReader.open(self.d))
        query = QueryParser(Version.LUCENE_30, "id", self.analyzer).parse(data['query'])
        hits = searcher.search(query, 1000)

        results = {}
        
        results['totalHits'] = hits.totalHits
        results['hits'] = {}

        for hit in hits.scoreDocs:
            record = {}
            doc = searcher.doc(hit.doc)
            fields = doc.getFields()
            record['score'] = hit.score
            for field in fields:
              if field.name() != "id":
                record[field.name()] = field.stringValue()
            results['hits'][doc.get('id')] = record

        return results

class Driver(object):

    def __init__(self, config, tablename):
        self.config = config
        self.indexdir = "IndexOf%s" % tablename
        self.sender = RPCSender(self.config)

    def rebuildIndex(self, fields, records):
        data = { 'indexdir': self.indexdir, 'fields': fields, 'records': records }
        return json.loads(self.sender.send_request('rebuildIndex', 'lucene-driver', data, '', '', key='lucene-worker'))

    def index(self, fields, record):
        data = { 'indexdir': self.indexdir,'fields': fields, 'record': record }
        return json.loads(self.sender.send_request('index', 'lucene-driver', data, '', '', key='lucene-worker'))

    def updateindex(self, fields, record):
        data = { 'indexdir': self.indexdir, 'fields': fields, 'record': record }
        return json.loads(self.sender.send_request('updateindex', 'lucene-driver', data, '', '', key='lucene-worker'))

    def removeindex(self, record):
        data = { 'indexdir': self.indexdir, 'fields': fields, 'record': record }
        return json.loads(self.sender.send_request('removeindex', 'lucene-driver', data, '', '', key='lucene-worker'))

    def query(self, query):
        data = { 'indexdir': self.indexdir, 'query': query }
        return json.loads(self.sender.send_request('query', 'lucene-driver', data, '', '', key='lucene-worker'))
