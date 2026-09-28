"""This file is the Graphical User Interface for iSolo."""
import BLL
import tkinter as tk
import pydoc
from tkinter import messagebox
from tkinter import ttk

SECRET_FIELDS = [
    "secret_doors",
    "secret_traps",
    "secret_treasure",
    "secret_cursed_treasure",
    "secret_airborne_disease",
    "secret_poison_gas",
]

AFFLICTION_LABELS = {
    "secret_airborne_disease": "disease",
    "secret_poison_gas": "poison",
    "secret_cursed_treasure": "cursed",
}

CONDITION_LABELS = {
    "secret_traps": "bleeding",
    "disease": "exhausted",
    "poison": "sickened",
    "cursed": "vampirism",
}

AFFLICTION_FIELDS = set(AFFLICTION_LABELS.keys())

class AppState():
    def __init__(self):
        self.BLL_connection = None

class NextGameStateWindow(tk.Toplevel):
    """tk.Toplevel is the parent class, and NextGameStateWindow is the child class. I use super() as a necessary setup so that the 
    new game state window will work properly. 
    
    self.raw_values is a dictionary where the raw_headers are the keys and the raw values from the current game_state are the values for those
    keys.
    
    AFFLICTION_FIELDS is a set that lists the different types of afflictions that can affect characters. self.base_affliction_count sums up
    how many empty afflictions a character has in the current game_state. A character is allowed to have up to two afflictions.
    
    self.base_condition_count sums how many conditions a given character has in the current game_state. secret_traps causes the bleeding condition,
    and the different types of afflictions also cause various conditions. The total number of conditions that a character has cannot exceed 2.
    
    The methods in this class are called from the constructor. These are not to be called from outside this class."""
    def __init__(self, master, display_headers, display_record, raw_headers, raw_record, on_submit, player_name):
        super().__init__(master)
        self.title("NEXT GAME STATE")
        self.display_headers = display_headers
        self.display_record = display_record
        self.raw_values = dict(zip(raw_headers, raw_record))
        self.on_submit = on_submit
        self.check_vars = {}
        self.checkbuttons = {}
        self.player_name = player_name

        self.base_affliction_count = sum(int(self.raw_values.get(f, 0)) for f in AFFLICTION_FIELDS)
        self.base_condition_count = int(self.raw_values.get("secret_traps", 0)) + self.base_affliction_count

        self._build_display()
        self._build_selection()
        self._update_checkbox_states()

    def _build_display(self):
        """The player_name associated with a character_ID was carefully obtained in the open_next_game_state_window function below. It
        was obtained so that it could be displayed by this method with the player_label widget."""
        
        instructions_label = tk.Label(self, text = "Instructions: Below is a generic True game state for one of the available characters. Your job is to choose two secrets that the character does not know about. Those secrets will be applied to the true game state.", font=("Arial", 10, "bold"), wraplength=450, justify="left")

        instructions_label.pack(padx=10, pady=(10, 0), anchor="w")
        player_label = tk.Label(self, text = f"Player Name: {self.player_name[1][0][0]}", font=("Arial", 10, "bold"))
        player_label.pack(padx=10, pady=(10, 0), anchor="w")
        
        display_frame = tk.Frame(self)
        display_frame.pack(padx=10, pady=10, fill="x")

        for header, value in zip(self.display_headers, self.display_record):
            row = tk.Frame(display_frame)
            row.pack(fill="x")
            tk.Label(row, text=f"{header}:", width=20, anchor="w").pack(side="left")
            tk.Label(row, text=str(value), anchor="w").pack(side="left")
        
    def _build_selection(self):
        """This Game State Window asks the user to populate a game state with secrets. The character is not aware of these secrets yet.
           This creates a check box for each field in the SECRET_FIELDS list defined above the NextGameStateWindow class. Each check box
           starts out unchecked, so we define a special tkinter variable that the check boxes can read called called var. When a check
           box is clicked, I call _update_checkbox_states."""
        selection_frame = tk.LabelFrame(self, text="Choose 2 fields to increment")
        selection_frame.pack(padx=10, pady=10, fill="x")

        for field in SECRET_FIELDS:
            var = tk.BooleanVar(value=False)
            self.check_vars[field] = var
            cb = tk.Checkbutton(
                selection_frame, text=field, variable=var,
                command=self._update_checkbox_states
            )
            cb.pack(anchor="w")
            self.checkbuttons[field] = cb

        tk.Button(self, text="Submit", command=self._submit).pack(pady=10)
    
    def _selected_fields(self):
        """selected is the list of SECRET_FIELDS (defined at the top of this file) that the user has selected by clicking it's check box.
           This method builds and returns that list of selected SECRET_FIELDS."""
        selected = list()
        for secret_field, isSelected in self.check_vars.items():
            if isSelected.get():
                selected.append(secret_field)
        return selected
    
    def _update_checkbox_states(self):
        """This method wont let the user select more than two SECRET_FIELDS to add to the current game state. 
        
           It sums up the total of existing afflictions and
           conditions already in the current game state with the number of new afflictions and conditions that will be introduced
           based on the user selections. The total afflictions and the total conditions are two separate sums. These sums are the
           projected_affliction_count and the projected_condition_count. These sums become actual sums if the GUI allows the user to
           select and submit them.
           
           Next, would_exceed_affliction and would_exceed_condition are both boolean values that tells us whether the user selections
           will violate the two affliction limit or the two condition limit.
           
           Any possible violation of the affliction limit, condition limit, or pick limit will cause a given check box to be disabled.
           This leaves the user with only valid options to choose from. Not all of the choices are related to afflictions and conditions, so
           there will always be at least two choices that the user can pick from."""
        selected = self._selected_fields()

        if len(selected) > 2:
            
            extra = selected[-1]
            self.check_vars[extra].set(False)
            selected = self._selected_fields()

        projected_affliction_count = self.base_affliction_count + sum(
            1 for secret_field in selected if secret_field in AFFLICTION_FIELDS
        )
        projected_condition_count = self.base_condition_count + sum(
            1 for secret_field in selected if secret_field == "secret_traps" or secret_field in AFFLICTION_FIELDS
        )

        two_selected = len(selected) >= 2

        for field, cb in self.checkbuttons.items():
            is_selected = field in selected

            would_exceed_affliction = (
                field in AFFLICTION_FIELDS
                and not is_selected
                and projected_affliction_count >= 2
            )
            would_exceed_condition = (
                (field == "secret_traps" or field in AFFLICTION_FIELDS)
                and not is_selected
                and projected_condition_count >= 2
            )
            would_exceed_pick_limit = two_selected and not is_selected

            if would_exceed_affliction or would_exceed_condition or would_exceed_pick_limit:
                cb.config(state="disabled")
            else:
                cb.config(state="normal")
    
    def _submit(self):
        """Once the user chooses what secrets they will add to the current game state, they have to click submit. That submit button will
           call this method. This method passes control to the on_submit function which is detailed below."""
        selected = self._selected_fields()
        if len(selected) != 2:
            messagebox.showwarning("Selection required", "You must choose exactly 2 fields.")
            return
        self.on_submit(selected, self.raw_values)
        self.destroy()

