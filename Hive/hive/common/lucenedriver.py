import lucene
from lucene import \
    SimpleFSDirectory, System, File, \
    Document, Field, StandardAnalyzer, IndexWriter, Version

class Driver(object):

  def __init__(self): 
    lucene.initVM()
    self.indexdir = "indexfile"
    self.d = SimpleFSDirectory(File(indexDir))
    self.analyzer = StandardAnalyzer(Version.LUCENE_30)

  def buildDocument(self, fields, record):
    doc = Document()
    doc.add(Field("text", record["_id"], Field.Store.YES, Field.Index.ANALYZED))
    for field in fields:
      doc.add(Field("text", record[field], Field.Store.YES, Field.Index.ANALYZED))
    return doc

  def index(self, fields, record):
    writer = IndexWriter(self.d, self.analyzer, True, IndexWriter.MaxFieldLength(512))

    doc = self.buildDocument(fields, record)
    writer.addDocument(doc)

    writer.optimize()
    writer.close()

  def updateindex(self, fields, record):
    writer = IndexWriter(self.d, self.analyzer, True, IndexWriter.MaxFieldLength(512))

    doc = self.buildDocument(fields, record)
    writer.updateDocument(lucene.Term("_id", record['_id']), doc)

    writer.optimize()
    writer.close()

  def removeindex(self, record):
    writer = IndexWriter(self.d, self.analyzer, True, IndexWriter.MaxFieldLength(512))

    writer.deleteDocuments(lucene.Term("_id", record['_id']))

    writer.optimize()
    writer.close()

  def query(self, query, fields):
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
