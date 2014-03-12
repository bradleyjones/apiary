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

class Driver(object):

    def __init__(self, config, tablename):
        self.env = lucene.getVMEnv()
        self.env.attachCurrentThread()
        self.config = config
        self.indexdir = "IndexOf%s" % tablename
        self.d = SimpleFSDirectory(File(self.indexdir))
        self.analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        self.conf = IndexWriterConfig(Version.LUCENE_CURRENT, self.analyzer)

        self.fieldType1 = FieldType()
        self.fieldType1.setIndexed(True)
        self.fieldType1.setStored(False)
        self.fieldType1.setTokenized(True)

        self.fieldType2 = FieldType()
        self.fieldType2.setIndexed(True)
        self.fieldType2.setStored(True)
        self.fieldType2.setTokenized(False)

    def rebuildIndex(self, fields, records):
        writer = IndexWriter(
            self.d, self.conf.setOpenMode(IndexWriterConfig.OpenMode.CREATE))

        for record in records:
          doc = self.buildDocument(fields, record)
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
            print "YO MAMA"
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


    def index(self, fields, record):
        writer = IndexWriter(
            self.d, self.conf)

        doc = self.buildDocument(fields, record)
        writer.addDocument(doc)

        writer.commit()
        writer.close()

    def updateindex(self, fields, record):
        writer = IndexWriter(
            self.d, self.conf)

        doc = self.buildDocument(fields, record)
        writer.updateDocument(lucene.Term("_id", record['_id']), doc)

        writer.optimize()
        writer.close()

    def removeindex(self, record):
        writer = IndexWriter(
            self.d, self.conf)

        writer.deleteDocuments(lucene.Term("_id", record['_id']))

        writer.optimize()
        writer.close()

    def query(self, query):
        searcher = IndexSearcher(DirectoryReader.open(self.d))
        query = QueryParser(Version.LUCENE_30, "id", self.analyzer).parse(query)
        hits = searcher.search(query, 1000)

        results = {}
        
        results['totalHits'] = hits.totalHits
        results['hits'] = []

        for hit in hits.scoreDocs:
            record = {}
            doc = searcher.doc(hit.doc)
            record['score'] = hit.score
            fields = doc.getFields()
            for field in fields:
                record[field.name()] = field.stringValue()
            results['hits'].append(record)

        return results