def on_closing(root_window, app_state):
    if app_state.BLL_connection is not None:
        app_state.BLL_connection.close()
    root_window.destroy()

def open_character_action_window(selected_fields, raw_values, parent_window, connection, cursor, app_state):
    """action is a python f-string that describes what action a character takes and whether they were successful or not. These actions
       are a response to one of the secrets in the current game_state. Which secret and success/failure are randomized.
       
       character_check is a variable that holds which secret the character is checking for, and action_success is a string that holds
       either 'success' or 'failure' to indicate the result of the character's action.
       
       The character_action_window displays the f-string stored in the action variable. The user reads it and clicks next. Control is 
       passed to open_comparison_window"""
    action_bll = BLL.Action_BLL(selected_fields, raw_values, connection, cursor)
    action, character_check, action_success = action_bll.character_action()
    action_window = tk.Toplevel(parent_window)
    action_window.title("CHARACTER ACTIONS")
    action_window.geometry("300x300")
    action_label = tk.Label(action_window, text = action, wraplength=250, justify="left")
    action_label.pack(padx=10, pady=(10, 0), anchor="w")
    next_button = ttk.Button(action_window, text="Next", command=lambda: open_comparison_window(selected_fields, raw_values, character_check, action_success, parent_window, action_window, connection, cursor, app_state))
    next_button.pack(padx=10, pady=(10, 0), anchor="w")

