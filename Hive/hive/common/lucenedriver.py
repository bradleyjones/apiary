import lucene
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

from multiprocessing import Process, Manager
import json
import uuid

luceneManager = None
luceneQueue = None
luceneReturn = None


def setup(config, workers=4):
    global luceneQueue, luceneManager, luceneReturn
    luceneManager = Manager()
    luceneQueue = luceneManager.Queue()
    luceneReturn = luceneManager.dict()
    for x in range(0, workers):
        worker = Worker(config, luceneQueue, luceneReturn)
        worker.start()


class Worker(Process):

    def __init__(self, config, queue, ret):
        Process.__init__(self)
        self.config = config
        self.connection = None
        self.channel = None
        self.queue = queue
        self.ret = ret

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

        while(True):
            data = self.queue.get()
            da = data[1]
            response = None
            try:
                self.d = SimpleFSDirectory(File(da['data']['indexdir']))
                self.analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
                self.conf = IndexWriterConfig(
                    Version.LUCENE_CURRENT,
                    self.analyzer)

                response = getattr(self, da['action'])(da['data'])
                self.d.close()
            except:
                pass
            if response is None:
                response = {}

            self.ret[data[0]] = response

    def rebuildIndex(self, data):
        writer = IndexWriter(
            self.d, self.conf.setOpenMode(IndexWriterConfig.OpenMode.CREATE))

        for record in data['records']:
            doc = self.buildDocument(data['fields'], record)
            writer.addDocument(doc)

        writer.commit()
        writer.close()

    def buildDocument(self, fields, record):
        doc = Document()
        doc.add(
            Field("id",
                  record["_id"],
                  self.fieldType2))
        for field in fields:
            if isinstance(record[field], dict):
                self.dictToFields(doc, record[field])
            else:
                doc.add(
                    Field(field,
                          record[field],
                          self.fieldType1))

        return doc

    def dictToFields(self, doc, record):
        for key in record:
            if isinstance(record[key], dict):
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
        query = QueryParser(
            Version.LUCENE_30,
            "id",
            self.analyzer).parse(
            data['query'])
        hits = searcher.search(query, 100000)

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
        global luceneQueue, luceneManager, luceneReturn
        self.config = config
        self.indexdir = "IndexOf%s" % tablename
        if luceneQueue is None:
            raise Exception("Run lucenedriver.setup() first!")

    def _sendMessage(self, data):
        id = str(uuid.uuid4())
        luceneQueue.put([id, data])
        while(not (id in luceneReturn)):
            pass
        return luceneReturn.pop(id)

    def rebuildIndex(self, fields, records):
        data = {
            'action': 'rebuildIndex',
            'data': {
                'indexdir': self.indexdir,
                'fields': fields,
                'records': records}}
        return self._sendMessage(data)

    def index(self, fields, record):
        data = {
            'action': 'index',
            'data': {
                'indexdir': self.indexdir,
                'fields': fields,
                'record': record}}
        return self._sendMessage(data)

    def updateindex(self, fields, record):
        data = {
            'action': 'updateindex',
            'data': {
                'indexdir': self.indexdir,
                'fields': fields,
                'record': record}}
        return self._sendMessage(data)

    def removeindex(self, record):
        data = {
            'action': 'removeindex',
            'data': {
                'indexdir': self.indexdir,
                'fields': fields,
                'record': record}}
        return self._sendMessage(data)

    def query(self, query):
        data = {
            'action': 'query',
            'data': {
                'indexdir': self.indexdir,
                'query': query}}
        return self._sendMessage(data)
