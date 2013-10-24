import sqlite3

class Agent(object):

    def __init__(self, id, heartbeat, dead=False):
        self.id = id
        self.dead = dead
        self.heartbeat = heartbeat

class AgentModel(object):

    def __init__(self, config):
        self.conn = sqlite3.connect(config['Database']['filepath'])
        self.c = self.conn.cursor()
        self.c.execute('''create table if not exists Agents(
                UUID TEXT PRIMARY KEY NOT NULL, 
                DEAD INT NOT NULL, 
                HEARTBEAT REAL NOT NULL)''')

    def new(self, id, heartbeat):
        return Agent(id, heartbeat)

    def save(self, agent):
        self.c.execute("SELECT * FROM Agents WHERE UUID=?", (agent.id, ))
        one = self.c.fetchone()
        if one == None:
            self.c.execute("INSERT INTO Agents VALUES (?, ?, ?)", (agent.id, agent.dead, agent.heartbeat))
        else: 
            self.c.execute("UPDATE Agents SET DEAD=?, HEARTBEAT=?  WHERE UUID=?", (agent.dead, agent.heartbeat, agent.id))
        self.conn.commit()

    def findAll(self):
        agents = {}
        for row in self.c.execute("SELECT * FROM Agents"):
            agents[row[0]] = Agent(row[0], row[2], row[1])
        print agents
        return agents

    def delete(self, agent):
        t = (agent.id, )
        self.c.execute("DELETE FROM Agents WHERE UUID=?", t)
        self.conn.commit()

    def find(self, id):
        t = (id, )
        self.c.execute("SELECT * FROM Agents WHERE UUID=?", t)
        one = self.c.fetchone()
        if one == None:
            return None
        else:
            return Agent(one[0], one[2], one[1]) 