def open_comparison_window(selected_fields, raw_values, character_check, action_success, parent_window, action_window, connection, cursor, app_state):
    """The BLL sends the request to the DAL to update the current game state with the user selections from the object of the NextGameStateWindow class.
       classify_state will either update an existing filtered_game_state or it will create a filtered_game_state depending on whether the
       current game state references a character that has already had a turn or not.
       
       Now that the filtered game state has been updated or created, it is now time to create the comparison_window. The actual game state
       and the filtered game state (What the player knows) are displayed so the user can compare the truth to what the player knows.
       
       display_current_game_state gets both the game_state and the filtered_game_state from the DAL and uses treevies to display them.
       
       After the user compares the two, they are free to click next. This will start the event loop again. The next game state is pulled from
       the game_states database table, the user will select secrets for it, and then the filtered_game_state will be updated or created.
       The user then gets a new comparison for that game state. When we run out of game states, the application terminates."""
    action_window.destroy()
    states_BLL = BLL.Game_States_BLL(connection, cursor)
    states_BLL.update_game_state(selected_fields, raw_values)
    comparison_BLL = BLL.Comparison_Engine_BLL(connection, cursor)
    comparison_BLL.classify_state(raw_values, selected_fields, character_check, action_success)
    
    comparison_window = tk.Toplevel(parent_window)
    comparison_window.title("GAME STATE COMPARISON")
    comparison_window.geometry("900x350")
    
    instructions_label = tk.Label(comparison_window, text = "The top row is the true game state, and the bottom row is the filtered game state that would be revealed to the player.",
                                  font = ("verdana", 12, "bold"), wraplength = 800, justify = "left")
    instructions_label.grid(row = 0, column = 0, columnspan = 3, padx = 5, pady = 5)
    
    tree = ttk.Treeview(comparison_window)
    tree.grid(row = 1, column = 0, columnspan = 3, sticky = "nsew", padx = 10, pady = 10)
    comparison_window.grid_columnconfigure(0, weight = 1)
    comparison_window.grid_columnconfigure(1, weight = 1)
    scrollbar = ttk.Scrollbar(comparison_window, orient = "horizontal", command = tree.xview)
    scrollbar.grid(row = 3, column = 0, sticky = "ew", pady = 10)
    tree.configure(xscrollcommand = scrollbar.set)
    comparison_headers, comparison_records = states_BLL.display_current_game_state(raw_values)
    populate_tree(tree, comparison_headers, comparison_records)
    
    quit_button = ttk.Button(comparison_window, text = "Quit", command = lambda: on_closing(comparison_window, app_state))
    quit_button.grid(row = 4, column = 0, padx = 10, pady = 10)
    comparison_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(comparison_window, app_state))
    
    next_button = ttk.Button(comparison_window, text = "Next", command = lambda: update_game_state(comparison_window, connection, cursor, app_state))
    next_button.grid(row = 4, column = 1, padx = 10, pady = 10)

def update_game_state(comparison_window, connection, cursor, app_state):
    open_next_game_state_window(comparison_window, connection, cursor, app_state)

