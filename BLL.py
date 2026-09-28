import DAL
from datetime import date
import random
from decimal import Decimal

class DB_BLL_Connection:
    """Methods: __init__(), connect(), close()
    
    This class passes the request to connect and close the database connection from the GUI to the DAL. This step is necessary keep the
    application modular. The details of the DAL is abstracted from the BLL and the GUI. Extending the functionality of the application and
    code reuse is very efficient with this architecture."""
    def __init__(self, states_user, states_password, states_host, states_port):
        """Args:
            states_user: Your user name when logging into workbench.
            states_password: Your password when logging into workbench.
            states_host: Your host name or host ip address when logging into workbench.
            states_port: The port number you use to log into workbench."""
        
        self.DAL_Connection = DAL.DB_DAL_Connection(states_user, states_password, states_host, states_port)

    def connect(self):
        """This method requests the database connection from the DAL, and returns the resulting connection and cursor objects to the GUI."""
        return self.DAL_Connection.connect()
    
    def close(self):
        """This method sends the request to close the database connection to the DAL."""
        self.DAL_Connection.close()

class Players_BLL:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        
    def display_players(self):
        players_DAL = DAL.Players_DAL(self.connection, self.cursor)
        headers, records = players_DAL.display_players()
        return headers, records
    
    def create_player(self, name):
        players_DAL = DAL.Players_DAL(self.connection, self.cursor)
        headers, records = players_DAL.get_all_players()
        
        if headers is None:
            return False
        
        try:
            id_index = headers.index("player_ID")
        except ValueError:
            return False
        
        if records:
            
            max_id = max(int(row[id_index]) for row in records)           
            new_id = max_id + 1
        else:
            new_id = 1
        
        new_id_string = f"{new_id:02d}"
        
        return players_DAL.create_player(new_id_string, name)
    
    def get_player_name_from_character(self, character_ID):
        players_DAL = DAL.Players_DAL(self.connection, self.cursor)
        return players_DAL.get_player_from_characterID(character_ID)
        

class Characters_BLL:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    def display_characters(self):
        characters_DAL = DAL.Characters_DAL(self.connection, self.cursor)
        headers, records = characters_DAL.display_characters()
        return headers, records
    
    def create_character(self, character_name, player_name):
        characters_DAL = DAL.Characters_DAL(self.connection, self.cursor)

        player_headers, player_records = characters_DAL.get_playerID(player_name)
        if not player_records:
            return False
        player_ID = player_records[0][0]
        
        headers, records = characters_DAL.get_all_characters()
        if headers is None:
            return False
        
        try:
            id_index = headers.index("character_ID")
        except ValueError:
            return False
        
        if records:
            max_id = max(int(row[id_index]) for row in records)           
            new_id = max_id + 1
        else:
            new_id = 1
        new_id_string = f"{new_id:03d}"
        return characters_DAL.create_character(new_id_string, character_name, player_ID)
    
    def get_character_name(self, character_ID):
        characters_DAL = DAL.Characters_DAL(self.connection, self.cursor)
        return characters_DAL.get_character_name_from_id(character_ID) 
        

