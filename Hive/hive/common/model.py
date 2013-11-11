import sqlite3
from collections import OrderedDict


class ModelObject(object):

    def __init__(self, columns, primary, data=None):
        self.primary = primary
        pos = 0
        self.columns = columns
        for column, typ in columns.iteritems():
            if data is None:
                setattr(self, column, None)
            else:
                if typ is "BOOL":
                    setattr(self, column, bool(data[pos]))
                else:
                    setattr(self, column, data[pos])
                pos = pos + 1

    def to_hash(self):
        response = {}
        for column in self.columns:
            response[column] = getattr(self, column, None)
        return response


class Model(object):

    def __init__(self, config):
        self.conn = sqlite3.connect(config['Database']['filepath'])
        self.c = self.conn.cursor()
        self.columns = OrderedDict()
        self.primary = None
        self.tablename = self.__class__.__name__ + "s"
        self.define()
        self.migrate()

    def setprimary(self, name):
        if self.primary is not None:
            raise Exception("Primary already defined")

        if name in self.columns:
            self.primary = name
        else:
            raise Exception("Primary not in columns")

    def addcolumn(self, name, tpe):
        if name in self.columns:
            raise Exception("Can't have duplicate column names")
        self.columns[name] = tpe

    def migrate(self):
        query = '''create table if not exists ''' + self.tablename
        query = query + '('
        query = query + self.primary + " " + \
            self.columns[self.primary] + " NOT NULL"
        for key, typ in self.columns.iteritems():
            if typ is "BOOL":
                typ = "INT"
            if key is not self.primary:
                query = query + ", " + key + " " + typ + " NOT NULL"
        query = query + ')'
        self.c.execute(query)

    def define(self):
        raise NotImplementedError()

    def new(self):
        return ModelObject(self.columns, self.primary)

    def save(self, model):
        t = (self.primary, getattr(model, self.primary, None))
        self.c.execute("DELETE FROM '%s' WHERE ?=?" % self.tablename, t)
        one = self.c.fetchone()
        tup = ()
        query = ""
        if one is None:
            query = "INSERT INTO '%s' VALUES (" % self.tablename
            first = True
            for column in self.columns:
                if not first:
                    query = query + ', '
                else:
                    first = False
                query = query + '?'
                tup = tup + (getattr(model, column, None), )
            query = query + ')'
        else:
            query = "UPDATE '%s' SET " % self.tablename
            first = True
            for column in self.columns:
                if not first:
                    query = query + ', '
                else:
                    first = False
                query = query + '?=?'
                tup = tup + (column, getattr(model, column, None))
            query = query + " WHERE ?=? "
            tup = tup + (self.primary, getattr(model, self.primary, None))

        self.c.execute(query, tup)
        self.conn.commit()

    def delete(self, model):
        t = (self.primary, getattr(model, self.primary, None))
        self.c.execute("DELETE FROM %s WHERE ?=?" % self.tablename, t)
        self.conn.commit()

    def findAll(self):
        agents = {}
        for row in self.c.execute("SELECT * FROM '%s'" % self.tablename):
            agents[row[0]] = ModelObject(self.columns, self.primary, row)
        return agents

    def find(self, id):
        t = (id, )
        self.c.execute(
            "SELECT * FROM '%s' WHERE %s=?" %
            (self.tablename, self.primary), t)
        row = self.c.fetchone()
        if row is None:
            return None
        else:
            return ModelObject(self.columns, self.primary, row)