def open_next_game_state_window(parent_window, connection, cursor, app_state):
    """Some users will create a new player and character, and some users won't. Either way, control will everntually wind up here.
    
    If the user did not create a new player and character, then the parent_window parameter will hold the players_window object created in the
    open_player_window function below.
    
    If the user did create a new player and character, then the parent_window parameter will hold the root_window. The root_window is
    the opening window where the user logs into the database. That window was hidden in the get_credentials function.
    
    Either way parent_window gets hidden here. We cannot destroy it because that may end the entire application, so it gets hidden.
    raw_headers and raw_record holds the information in the game_states table on the database. The display_headers and display_record
    holds the output from a view of the game_states table. The view just formats the information in a user friendly way.
    
    The BLL gets raw and display data from the DAL, and returns it here. Note that only the data for one game state is being returned, not
    all of them. The whole cycling through the different game states for all of the characters in the database is handled one at a time 
    in the BLL.
    
    The BLL passes a request to call a stored procedure from the DAL that returns the player name associated with a given character ID.
    The stored procedure is located in states_of_games_DB.sql
    
    NextGameStateWindow() is a class instantiation. A new object of this class gets created every time the BLL moves to the next
    game state in the database. Once the BLL resolves all of the game states in the database, the application terminates. That concludes
    the demostration. For each game state, NextGameStateWindow will render a window that shows all of the fields of that game state. If 
    this is the first time the user has seen that player, then the game state will be pretty generic. As time goes on, that player's
    game state will evolve in complexity from previous turns.
    
    on_submit is an inner function. Its local scope gives it access to parent_window, connection, cursor, and app_state. NextGameStateWindow
    does not need to know about those local parameters to do its job. on_submit will be called by a method within a NextGameStateWindow object. 
    That object stays decoupled from the BLL and its inner workings. The purpose of that object is to render a window and pass on user input. 
    The data obtained from that window will be processed by the BLL. on_submit is called by a submit button that keeps the GUI and BLL decoupled.
    This is an example of abstraction, an important OOP property."""
    parent_window.withdraw()
    game_state_bll = BLL.Game_States_BLL(connection, cursor)
    display_headers, display_record, raw_headers, raw_record = game_state_bll.display_next_game_state()
    players_bll = BLL.Players_BLL(connection, cursor)
    character_ID = int(raw_record[1])
    play_name = players_bll.get_player_name_from_character(character_ID)
    
    if display_headers is None:
        messagebox.showinfo("Filtering Complete", "All game states have been filtered.")
        return
    
    def on_submit(selected_fields, raw_values):
        open_character_action_window(selected_fields, raw_values, parent_window, connection, cursor, app_state)
    
    NextGameStateWindow(parent_window, display_headers, display_record, raw_headers, raw_record, on_submit, play_name)

def open_new_character_form(character_window, connection, cursor, root_window, app_state, player_name):
    """Here we have the same architecture as the open_new_player_form function with the inner function utilizing the parameters passed
    into this function. The BLL passes the new character name to the DAL to store in the database. The BLL returns a boolean to 
    indicate that the name was added successfully. That boolean is stored in the variable called 'success'. Control is passed to 
    the open_next_game_state_window function."""
    form_window = tk.Toplevel(character_window)
    form_window.title("CREATE NEW CHARACTER")
    form_window.geometry("450x120")
    
    player_name_Label = tk.Label(form_window, text = f"Player Name: {player_name}")
    player_name_Label.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "w")
    character_name_label = tk.Label(form_window, text = "New Character Name:")
    character_name_label.grid(row = 1, column = 0, padx = 10, pady = 10,sticky = "w")
    character_name_entry = tk.Entry(form_window, width = 35)
    character_name_entry.grid(row = 1, column = 1, padx = 10, pady = 10)
    
    def submit_new_character():
        character_name = character_name_entry.get().strip()
        if not character_name:
            messagebox.showerror("Input Error", "Character Name Cannot Be Empty.")
            return
        
        characters_bll = BLL.Characters_BLL(connection, cursor)
        success = characters_bll.create_character(character_name, player_name)
        if not success:
            messagebox.showerror("Data Error", "Failed to create character.")
            return
        
        game_state_bll = BLL.Game_States_BLL(connection, cursor)
        success = game_state_bll.create_states(character_name)
        if not success:
            messagebox.showerror("Data Error", "Character created, but failed to create initial game state.")
            return
        
        form_window.destroy()
        character_window.destroy()
    
        open_next_game_state_window(root_window, connection, cursor, app_state)

    submit_button = tk.Button(form_window, text="Submit", command=submit_new_character)
    submit_button.grid(row=2, column=0, columnspan=2, pady=10)
    