class Game_States_BLL:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        
    def get_todays_date(self):
        todays_date = date.today()
        sql_date = todays_date.strftime("%Y-%m-%d")
        return sql_date

    def create_states(self, character_name):
        today = self.get_todays_date()
        state_DAL = DAL.Game_States_DAL(self.connection, self.cursor)
        character_headers, character_records = state_DAL.get_characterID(character_name)
        if not character_records:
            return False
        character_ID = character_records[0][0]
        return state_DAL.create_game_state(today, character_ID)
    
    def get_next_state_to_filter(self):
        state_DAL = DAL.Game_States_DAL(self.connection, self.cursor)
        state_headers, state_records = state_DAL.get_state_list()
        filtered_headers, filtered_records = state_DAL.get_filtered_state_list()
        
        if state_headers is None or filtered_records is None:
            return None, None
        
        filtered_turns_by_character = {}
        for _, character_ID, turn in filtered_records:
            filtered_turns_by_character.setdefault(character_ID, set()).add(turn)
        
        candidates_by_character = {}
        for record in state_records:
            system_date, character_ID, turn = record
            if turn not in filtered_turns_by_character.get(character_ID, set()):
                candidates_by_character.setdefault(character_ID, []).append(record)
        
        for character_ID, candidates in candidates_by_character.items():
            candidates.sort(key = lambda r: r[2])
            return state_headers, candidates[0]
        return state_headers, None
    
    def display_next_game_state(self):
        state_headers, state_record = self.get_next_state_to_filter()

        if state_record is None:
            return None, None, None, None

        state_DAL = DAL.Game_States_DAL(self.connection, self.cursor)
        system_date, character_ID, turn = state_record[0], state_record[1], state_record[2]

        self._carry_forward_raw_secrets(character_ID, turn, system_date)

        display_headers, display_records = state_DAL.get_next_game_state(system_date, character_ID, turn)
        raw_headers, raw_records = state_DAL.get_raw_game_state(system_date, character_ID, turn)

        if not display_records or not raw_records:
            return None, None, None, None

        return display_headers, display_records[0], raw_headers, raw_records[0]

    def _carry_forward_raw_secrets(self, character_ID, turn, system_date):
        state_DAL = DAL.Game_States_DAL(self.connection, self.cursor)

        _, all_states = state_DAL.get_state_list()
        prev = next((r for r in (all_states or [])
                    if r[1] == character_ID and r[2] == turn - 1), None)
        if prev is None:
            return

        prev_headers, prev_records = state_DAL.get_raw_game_state(prev[0], prev[1], prev[2])
        if not prev_records:
            return
        prev_row = dict(zip(prev_headers, prev_records[0]))

        cur_headers, cur_records = state_DAL.get_raw_game_state(system_date, character_ID, turn)
        if not cur_records:
            return
        cur_row = dict(zip(cur_headers, cur_records[0]))

        secret_fields = ["secret_doors", "secret_traps", "secret_treasure", "secret_cursed_treasure", "secret_airborne_disease", "secret_poison_gas"]
        status_fields = ["condition1", "condition2", "affliction1", "affliction2"]

        if any(cur_row[f] != 0 for f in secret_fields) or any(cur_row[f] is not None for f in status_fields):
            return  

        state_updates = Update_States_BLL(self.connection, self.cursor)
        state_updates.carry_forward_secrets_updater(
        system_date, character_ID, turn,
        prev_row["secret_doors"], prev_row["secret_traps"], prev_row["secret_treasure"],
        prev_row["secret_cursed_treasure"], prev_row["secret_airborne_disease"], prev_row["secret_poison_gas"],
        prev_row["condition1"], prev_row["condition2"], prev_row["affliction1"], prev_row["affliction2"])
    
    def display_current_game_state(self, raw_values):
        system_date = raw_values.get("system_date")
        character_ID = raw_values.get("character_ID")
        turn = raw_values.get("turn")
        
        state_DAL = DAL.Game_States_DAL(self.connection, self.cursor)
        true_headers, true_records = state_DAL.get_next_game_state(system_date, character_ID, turn)
        filtered_headers, filtered_records = state_DAL.get_next_filtered_game_state(system_date, character_ID, turn)
        true_records.extend(filtered_records)
        return true_headers, true_records
        
    def create_filtered_game_state(self, raw_values):
        systemDate = raw_values.get("system_date")
        cID = raw_values.get("character_ID")
        turn_number = raw_values.get("turn")
        starvation = raw_values.get("starvation_mode")
        subsistence = raw_values.get("subsistence_level")
        speed = raw_values.get("overland_speed")
        state_DAL = DAL.Game_States_DAL(self.connection, self.cursor)

        carried = [0, 0, 0, 0, 0, 0]
        carried_condition1, carried_condition2 = None, None
        _, filtered_pks = state_DAL.get_filtered_state_list()
        prev = next((r for r in (filtered_pks or [])
                    if r[1] == cID and r[2] == turn_number - 1), None)
        if prev is not None:
            f_headers, f_records = state_DAL.get_next_filtered_game_state(prev[0], prev[1], prev[2])
            if f_records:
                row = dict(zip(f_headers, f_records[0]))
                fields = ["Secret Doors", "Secret Traps", "Secret Treasure", "Secret Cursed Treasure", "Secret Airborne Disease", "Secret Poison Gas"]
                carried = [row[f] for f in fields]
                carried_condition1 = row["Condition1"]
                carried_condition2 = row["Condition2"]

        state_DAL.create_filtered_state(systemDate, cID, turn_number, starvation, subsistence, speed, *carried, carried_condition1, carried_condition2)
    
    def update_filtered_game_state(self, raw_values, character_check, action_success, selected_fields):
        system_date = raw_values.get("system_date")
        character_ID = raw_values.get("character_ID")
        turn = raw_values.get("turn")
        starvation = raw_values.get("starvation_level")
        speed = raw_values.get("overland_speed")
        state_updates = Update_States_BLL(self.connection, self.cursor)
    
        action = action_success.lower() if action_success else ""

        if "secret_traps" in selected_fields:
            state_updates.filtered_secret_traps_updater(system_date, character_ID, turn)
            state_updates.condition_updater('Bleeding', system_date, character_ID, turn)
    
        if "secret_cursed_treasure" in selected_fields and character_check != "secret_cursed_treasure":
            state_updates.affliction_updater('Curse', system_date, character_ID, turn)
            state_updates.condition_updater('Vampirism', system_date, character_ID, turn)
    
        if "secret_airborne_disease" in selected_fields and character_check != 'secret_airborne_disease':
            state_updates.affliction_updater('Disease', system_date, character_ID, turn)
            state_updates.condition_updater('Exhausted', system_date, character_ID, turn)
    
        if "secret_poison_gas" in selected_fields and character_check != 'secret_poison_gas':
            state_updates.affliction_updater('Poison', system_date, character_ID, turn)
            state_updates.condition_updater('Sickened', system_date, character_ID, turn)
        
        match character_check:
            case "secret_doors":
                if action == 'succeeds':
                    state_updates.filtered_secret_doors_updater(system_date, character_ID, turn)
            case "secret_treasure":
                if action == 'succeeds':
                    state_updates.filtered_secret_treasure_updater(system_date, character_ID, turn)
                    state_updates.subsistence_updater(system_date, character_ID, turn)
                    speed = speed + Decimal('0.5')
                    state_updates.filtered_overland_speed_updater(system_date, character_ID, turn, speed)
            case "secret_cursed_treasure":
                if action == 'fails':
                    state_updates.affliction_updater('Curse', system_date, character_ID, turn)
                    state_updates.condition_updater('Vampirism', system_date, character_ID, turn)
                elif action == 'succeeds':
                    state_updates.filtered_secret_cursed_treasure_updater(system_date, character_ID, turn)
                
            case "secret_airborne_disease":
                if action == 'fails':
                    state_updates.affliction_updater('Disease', system_date, character_ID, turn)
                    state_updates.condition_updater('Exhausted', system_date, character_ID, turn)
                elif action == 'succeeds':
                    state_updates.filtered_secret_disease_updater(system_date, character_ID, turn)
                
            case "secret_poison_gas":
                if action == 'fails':
                    state_updates.affliction_updater('Poison', system_date, character_ID, turn)
                    state_updates.condition_updater('Sickened', system_date, character_ID, turn)
                elif action == 'succeeds':
                    state_updates.filtered_secret_poison_gas_updater(system_date, character_ID, turn)
                
    def update_game_state(self, selected_fields, raw_values):
        system_date = raw_values.get("system_date")
        character_ID = raw_values.get("character_ID")
        turn = raw_values.get("turn")
        starvation = raw_values.get("starvation_mode")
        speed = raw_values.get("overland_speed")
        state_updates = Update_States_BLL(self.connection, self.cursor)
        
        for secret in selected_fields:
            match secret:
                case "secret_doors":
                    state_updates.secret_doors_updater(system_date, character_ID, turn)
                case "secret_traps":
                    state_updates.secret_traps_updater(system_date, character_ID, turn)
                case "secret_treasure":
                    state_updates.secret_treasure_updater(system_date, character_ID, turn)
                case "secret_cursed_treasure":
                    state_updates.secret_cursed_treasure_updater(system_date, character_ID, turn)
                case "secret_airborne_disease":
                    state_updates.secret_disease_updater(system_date, character_ID, turn)
                case "secret_poison_gas":
                    state_updates.secret_poison_gas_updater(system_date, character_ID, turn)
                         
