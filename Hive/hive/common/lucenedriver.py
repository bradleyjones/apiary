import sys, os, lucene, threading, time
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

class Driver(object):

    def __init__(self, config, tablename):
        lucene.initVM()
        self.config = config
        self.indexdir = "IndexOf%s" % tablename
        self.d = SimpleFSDirectory(File(self.indexdir))
        self.analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

        self.fieldType1 = FieldType()
        self.fieldType1.setIndexed(True)
        self.fieldType1.setStored(False)
        self.fieldType1.setTokenized(True)

        self.fieldType2 = FieldType()
        self.fieldType2.setIndexed(True)
        self.fieldType2.setStored(True)
        self.fieldType2.setTokenized(False)

    def buildDocument(self, fields, record):
        doc = Document()
        doc.add(
            Field("text",
                  record["_id"],
                  self.fieldType2))
        for field in fields:
            doc.add(
                Field("text",
                      record[field],
                      self.fieldType1))
        return doc

    def index(self, fields, record):
        conf = IndexWriterConfig(Version.LUCENE_CURRENT, self.analyzer)
        writer = IndexWriter(
            self.d, conf)

        doc = self.buildDocument(fields, record)
        writer.addDocument(doc)

        writer.commit()
        writer.close()

    def updateindex(self, fields, record):
        conf = IndexWriterConfig(Version.LUCENE_CURRENT, self.analyzer)
        writer = IndexWriter(
            self.d, conf)

        doc = self.buildDocument(fields, record)
        writer.updateDocument(lucene.Term("_id", record['_id']), doc)

        writer.optimize()
        writer.close()

    def removeindex(self, record):
        writer = IndexWriter(
            self.d,
            self.analyzer,
            True,
            IndexWriter.MaxFieldLength(512))

        writer.deleteDocuments(lucene.Term("_id", record['_id']))

        writer.optimize()
        writer.close()

    def query(self, query):
        searcher = IndexSearcher(self.d)
        query = QueryParser(Version.LUCENE_30, "text", analyzer).parse(query)
        hits = searcher.search(query, 1000)

        results = []

        for hit in hits.scoreDocs:
            record = {}
            doc = searcher.doc(hit.doc)
            for field in fields:
                record[field] = doc.get(field).encode("utf-8")
            results.append(record)

        return results