def open_character_window(root_window, app_state, connection, cursor, name):
    """This function works a lot like the open_player_window. It uses the populate_tree helper function to list all of the existing 
    characters in the database in treeview. That way the user can see which characters already exist before creating a new character for the 
    player already created. 
    
    The user clicks the 'New Character' button to call the open_new_character_form function. A window opens that is similar to the one
    used to create a new player. This window stays open so the user can reference all the current character names before selecting a
    new one."""
    character_window = tk.Toplevel(root_window)
    character_window.title("LIST OF CHARACTERS")
    character_window.geometry("900x350")
    
    instructions_label = tk.Label(character_window, text = "Here, you can see all of the current characters and which player plays each character. Now you can create a character for your player below.",
                                  font = ("verdana", 12, "bold"), wraplength = 800, justify = "left")
    instructions_label.grid(row = 0, column = 0, columnspan = 3, padx = 5, pady = 5)
    
    tree = ttk.Treeview(character_window)
    tree.grid(row = 1, column = 0, columnspan = 2, sticky = "nsew", padx = 10, pady = 10)
    character_window.grid_columnconfigure(0, weight = 1)
    character_window.grid_columnconfigure(1, weight = 1)
    scrollbar = ttk.Scrollbar(character_window, orient = "vertical", command = tree.yview)
    scrollbar.grid(row = 1, column = 2, sticky = "ns", pady = 10)
    tree.configure(yscrollcommand = scrollbar.set)
    
    characters_bll = BLL.Characters_BLL(connection, cursor)
    headers, records  = characters_bll.display_characters()
    if headers is not None:
        populate_tree(tree, headers, records)
    else:
        messagebox.showerror("Data Error", "Failed to load character data.")
    
    new_character_button = ttk.Button(character_window, text = "New Character", command = lambda: open_new_character_form(character_window, connection, cursor, root_window, app_state, name))
    new_character_button.grid(row = 3, column = 0, sticky = "w", padx = 10, pady = 10)
    quit_button = ttk.Button(character_window, text = "Quit", command = lambda: on_closing(root_window, app_state))
    quit_button.grid(row = 3, column = 1, padx = 10, pady = 10)
    character_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(root_window, app_state))

def open_new_player_form(players_window, connection, cursor, root_window, app_state):
    """This function opens a small window that allows you to enter a name for a new player. The player window stays open so the user
    can see the names of all the players currently in the database.
    
    The submit button leads to the inner function submit_new_player(). This inner function simplifies software organization because
    name_entry and all of the parameters passed into open_new_player_form are in scope. there is no need to pass these to a new function."""    
    form_window = tk.Toplevel(players_window)
    form_window.title("CREATE NEW PLAYER")
    form_window.geometry("475x120")
    
    name_Label = tk.Label(form_window, text = "New Player Name:")
    name_Label.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "w")
    
    name_entry = tk.Entry(form_window, width = 50)
    name_entry.grid(row = 0, column = 1, padx = 10, pady = 10)

    def submit_new_player():
        """"This inner function passes the new player name through the BLL and to the DAL, so it can be added to the database.
        The DAL returns a boolean to indicate success with adding the new player to the database. Once a new player is successfully
        created, control is passed to the open_character_window, so a new character can be created and associated with the new player."""
        name = name_entry.get().strip()
        if not name:
            messagebox.showerror("Input Error", "Player Name Cannot Be Empty.")
            return
        players_bll = BLL.Players_BLL(connection, cursor)
        success = players_bll.create_player(name)
    
        if not success:
            messagebox.showerror("Data Error", "Failed to create player.")
            return
            
        form_window.destroy()
        players_window.destroy()
        open_character_window(root_window, app_state, connection, cursor, name)
            
    submit_button = ttk.Button(form_window, text = "Submit", command = submit_new_player)
    submit_button.grid(row = 1, column = 0, columnspan = 2, pady = 10)