class Update_States_BLL:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.updater_DAL = DAL.States_Updater_DAL(connection, cursor)
    
    def turn_updater(self, new_turn, system_date, character_ID, turn_number):
        self.updater_DAL.turn(new_turn, system_date, character_ID, turn_number)
        
    def subsistence_updater(self, system_date, character_ID, turn):
        self.updater_DAL.subsistence(system_date, character_ID, turn)
    
    def condition_updater(self, new_condition, system_date, character_ID, turn):
         self.updater_DAL.condition(new_condition, system_date, character_ID, turn)
    
    def affliction_updater(self, new_affliction, system_date, character_ID, turn):
        self.updater_DAL.affliction(new_affliction, system_date, character_ID, turn)
    
    def secret_doors_updater(self, system_date, character_ID, turn):
        self.updater_DAL.secret_doors(system_date, character_ID, turn)
    
    def filtered_secret_doors_updater(self, system_date, character_ID, turn):
        self.updater_DAL.filtered_secret_doors(system_date, character_ID, turn)
    
    def secret_traps_updater(self, system_date, character_ID, turn):
        self.updater_DAL.secret_traps(system_date, character_ID, turn)
    
    def filtered_secret_traps_updater(self, system_date, character_ID, turn):
        self.updater_DAL.filtered_secret_traps(system_date, character_ID, turn)
    
    def secret_treasure_updater(self, system_date, character_ID, turn):
        self.updater_DAL.secret_treasure(system_date, character_ID, turn)
    
    def filtered_secret_treasure_updater(self, system_date, character_ID, turn):
        self.updater_DAL.filtered_secret_treasure(system_date, character_ID, turn)
    
    def secret_cursed_treasure_updater(self, system_date, character_ID, turn):
        self.updater_DAL.secret_cursed_treasure(system_date, character_ID, turn)
    
    def filtered_secret_cursed_treasure_updater(self, system_date, character_ID, turn):
        self.updater_DAL.filtered_secret_cursed_treasure(system_date, character_ID, turn)
    
    def secret_disease_updater(self, system_date, character_ID, turn):
        self.updater_DAL.secret_disease(system_date, character_ID, turn)
    
    def filtered_secret_disease_updater(self, system_date, character_ID, turn):
        self.updater_DAL.filtered_secret_disease(system_date, character_ID, turn)
    
    def secret_poison_gas_updater(self, system_date, character_ID, turn):
        self.updater_DAL.secret_poison_gas(system_date, character_ID, turn)
    
    def filtered_secret_poison_gas_updater(self, system_date, character_ID, turn):
        self.updater_DAL.filtered_secret_poison_gas(system_date, character_ID, turn)
    
    def overland_speed_updater(self, system_date, character_ID, turn, new_overland_speed):
        self.updater_DAL.overland_speed(system_date, character_ID, turn, new_overland_speed)
    
    def filtered_overland_speed_updater(self, system_date, character_ID, turn, new_overland_speed):
        self.updater_DAL.filtered_overland_speed(system_date, character_ID, turn, new_overland_speed)
        
    def carry_forward_secrets_updater(self, system_date, character_ID, turn, doors, traps, treasure, cursed, disease, poison, condition1, condition2, affliction1, affliction2):
        self.updater_DAL.carry_forward_secrets(system_date, character_ID, turn, doors, traps, treasure, cursed, disease, poison, condition1, condition2, affliction1, affliction2)

