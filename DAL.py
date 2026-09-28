import mysql.connector
import logging

logger = logging.getLogger(__name__)

class DB_DAL_Connection:
    def __init__(self, states_user, states_password, states_host='localhost', states_port=3306):
        """Args:
            states_user: Your user name when logging into workbench.
            states_password: Your password when logging into workbench.
            states_host: Your host name or host ip address when logging into workbench.
            states_port: The port number you use to log into workbench.
            
        Attributes: 
            self.connection: The connection to the 'generic_game_states' database. This database is created in 'states_of_games_DB.sql'.
            self.cursor: The database cursor returned by mysql.connector.
        
        Methods: connect(), close()
        
        This class manages the connection to the database."""
        self.host = states_host
        self.port = states_port
        self.db = 'generic_game_states'
        self.user = states_user
        self.password = states_password
        self.connection = None
        self.cursor = None

    def connect(self):
        """Returns:
            self.connection: Connection to the 'generic_game_states' database
            self.cursor: Database cursor returned by mysql.connector
        
        This method connects to the database, and it returns the connection and cursor objects."""
        try:
            self.connection = mysql.connector.connect(host = self.host, port = self.port, database = self.db, user = self.user, password = self.password)
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as e:
            logger.error(f"Database connection failed: {e}")
            self.connection = None
            self.cursor = None
        
        return self.connection, self.cursor
    
    def close(self):
        """This method closes the database connection once it is no longer needed."""
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.connection is not None:
            self.connection.close()
            self.connection = None

class DAL_Procedure_Engine:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    def call_procedure(self, procedure_name, params = None):
        if self.cursor is None:
            return None, None
        
        parameters = params or []
        
        try:
            self.cursor.callproc(procedure_name, parameters)
            for result in self.cursor.stored_results():
                headers = [column[0] for column in result.description]
                records = result.fetchall()
                return headers, records
            logger.warning(f"Procedure '{procedure_name}' returned no result sets")
            return None, None
        except mysql.connector.Error as e:
            logger.error(f"Failed to call procedure '{procedure_name}': {e}")
            return None, None
    
    def call_procedure_no_results(self, procedure_name, params = None):
        if self.cursor is None or self.connection is None:
            return False
        
        parameters = params or []
        try:
            self.cursor.callproc(procedure_name, parameters)
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            logger.error(f"Failed to call procedure '{procedure_name}': {e}")
            self.connection.rollback()
            return False

class Players_DAL:
    def __init__(self, connection, cursor):
        self.Procedure_Engine = DAL_Procedure_Engine(connection, cursor)
    
    def display_players(self):
        return self.Procedure_Engine.call_procedure("get_players_view")
    
    def get_all_players(self):
        return self.Procedure_Engine.call_procedure("get_players")
    
    def create_player(self, player_ID, name):
        return self.Procedure_Engine.call_procedure_no_results("new_player", [player_ID, name])
    
    def get_player_from_characterID(self, character_ID):
        return self.Procedure_Engine.call_procedure("get_player_name_from_characterID", [character_ID])
        

class Characters_DAL:
    def __init__(self, connection, cursor):
        self.Procedure_Engine = DAL_Procedure_Engine(connection, cursor)
    
    def display_characters(self):
        return self.Procedure_Engine.call_procedure("get_characters_view")
    
    def get_all_characters(self):
        return self.Procedure_Engine.call_procedure("get_characters")
    
    def create_character(self, character_ID, character_name, player_ID):
        return self.Procedure_Engine.call_procedure_no_results("new_character", [character_ID, character_name, player_ID])
    
    def get_playerID(self, player_name):
        return self.Procedure_Engine.call_procedure("call_get_player_ID", [player_name])
    
    def get_character_name_from_id(self, character_ID):
        return self.Procedure_Engine.call_procedure("call_get_character_name", [character_ID])

class Game_States_DAL:
    def __init__(self, connection, cursor):
        self.Procedure_Engine = DAL_Procedure_Engine(connection, cursor)

    def get_characterID(self, character_name):
        return self.Procedure_Engine.call_procedure("call_get_character_ID", [character_name])

    def create_game_state(self, todays_date, character_ID):
        return self.Procedure_Engine.call_procedure_no_results("new_game_state", [todays_date, character_ID])
    
    def get_state_list(self):
        return self.Procedure_Engine.call_procedure("get_game_state_list")
    
    def get_filtered_state_list(self):
        return self.Procedure_Engine.call_procedure("get_filtered_game_state_list")
    
    def get_next_game_state(self, system_date, character_ID, turn):
        return self.Procedure_Engine.call_procedure("get_game_state", [system_date, character_ID, turn])
    
    def get_next_filtered_game_state(self, system_date, character_ID, turn):
        return self.Procedure_Engine.call_procedure("get_filtered_game_state", [system_date, character_ID, turn])
    
    def get_raw_game_state(self, system_date, character_ID, turn):
        return self.Procedure_Engine.call_procedure("get_raw_game_state", [system_date, character_ID, turn])

    def create_filtered_state(self, system_date, characterID, turn, starve, subsistence, overland_speed,
                           doors=0, traps=0, treasure=0, cursed=0, disease=0, poison=0, condition1=None, condition2=None):
        self.Procedure_Engine.call_procedure_no_results("new_filtered_game_state",
        [system_date, characterID, turn, starve, subsistence, overland_speed, doors, traps, treasure, cursed, disease, poison, condition1, condition2])