def populate_tree(tree, headers, records):
    """This function is a reusable helper that takes a treeview widget object, a list of headers, and a list of rows, and clears out whatever
        is already in the widget object. Then it refreshes the widget object with the headers and rows from the database.
    
    First I delete existing rows to prevent repeated entries. delete() expects multiple arguments where each argument is a row ID.
    get_children returns a tuple of row IDs, so we use * to upack the tuple into comma separated row IDs."""
    tree.delete(*tree.get_children())
    
    tree["columns"] = headers
    tree["show"] = "headings"
    for header in headers:
        tree.heading(header, text = header, anchor = "center")
        tree.column(header, width = 120, anchor = "center")
    
    for row in records:
        tree.insert("", "end", values = row)

def open_player_window(root_window, app_state, connection, cursor):
    """This function displays the player window. It shows all of the players that are in the pre-populated database. If the user wishes
    to create a new player and add it to the list of players, that can be done here. The connection and cursor objects are passed through
    the BLL layer to the DAL. There the player data is read from the database and returned into the headers and records variables.
    Treeview() is used to display the information in the player_window. populate_tree is a helper function that renders the database
    information using commond methods of Treeview().
    
    There are two pathways to the game state window. The user can choose to create a new player and a new character for that player by
    clicking the 'New' button. This pathway will add a new player and character to the database for later use. The more direct route is
    to skip player/character creation and click 'Next'. Player/Character creation is a minor feature of this demo. The demonstration runs
    perfectly fine with the players and characters that are prepopulated in the database."""
    players_window = tk.Toplevel(root_window)
    players_window.title("LIST OF PLAYERS")
    players_window.geometry("975x325")
    
    instructions_label = tk.Label(players_window, text = "Instructions: To use existing players, click 'Next' OR To Create a new player, click 'New'",
                                  font = ("verdana", 12, "bold"))
    instructions_label.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = (10, 0), sticky = "w")
    
    tree = ttk.Treeview(players_window, height = 8)
    tree.grid(row = 1, column = 0, columnspan = 2, sticky = "nsew", padx = 10, pady = 10)
    scrollbar = ttk.Scrollbar(players_window, orient = "vertical", command = tree.yview)
    scrollbar.grid(row = 1, column = 2, sticky = "ns", pady = 10)
    tree.configure(yscrollcommand = scrollbar.set)
    
    players_window.grid_columnconfigure(0, weight = 1)
    players_window.grid_columnconfigure(1, weight = 1)
    
    players_bll = BLL.Players_BLL(connection, cursor)
    headers, records = players_bll.display_players()
    
    if headers is not None:
        populate_tree(tree, headers, records)
    else:
        messagebox.showerror("Data Error", "Failed to load player data.")
    
    new_button = ttk.Button(players_window, text = "New", command = lambda: open_new_player_form(players_window, connection, cursor,
                            root_window, app_state))
    new_button.grid(row = 3, column = 1, padx = 10, pady = 10)
    next_button = ttk.Button(players_window, text="Next", command=lambda: open_next_game_state_window(players_window, connection, cursor, app_state))
    next_button.grid(row = 3, column = 2, sticky = "e", padx = 10, pady = 10)
    quit_button = ttk.Button(players_window, text = "Quit", command = lambda: on_closing(root_window, app_state))
    quit_button.grid(row = 3, column = 0, padx = 10, pady = 10)
    players_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(root_window, app_state))