class Action_BLL:
    def __init__(self, selected_fields, raw_values, connection, cursor):
        self.selected_fields = selected_fields
        self.raw_values = raw_values
        self.connection = connection
        self.cursor = cursor
    
    def character_action(self):
        success_options = ["succeeds", "fails"]
        character_check = random.choice(self.selected_fields)
        action_success = random.choice(success_options)
        characterID = self.raw_values.get('character_ID')
        character_bll = Characters_BLL(self.connection, self.cursor)
        character = character_bll.get_character_name(characterID)
        
        match character_check:
            case "secret_doors":
                action = f"{character[1][0][0]} checks for secret doors and {action_success}."
            case "secret_traps":
                action = f"{character[1][0][0]} checks for secret traps and {action_success}."
            case "secret_treasure":
                action = f"{character[1][0][0]} searches for hidden treasure and {action_success}."
            case "secret_cursed_treasure":
                action = f"{character[1][0][0]} finds hidden treasure and casts a detect curse spell upon the treasure. The spell {action_success}."
            case "secret_airborne_disease":
                action = f"{character[1][0][0]} senses something heavy in the air and casts a detect disease spell. The spell {action_success}."
            case "secret_poison_gas":
                action = f"{character[1][0][0]} inhales air painfully and casts a detect poison spell. The spell {action_success}."
        
        return action, character_check, action_success

