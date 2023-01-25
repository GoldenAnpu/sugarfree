import sqlite3


class States:
    start = 'start'
    main_menu = 'main_menu'
    getting_info = 'getting_info'
    converting_units = 'converting_units'
    converting_units_to_mmol = 'converting_units_to_mmol'
    converting_units_to_mg = 'converting_units_to_mg'


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('account_states.db')
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS states (user_id INTEGER PRIMARY KEY, state TEXT)''')
        self.conn.commit()

    def set_state(self, user_id: int, state: str):
        c = self.conn.cursor()
        if self.get_state(user_id) is not None:
            c.execute("UPDATE states SET state = ? WHERE user_id = ?", (state, user_id))
        else:
            c.execute("INSERT INTO states (user_id, state) VALUES (?, ?)", (user_id, state))
        self.conn.commit()

    def get_state(self, user_id: int):
        c = self.conn.cursor()
        c.execute("SELECT state FROM states WHERE user_id = ?", (user_id,))
        result = c.fetchone()
        return result[0] if result else None
