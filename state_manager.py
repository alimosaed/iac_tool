import sqlite3
import json

class StateManager:
    def __init__(self, db_file='iac_state.db'):
        self.db_file = db_file
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                config TEXT NOT NULL,
                UNIQUE(type, name)
            )
        ''')
        conn.commit()
        conn.close()

    def load_state(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT type, name, config FROM resources")
        rows = cursor.fetchall()
        conn.close()

        state = {}
        for row in rows:
            resource_type, name, config = row
            if resource_type not in state:
                state[resource_type] = {}
            state[resource_type][name] = json.loads(config)
        return state

    def save_state(self, resources):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        for resource in resources:
            resource_type = resource['type']
            name = resource['name']
            config = json.dumps(resource['config'])
            
            cursor.execute('''
                INSERT OR REPLACE INTO resources (type, name, config)
                VALUES (?, ?, ?)
            ''', (resource_type, name, config))
        
        conn.commit()
        conn.close()

    def remove_resource(self, resource_type, name):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM resources WHERE type = ? AND name = ?", (resource_type, name))
        conn.commit()
        conn.close()

    def get_resource(self, resource_type, name):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT config FROM resources WHERE type = ? AND name = ?", (resource_type, name))
        row = cursor.fetchone()
        conn.close()

        if row:
            return json.loads(row[0])
        return None