class States_Updater_DAL:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor  
        self.Procedure_Engine = DAL_Procedure_Engine(connection, cursor)
        
    def turn(self, new_turn, system_date, character_ID, turn_number):
        self.Procedure_Engine.call_procedure_no_results("update_turn", [new_turn, system_date, character_ID, turn_number])
    
    def subsistence(self, system_date, character_ID, turn):
        self.Procedure_Engine.call_procedure_no_results("increase_subsistence", [system_date, character_ID, turn])
    
    def condition(self, new_condition, system_date, character_ID, turn):
        self.Procedure_Engine.call_procedure_no_results("update_condition", [new_condition, system_date, character_ID, turn])
    
    def affliction(self, new_affliction, system_date, character_ID, turn):
        self.Procedure_Engine.call_procedure_no_results("update_affliction", [new_affliction, system_date, character_ID, turn])
    
    def secret_doors(self, system_date, character_ID, turn):
        self.Procedure_Engine.call_procedure_no_results("update_secret_doors", [system_date, character_ID, turn])
    
    def filtered_secret_doors(self, system_date, character_ID, turn):
        self.Procedure_Engine.call_procedure_no_results("update_filtered_secret_doors", [system_date, character_ID, turn])
    
    def secret_traps(self, system_date, character_ID, turn):
        self.Procedure_Engine.call_procedure_no_results("update_secret_traps", [system_date, character_ID, turn])
    
    def filtered_secret_traps(self, system_date, character_ID, turn):
        self.Procedure_Engine.call_procedure_no_results("update_filtered_secret_traps", [system_date, character_ID, turn])
    
    def secret_treasure(self, system_date, character_ID, turn):
        self.Procedure_Engine.call_procedure_no_results("update_secret_treasure", [system_date, character_ID, turn])
    
    def filtered_secret_treasure(self, system_date, character_ID, turn):
        self.Procedure_Engine.call_procedure_no_results("update_filtered_secret_treasure", [system_date, character_ID, turn])
    
    def secret_cursed_treasure(self, system_date, character_ID, turn):
        self.Procedure_Engine.call_procedure_no_results("update_secret_cursed_treasure", [system_date, character_ID, turn])
    
    def filtered_secret_cursed_treasure(self, system_date, character_ID, turn):
        self.Procedure_Engine.call_procedure_no_results("update_filtered_secret_cursed_treasure", [system_date, character_ID, turn])
    
    def secret_disease(self, system_date, character_ID, turn):
        self.Procedure_Engine.call_procedure_no_results("update_secret_airborne_disease", [system_date, character_ID, turn])
    
    def filtered_secret_disease(self, system_date, character_ID, turn):
        self.Procedure_Engine.call_procedure_no_results("update_filtered_secret_airborne_disease", [system_date, character_ID, turn])
    
    def secret_poison_gas(self, system_date, character_ID, turn):
        self.Procedure_Engine.call_procedure_no_results("update_secret_poison_gas", [system_date, character_ID, turn])
    
    def filtered_secret_poison_gas(self, system_date, character_ID, turn):
        self.Procedure_Engine.call_procedure_no_results("update_filtered_secret_poison_gas", [system_date, character_ID, turn])
    
    def overland_speed(self, system_date, character_ID, turn, new_overland_speed):
        self.Procedure_Engine.call_procedure_no_results("update_overland_speed", [system_date, character_ID, turn, new_overland_speed])
    
    def filtered_overland_speed(self, system_date, character_ID, turn, new_overland_speed):
        self.Procedure_Engine.call_procedure_no_results("update_filtered_overland_speed", [system_date, character_ID, turn, new_overland_speed])
    
    def carry_forward_secrets(self, system_date, character_ID, turn, doors, traps, treasure, cursed, disease, poison, condition1, condition2, affliction1, affliction2):
        self.Procedure_Engine.call_procedure_no_results("carry_forward_secrets", [system_date, character_ID, turn, doors, traps, treasure, cursed, disease, poison,
         condition1, condition2, affliction1, affliction2])