class Comparison_Engine_BLL:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        
    def classify_state(self, raw_values, selected_fields, character_check, action_success):
        """game_states is a table in the database.
           current game_state refers to a record from the game_states table. I examine each game state one at a time.
           raw_values is a dictionary. The keys are the column names from game_states. The values are fields from current game_state that
           correspond to each column name.
           
           This method stores the character_ID and turn number from the current game_state into variables. It stores action_success in action_clean
           after doing any needed cleanup to ensure the string is valid.
           
           _ captures the column names from the filtered_game_states Database table. This is not important, so it gets ignored.
           filtered_pks (filtered primary keys) captures the composite primary key from the filtered_game_states database table. The composite
           primary key consists of system_date, character_ID, and turn.
           
           The filtered_game_states database table is initially empty until filtered_game_states are created and stored there.
           
           row_exists is a boolean value. 
           If row_exists is true, then the current game_state already has an existing game state in the filtered_game_states table. Is all
           that is left to do is to update that filtered game state with the new selections the user made for this game state. This use case
           applies when a particular character_ID has already played one turn, and is now playing another turn.
           
           if row_exists is false, then this is the first turn for a particular character to be played, so I will create a new filtered
           game state for that character_ID. During subsequent turns this newly created filtered game state will get updated with additional
           information."""
        character_ID = str(raw_values.get("character_ID")).strip()
        turn = raw_values.get("turn")
        action_clean = action_success.lower().strip() if action_success else ""

        states_BLL = Game_States_BLL(self.connection, self.cursor)
        states_DAL = DAL.Game_States_DAL(self.connection, self.cursor)
        _, filtered_pks = states_DAL.get_filtered_state_list()

        row_exists = any(r[1] == character_ID and r[2] == turn for r in (filtered_pks or []))

        if not row_exists:
            states_BLL.create_filtered_game_state(raw_values)

        states_BLL.update_filtered_game_state(raw_values, character_check, action_clean, selected_fields)
            
           
        
        

            
        