def get_credentials(un, pw, host, port, root_window, app_state):
    """Args:
        un: User name, your user name when logging into workbench.
        pw: Password, your password when logging into workbench.
        host: Your host name or host ip address when logging into workbench.
        port: The port number you use to log into workbench.
        root_window: The root window for the application. The root window is the screen where you enter your workbench credentials.
        app_state: The object of the class AppState(). 
        
    This function gets the database credentials from the Entry widgets, stores them in variables, and passes them to the Business Logic Layer (BLL).
    The BLL will pass those credentials to the Data Access Layer (DAL) where they will be stored as instance variables in a class that will
    use them to connect to the database. All database interacteractions are handled in the Data Access Layer. That allows a separaction of
    concerns which contributes to overall organization and makes the application easily scalable.
     
    The get() method reads everything in as a string. However workbench requires the port number to be a whole number, so it is
    immediately converted to an int.
    
    DB_BLL_Connection is instantiated, and that object is stored in BLL_connection.
    BLL_connection is an instance variable of the AppState class defined towards the top of this file.
    
    app_state (alias for AppState).BLL_connection will ultimately return the connection object and cursor object which can be passed
    around and used as needed to query the database. Once these objects are obtained, control is passed to the open_player_window
    function above."""
    user = un.get()
    password = pw.get()
    login_host = host.get()
    try:
        login_port = int(port.get())
    except ValueError:
        messagebox.showerror("Input Error", "Port must be a number.")
        return
        
    app_state.BLL_connection = BLL.DB_BLL_Connection(user, password, login_host, login_port)
    connection, cursor = app_state.BLL_connection.connect()
    if connection is not None:
        root_window.withdraw()
        open_player_window(root_window, app_state, connection, cursor)
    else:
        messagebox.showerror("Login Error", "Invalid credentials. \nPlease try again.")
    
def main():
    """The GUI is implemented with the Tkinter python library. The root window for this application is a login screen. That login screen
    allows you to log into workbench using your own credentials provided you have workbench installed and set up on your local computer.
    A potential user needs to open the file: states_of_games_DB.sql in their workbench installation and execute it before running GUI.py. The
    SQL file will delete and create the database and associated views, functions, and stored procedures each time it is executed. This main
    method is just a login window and a series of widgets that facilitate your workbench login. When the user clicks the submit button,
    control is passed to the get_credentials function above."""
    app_state = AppState()
    root = tk.Tk()
    root.title('DATABASE LOGIN')
    root.geometry('500x275')
    
    user_label = tk.Label(root, text = "User Name:")
    user_label.grid(row = 0, column = 0, padx = 5, pady = 10, sticky = "w")
    
    user_entry = tk.Entry(root, width = 50)
    user_entry.grid(row = 0, column = 10, pady = 10, sticky = "w")
    
    pw_label = tk.Label(root, text = "Password:")
    pw_label.grid(row = 2, column = 0, padx = 5, pady = 10, sticky = "w")
    
    pw_entry = tk.Entry(root, width = 50, show = "*")
    pw_entry.grid(row = 2, column = 10, pady = 10, sticky = "w")
    
    host_label = tk.Label(root, text = "Host:")
    host_label.grid(row = 4, column = 0, padx = 5, pady = 10, sticky = "w")
    
    host_entry = tk.Entry(root, width = 30)
    host_entry.insert(0, "127.0.0.1")
    host_entry.grid(row = 4, column = 10, pady = 10, sticky = "w")
    
    port_label = tk.Label(root, text = "Port:")
    port_label.grid(row = 6, column = 0, padx = 5, pady = 10, sticky = "w")
    
    port_entry = tk.Entry(root, width = 20)
    port_entry.insert(0, "3306")
    port_entry.grid(row = 6, column = 10, pady = 10, sticky = "w")
    
    login_button = ttk.Button(root, text = "SUBMIT", command = lambda:get_credentials(user_entry, pw_entry, host_entry, port_entry, root, app_state))
    login_button.grid(row = 8, column = 10, pady = 10)
    
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, app_state))
    root.mainloop()
    
if __name__ == "__main__": main()