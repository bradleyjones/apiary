import sqlite3


class Agent(object):

    def __init__(self, id, heartbeat, dead=False, authenticated=False):
        self.id = id
        self.dead = dead
        self.authenticated = authenticated
        self.heartbeat = heartbeat


class AgentModel(object):

    def __init__(self, config):
        self.conn = sqlite3.connect(config['Database']['filepath'])
        self.c = self.conn.cursor()
        self.c.execute('''create table if not exists Agents(
                UUID TEXT PRIMARY KEY NOT NULL,
                AUTHENTICATED INT NOT NULL,
                DEAD INT NOT NULL,
                HEARTBEAT REAL NOT NULL)''')

    def new(self, id, heartbeat):
        return Agent(id, heartbeat)

    def save(self, agent):
        self.c.execute("SELECT * FROM Agents WHERE UUID=?", (agent.id, ))
        one = self.c.fetchone()
        if one is None:
            self.c.execute(
                "INSERT INTO Agents VALUES (?, ?, ?, ?)",
                (agent.id,
                 agent.authenticated,
                 agent.dead,
                 agent.heartbeat))
        else:
            self.c.execute(
                "UPDATE Agents SET DEAD=?, HEARTBEAT=?, AUTHENTICATED=? WHERE UUID=?",
                (agent.dead,
                 agent.heartbeat,
                 agent.authenticated,
                 agent.id))
        self.conn.commit()

    def findAll(self):
        agents = {}
        for row in self.c.execute("SELECT UUID, HEARTBEAT, DEAD, AUTHENTICATED FROM Agents"):
            agents[row[0]] = Agent(row[0], row[1], row[2], row[3])
        return agents

    def delete(self, agent):
        t = (agent.id, )
        self.c.execute("DELETE FROM Agents WHERE UUID=?", t)
        self.conn.commit()

    def find(self, id):
        t = (id, )
        self.c.execute("SELECT UUID, HEARTBEAT, DEAD, AUTHENTICATED FROM Agents WHERE UUID=?", t)
        row = self.c.fetchone()
        if row is None:
            return None
        else:
            print row
            return Agent(row[0], row[1], row[2], row[3])
