DROP DATABASE IF EXISTS `generic_game_states`;
CREATE DATABASE IF NOT EXISTS `generic_game_states`;
USE `generic_game_states`;

DROP TABLE IF EXISTS `players`;

CREATE TABLE `players` (
`player_ID` char(2) NOT NULL,
`player_name` varchar(50) NOT NULL,
PRIMARY KEY (`player_ID`)
);

INSERT INTO `players` VALUES
(2, 'Michael Scott'),
(3, 'Barney Stinson'),
(4, 'Al Bundy'),
(5, 'Mr. Bean'),
(6, 'Cosmo Kramer'),
(7, 'Dwight Schrute'),
(8, 'George Costanza'),
(13, 'Sheldon Cooper'),
(15, 'Sophia Petrillo'),
(16, 'Chandler Bing');

DROP TABLE IF EXISTS `characters`;

CREATE TABLE `characters` (
`character_ID` char(3) NOT NULL,
`character_name` varchar(50) NOT NULL,
`player_ID` char(2) NOT NULL,
PRIMARY KEY (`character_ID`),
FOREIGN KEY (`player_ID`) REFERENCES `players` (`player_ID`)
);

INSERT INTO `characters` VALUES
('101', 'Tom', '2'),
('102', 'Jerry', '3'),
('103', 'Buggs Bunny', '4'),
('104', 'Sponge Bob', '5'),
('105', 'Homer Simpson', '6'),
('106', 'Donald Duck', '7'),
('107', 'Scooby Doo', '8'),
('108', 'Daffy Duck', '4'),
('109', 'Pikachu', '8'),
('110', 'Road Runner', '2'),
('111', 'Fred Flintstone', '5'),
('112', 'Betty Boop', '13'),
('113', 'Goofy', '13'),
('114', 'Popeye', '15'),
('115', 'Woody Woodpecker', '16');

DROP TABLE IF EXISTS `game_states`;

CREATE TABLE `game_states` (
`system_date` DATE NOT NULL,
`character_ID` char(3) NOT NULL,
`turn` int NOT NULL,
`starvation_mode` boolean NOT NULL,
`subsistence_level` enum ('Poor', 'Fair', 'Good') NOT NULL,
`condition1` varchar(50),
`condition2` varchar(50),
`affliction1` varchar(25),
`affliction2` varchar(25),
`secret_doors` int NOT NULL,
`secret_traps` int NOT NULL,
`secret_treasure` int NOT NULL,
`secret_cursed_treasure` int NOT NULL,
`secret_airborne_disease` int NOT NULL,
`secret_poison_gas` int NOT NULL,
`overland_speed` decimal(3,1) NOT NULL,
PRIMARY KEY (`system_date`, `character_ID`, `turn`),
FOREIGN KEY (`character_ID`) REFERENCES `characters` (`character_ID`)
);

INSERT INTO `game_states` VALUES
('2026-08-10', '111',   3, 0, 'Fair', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5),
('2026-08-11', '111',   4, 0, 'Fair', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5),
('2026-08-10', '101',   5, 1, 'Poor', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 13.25), 
('2026-08-10', '101',   6, 1, 'Poor', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 13.25),
('2026-08-10', '114',  10, 0, 'Fair', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5),
('2026-08-11', '114',  11, 0, 'Fair', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5),
('2026-08-14', '114',  12, 0, 'Fair', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5),
('2026-08-13', '104',  15, 0, 'Good', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5),
('2026-08-13', '104',  16, 0, 'Good', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5),
('2026-08-11', '108',  25, 1, 'Poor', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 13.25),
('2026-08-13', '108',  26, 1, 'Poor', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 13.25),
('2026-08-16', '108',  27, 1, 'Poor', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 13.25),
('2026-08-10', '110',  40, 1, 'Poor', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 13.25),
('2026-08-10', '110',  41, 1, 'Poor', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 13.25),
('2026-08-18', '110',  42, 1, 'Poor', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 13.25),
('2026-08-11', '103',  52, 0, 'Good', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5),
('2026-08-13', '103',  53, 0, 'Good', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5),
('2026-08-17', '103',  54, 0, 'Good', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5),
('2026-08-11', '112',  59, 0, 'Good', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5),
('2026-08-11', '107',  60, 0, 'Fair', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5),
('2026-08-13', '112',  60, 0, 'Good', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5),
('2026-08-11', '107',  61, 0, 'Fair', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5),
('2026-08-11', '115',  86, 0, 'Good', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5),
('2026-08-12', '115',  87, 0, 'Good', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5),
('2026-08-13', '109',  98, 0, 'Good', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5),
('2026-08-13', '109',  99, 0, 'Good', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5),
('2026-08-10', '105', 100, 1, 'Poor', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 13.25),
('2026-08-10', '105', 101, 1, 'Poor', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 13.25),
('2026-08-10', '106', 111, 0, 'Fair', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5),
('2026-08-10', '106', 112, 0, 'Fair', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5);

DROP TABLE IF EXISTS `filtered_game_states`;

/*This table gets populated by the application. The filter produces the filtered game state.*/
CREATE TABLE `filtered_game_states` (
`system_date` DATE NOT NULL,
`character_ID` char(3) NOT NULL,
`turn` int NOT NULL,
`starvation_mode` boolean NOT NULL,
`subsistence_level` enum ('Poor', 'Fair', 'Good') NOT NULL,
`condition1` varchar(50),
`condition2` varchar(50),
`affliction1` varchar(25),
`affliction2` varchar(25),
`secret_doors` int NOT NULL,
`secret_traps` int NOT NULL,
`secret_treasure` int NOT NULL,
`secret_cursed_treasure` int NOT NULL,
`secret_airborne_disease` int NOT NULL,
`secret_poison_gas` int NOT NULL,
`overland_speed` decimal(3,1) NOT NULL,
PRIMARY KEY (`system_date`, `character_ID`, `turn`),
FOREIGN KEY (`character_ID`) REFERENCES `characters` (`character_ID`)
);

DROP VIEW IF EXISTS `game_state_view`;
/*VIEWS*/
CREATE VIEW `game_state_view` AS
	SELECT 
    DATE_FORMAT(g.system_date, '%m/%d/%Y') AS `System Date`,
    c.character_name AS `Character Name`,
    g.turn AS `Turn Number`,
    g.starvation_mode AS `Starvation Mode`,
    g.subsistence_level AS `Subsistence Level`,
    g.condition1 AS `Condition1`,
    g.condition2 AS `Condition2`,
    g.affliction1 AS `Affliction1`,
    g.affliction2 AS `Affliction2`,
    g.secret_doors AS `Secret Doors`,
    g.secret_traps AS `Secret Traps`,
    g.secret_treasure AS `Secret Treasure`,
    g.secret_cursed_treasure AS `Secret Cursed Treasure`,
    g.secret_airborne_disease AS `Secret Airborne Disease`,
    g.secret_poison_gas AS `Secret Poison Gas`,
    CONCAT(g.overland_speed, ' miles/day') AS `Overland Speed`
    FROM game_states g
    INNER JOIN characters c ON g.character_ID = c.character_ID;
    
    DROP VIEW IF EXISTS `filtered_game_state_view`;
    CREATE VIEW `filtered_game_state_view` AS
		SELECT
		DATE_FORMAT(f.system_date, '%m/%d/%Y') AS `System Date`,
		c.character_name AS `Character Name`,
		f.turn AS `Turn Number`,
		f.starvation_mode AS `Starvation Mode`,
		f.subsistence_level AS `Subsistence Level`,
		f.condition1 AS `Condition1`,
		f.condition2 AS `Condition2`,
		f.affliction1 AS `Affliction1`,
		f.affliction2 AS `Affliction2`,
		f.secret_doors AS `Secret Doors`,
		f.secret_traps AS `Secret Traps`,
		f.secret_treasure AS `Secret Treasure`,
		f.secret_cursed_treasure AS `Secret Cursed Treasure`,
		f.secret_airborne_disease AS `Secret Airborne Disease`,
		f.secret_poison_gas AS `Secret Poison Gas`,
        CONCAT(f.overland_speed, ' miles/day') AS `Overland Speed`
		FROM filtered_game_states f
		INNER JOIN characters c ON f.character_ID = c.character_ID;
	
    DROP VIEW IF EXISTS `player_view`;
    CREATE VIEW `player_view` AS
		SELECT
        player_ID AS `Player ID`,
        player_name AS `Player Name`
        FROM players;
    
    DROP VIEW IF EXISTS `character_view`;
    CREATE VIEW `character_view` AS
		SELECT
        c.character_ID AS `Character ID`,
        c.character_Name AS `Character Name`,
        c.player_ID AS `Player ID`,
        p.player_name AS `Player Name`
        FROM characters c
        INNER JOIN players p ON c.player_ID = p.player_ID;
	
    /*FUNCTIONS*/
    DROP FUNCTION IF EXISTS `get_player_ID`;
    DELIMITER $$
    
    CREATE FUNCTION get_player_ID (p_player_name varchar(50))
    RETURNS varchar(2)
    DETERMINISTIC
    READS SQL DATA
    BEGIN
		DECLARE ID varchar(2);
		SELECT TRIM(player_ID) INTO ID FROM players
        WHERE player_name = p_player_name;
        RETURN ID;
	END$$
    DELIMITER ;
    
     DROP FUNCTION IF EXISTS `get_character_ID`;
    DELIMITER $$
    
    CREATE FUNCTION get_character_ID (c_character_name varchar(50))
    RETURNS varchar(3)
    DETERMINISTIC
    READS SQL DATA
    BEGIN
		DECLARE ID varchar(3);
        SELECT TRIM(character_ID) INTO ID FROM characters
        WHERE character_name = c_character_name;
        return ID;
    END$$
    DELIMITER ;
    
     DROP FUNCTION IF EXISTS `get_player_name`;
    DELIMITER $$
    
    CREATE FUNCTION get_player_name(ID char(2))
    RETURNS varchar(50)
    DETERMINISTIC
    BEGIN
		DECLARE player varchar(50);
        SELECT player_name INTO player FROM players
        WHERE ID = players.player_ID;
        RETURN player;
    END$$
    DELIMITER ;
    
	DROP FUNCTION IF EXISTS `get_character_name`;
    DELIMITER $$
    CREATE FUNCTION get_character_name(ID char(3))
    RETURNS varchar(50)
    DETERMINISTIC
    BEGIN
		DECLARE char_name varchar(50);
        SELECT character_name INTO char_name FROM characters
        WHERE ID = characters.character_ID;
        RETURN char_name;
    END$$
    DELIMITER ;
    
    /*STORED PROCEDURES*/
    /*READ OPERATIONS*/
    DROP PROCEDURE IF EXISTS `call_get_player_ID`;
    DELIMITER $$
    CREATE PROCEDURE call_get_player_ID(IN p_player_name varchar(35))
    BEGIN
		SELECT get_player_ID(p_player_name) AS player_ID;
	END$$
    DELIMITER ;
    
  DROP PROCEDURE IF EXISTS `call_get_character_ID`;
    DELIMITER $$
    CREATE PROCEDURE call_get_character_ID(IN c_character_name varchar(35))
    BEGIN
		SELECT get_character_ID(c_character_name) AS character_ID;
	END$$
    DELIMITER ;  
    
    DROP PROCEDURE IF EXISTS `call_get_character_name`;
    DELIMITER $$
    CREATE PROCEDURE call_get_character_name(IN id char(3))
    BEGIN
		SELECT get_character_name(id) AS character_name;
	END$$
    DELIMITER ;
    
    DROP PROCEDURE IF EXISTS `get_player_name_from_characterID`;
    DELIMITER $$
    CREATE PROCEDURE get_player_name_from_characterID(IN c_characterID varchar(35))
    BEGIN
		SELECT get_player_name((SELECT player_ID FROM characters WHERE character_ID = c_characterID)) AS player_name;
	END$$
    DELIMITER ;
    
	DROP PROCEDURE IF EXISTS `get_game_state_list`;
    DELIMITER $$
    /*The Primary Keys for both game state tables are needed to identify each individual game state. This procedure returns all of the primary keys in the game_states table. That serves
    as the list of all game states. My application will cycle through all of these true game states from this list of primary keys. This ensures that it examines each one. One at a time.*/
    CREATE PROCEDURE get_game_state_list()
    BEGIN
		SELECT system_date, character_ID, turn FROM game_states;
    END$$
    DELIMITER ;
    
    /*Similarly, this gets all of the primary keys currently in the filtered_game_states table. The contents of this table will change over time. Many of the games states in the game states table 
    shows up more than once because each game state entry represents a different turn. When the filtered_game_states table has more than one turn for the same player, the oldest turn gets deleted. It no longer
    serves a purpose. This procedure gets the list of all primary keys currently in the game_states table. The BLL can then determine whether anything needs to be deleted.*/
   DROP PROCEDURE IF EXISTS `get_filtered_game_state_list`;
   DELIMITER $$
    
    CREATE PROCEDURE get_filtered_game_state_list()
	BEGIN
		SELECT system_date, character_ID, turn FROM filtered_game_states;
    END$$
	DELIMITER ;
    
    DROP PROCEDURE IF EXISTS `get_players`;
    DELIMITER $$
    
    CREATE PROCEDURE get_players()
    BEGIN
		SELECT * FROM players;
	END$$
    DELIMITER ;
    
 DROP PROCEDURE IF EXISTS `get_characters`;
    DELIMITER $$
    
    CREATE PROCEDURE get_characters()
    BEGIN
		SELECT * FROM characters;
	END$$
    DELIMITER ;
    
DROP PROCEDURE IF EXISTS `get_raw_game_state`;
DELIMITER $$
CREATE PROCEDURE get_raw_game_state (IN sys_date DATE,
                                      IN ID CHAR(3),
                                      IN turn_number INT)
BEGIN
	SELECT * FROM game_states
    WHERE system_date = sys_date
      AND character_ID = ID
      AND turn = turn_number;
END$$
DELIMITER ;
    
     DROP PROCEDURE IF EXISTS `get_game_state`;
    DELIMITER $$
    
    CREATE PROCEDURE get_game_state (IN sys_date date,
									    ID char(3),
                                        turn_number int)
    BEGIN
		DECLARE v_char_name VARCHAR(50);
		SET v_char_name = get_character_name(ID);
		SELECT * FROM game_state_view
        WHERE `System Date` = DATE_FORMAT(sys_date, '%m/%d/%Y')
          AND `Character Name` = v_char_name
          AND `Turn Number` = turn_number;
	END$$
    DELIMITER ;
    
DROP PROCEDURE IF EXISTS `get_filtered_game_state`;
DELIMITER $$
CREATE PROCEDURE get_filtered_game_state (IN sys_date DATE,
                                           IN ID CHAR(3),
                                           IN turn_number int)
BEGIN
	DECLARE v_char_name VARCHAR(50);
    SET v_char_name = get_character_name(ID);

	SELECT * FROM filtered_game_state_view
    WHERE `System Date` = DATE_FORMAT(sys_date, '%m/%d/%Y')
      AND `Character Name` = v_char_name
      AND `Turn Number` = turn_number;
END$$
DELIMITER ;
    
     DROP PROCEDURE IF EXISTS `get_players_view`;
    DELIMITER $$
    
    CREATE PROCEDURE get_players_view ()
    BEGIN
		SELECT
        v.`Player ID`,
        v.`Player Name`,
        COUNT(c.character_ID) AS `Number of Characters`
        FROM `player_view` v
        LEFT JOIN characters c ON v.`player ID` = c.player_ID
        GROUP BY v.`player ID`, v.`Player Name`
        ORDER BY v.`player ID` ASC;
    END$$
    DELIMITER ;
    
     DROP PROCEDURE IF EXISTS `get_characters_view`;
    DELIMITER $$
    
    CREATE PROCEDURE get_characters_view ()
    BEGIN
		SELECT * FROM character_view;
    END$$
    DELIMITER ;
    
     DROP PROCEDURE IF EXISTS `get_conditions`;
    DELIMITER $$
    
    CREATE PROCEDURE get_conditions(IN sys_date date,
									ID char(3),
                                    turn_number decimal(3,0))
	BEGIN
		SELECT condition1, condition2 FROM game_states
        WHERE sys_date = system_date AND ID = character_ID AND turn_number = turn;
    END$$
    DELIMITER ;
    
	DROP PROCEDURE IF EXISTS `get_afflictions`;
    DELIMITER $$
    
    CREATE PROCEDURE get_afflictions(IN sys_date date,
									    ID char(3),
                                        turn_number decimal(3,0))
	BEGIN
		SELECT affliction1, affliction2 FROM game_states
        WHERE sys_date = system_date AND ID = character_ID AND turn_number = turn;
    END$$
    DELIMITER ;
    
     DROP PROCEDURE IF EXISTS `get_overland_speed`;
    DELIMITER $$
    CREATE PROCEDURE get_overland_speed (IN sys_date date,
									        ID char(3),
                                            turn_number decimal(3,0))
	BEGIN
		SELECT overland_speed FROM game_states
        WHERE sys_date = system_date AND ID = character_ID AND turn_number = turn;
    END$$
    DELIMITER ;
    
     DROP PROCEDURE IF EXISTS `get_filtered_overland_speed`;
    DELIMITER $$
    CREATE PROCEDURE get_filtered_overland_speed (IN sys_date date,
									        ID char(3),
                                            turn_number decimal(3,0))
	BEGIN
		SELECT overland_speed FROM filtered_game_states
        WHERE sys_date = system_date AND ID = character_ID AND turn_number = turn;
    END$$
    DELIMITER ;

/*Create Operations*/
 DROP PROCEDURE IF EXISTS `new_player`;
DELIMITER $$

CREATE PROCEDURE new_player (IN pID char(2),
                                p_name varchar(50))
BEGIN
	INSERT INTO players VALUES
    (pID, p_name);
END$$
DELIMITER ;

 DROP PROCEDURE IF EXISTS `new_character`;
DELIMITER $$

CREATE PROCEDURE new_character (IN cID char(3),
                                IN c_name varchar(50),
								IN pID char(3))
BEGIN
	INSERT INTO characters(character_ID, character_name, player_ID) 
    VALUES (cID, c_name, pID);
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS `new_game_state`;
DELIMITER $$
CREATE PROCEDURE new_game_state (IN sys_date date,
									cID char(3))
BEGIN
	INSERT INTO game_states VALUES
    (sys_date, cID, 1, 0, 'Fair', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 15.5);
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS `new_filtered_game_state`;
DELIMITER $$
CREATE PROCEDURE new_filtered_game_state (IN sys_date date, cID char(3), turn int,
    starve boolean, sub_level enum('Poor','Fair','Good'), speed decimal(3,1),
    p_doors int, p_traps int, p_treasure int, p_cursed int, p_disease int, p_poison int,
    p_condition1 varchar(50), p_condition2 varchar(50))
BEGIN
    INSERT INTO filtered_game_states VALUES
    (sys_date, cID, turn, starve, sub_level, p_condition1, p_condition2, NULL, NULL,
     p_doors, p_traps, p_treasure, p_cursed, p_disease, p_poison, speed);
END$$
DELIMITER ;

/*Update Operations*/
DROP PROCEDURE IF EXISTS `carry_forward_secrets`;
DELIMITER $$
CREATE PROCEDURE carry_forward_secrets(
    IN sys_date DATE, IN ID CHAR(3), IN turn_number INT,
    IN p_doors INT, IN p_traps INT, IN p_treasure INT,
    IN p_cursed INT, IN p_disease INT, IN p_poison INT,
    IN p_condition1 VARCHAR(50), IN p_condition2 VARCHAR(50),
    IN p_affliction1 VARCHAR(25), IN p_affliction2 VARCHAR(25))
BEGIN
    UPDATE game_states
    SET secret_doors = secret_doors + p_doors,
        secret_traps = secret_traps + p_traps,
        secret_treasure = secret_treasure + p_treasure,
        secret_cursed_treasure = secret_cursed_treasure + p_cursed,
        secret_airborne_disease = secret_airborne_disease + p_disease,
        secret_poison_gas = secret_poison_gas + p_poison,
        condition1 = p_condition1,
        condition2 = p_condition2,
        affliction1 = p_affliction1,
        affliction2 = p_affliction2
    WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
END$$
DELIMITER ;

 DROP PROCEDURE IF EXISTS `update_turn`;
DELIMITER $$

CREATE PROCEDURE update_turn(IN new_turn int,
								sys_date date,
								ID char(3),
                                turn_number int)
BEGIN
	UPDATE game_states
    SET turn = new_turn
    WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
    
    UPDATE filtered_game_states
    SET turn = new_turn
    WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
END$$
DELIMITER ;

/*when a character discovers treasure, their subsistence level increases. If a character has a subsistence level of 'Poor', then starvation mode activates as a boolean
value. If I had a game engine, then it would impose some kind of penalty to the true game state for being in starvation mode. In the interests of keeping things
simple, I am not imposing a penalty for starvation mode.*/
 DROP PROCEDURE IF EXISTS `increase_subsistence`;
DELIMITER $$

CREATE PROCEDURE increase_subsistence(IN sys_date date,
								         ID char(3),
                                         turn_number int)
BEGIN
UPDATE game_states
SET
	starvation_mode = CASE
		WHEN subsistence_level = 'Poor' THEN 0
        ELSE starvation_mode
	END,
    subsistence_level = CASE
		WHEN subsistence_level = 'Poor' THEN 'Fair'
        WHEN subsistence_level = 'Fair' THEN 'Good'
        ELSE subsistence_level
	END
WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;

UPDATE filtered_game_states
SET
	starvation_mode = CASE
		WHEN subsistence_level = 'Poor' THEN 0
        ELSE starvation_mode
	END,
    subsistence_level = CASE
		WHEN subsistence_level = 'Poor' THEN 'Fair'
        WHEN subsistence_level = 'Fair' THEN 'Good'
        ELSE subsistence_level
	END
WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
END$$
DELIMITER ;

 DROP PROCEDURE IF EXISTS `update_condition`;
DELIMITER $$

/*A character will know immediately what conditions they are subjected to, so both the true game state and the filtered game state will show  matching conditions.
However they probably wont know why they are subjected to those conditions.*/
CREATE PROCEDURE update_condition(IN new_condition varchar(25),
                                      sys_date date,
                                      ID char(3),
                                      turn_number int)
BEGIN
	IF (SELECT condition1 FROM game_states WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number) IS NULL THEN
		UPDATE game_states
        SET condition1 = new_condition
        WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
        
        UPDATE filtered_game_states 
        SET condition1 = new_condition
        WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
	else
		UPDATE game_states
        SET condition2 = new_condition
        WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
        
        UPDATE filtered_game_states
        SET condition2 = new_condition
        WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
	END IF;
END$$
DELIMITER ;

/*A character wont instantly know what afflictions they are subjected to unless they take some kind of action to determine what they are afflicted with. For example, suppose someone gets
poisoned. That person does not instantly know they have been poisoned, but they may figure it out in time. The true game state (game_states) will reflect that they have been
poisoned, but the filtered game state wont show that they have been poisoned because the character is not instantly aware of it.*/
DROP PROCEDURE IF EXISTS `update_affliction`;
DELIMITER $$


CREATE PROCEDURE update_affliction(IN new_affliction varchar(25),
                                      sys_date date,
                                      ID char(3),
                                      turn_number decimal(3,0))
BEGIN
	IF (SELECT affliction1 FROM game_states WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number) IS NULL THEN
        UPDATE game_states
        SET affliction1 = new_affliction
        WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
	else
        UPDATE game_states
        SET affliction2 = new_affliction
        WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
	END IF;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS `update_secret_doors`;
DELIMITER $$

CREATE PROCEDURE update_secret_doors(IN sys_date date,
									    ID char(3),
                                        turn_number int)
BEGIN
	UPDATE game_states
    SET secret_doors = secret_doors + 1
     WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS `update_filtered_secret_doors`;
DELIMITER $$

CREATE PROCEDURE update_filtered_secret_doors(IN sys_date date,
									          ID char(3),
                                              turn_number int)
BEGIN
	UPDATE filtered_game_states
    SET secret_doors = secret_doors + 1
	WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS `update_secret_traps`;
DELIMITER $$

CREATE PROCEDURE update_secret_traps(IN sys_date date,
									    ID char(3),
                                        turn_number int)
BEGIN
	UPDATE game_states
    SET secret_traps = secret_traps + 1
     WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS `update_filtered_secret_traps`;
DELIMITER $$
CREATE PROCEDURE update_filtered_secret_traps(IN sys_date date,
									             ID char(3),
                                                 turn_number int)
BEGIN
	UPDATE filtered_game_states
    SET secret_traps = secret_traps + 1
	WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS `update_secret_treasure`;
DELIMITER $$
CREATE PROCEDURE update_secret_treasure(IN sys_date date,
										   ID char(3),
                                           turn_number int)
BEGIN
	UPDATE game_states
    SET secret_treasure = secret_treasure + 1
	WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS `update_filtered_secret_treasure`;
DELIMITER $$
CREATE PROCEDURE update_filtered_secret_treasure(IN sys_date date,
									                ID char(3),
                                                    turn_number int)
BEGIN
	UPDATE filtered_game_states
    SET secret_treasure = secret_treasure + 1
	WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS `update_secret_cursed_treasure`;
DELIMITER $$
CREATE PROCEDURE update_secret_cursed_treasure(IN sys_date date,
									              ID char(3),
                                                  turn_number int)
BEGIN
	UPDATE game_states
    SET secret_cursed_treasure = secret_cursed_treasure + 1
	WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS `update_filtered_secret_cursed_treasure`;
DELIMITER $$
CREATE PROCEDURE update_filtered_secret_cursed_treasure(IN sys_date date,
									                ID char(3),
                                                    turn_number int)
BEGIN
	UPDATE filtered_game_states
    SET secret_cursed_treasure = secret_cursed_treasure + 1
	WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS `update_secret_airborne_disease`;
DELIMITER $$
CREATE PROCEDURE update_secret_airborne_disease(IN sys_date date,
									               ID char(3),
                                                   turn_number int)
BEGIN
	UPDATE game_states
    SET secret_airborne_disease = secret_airborne_disease + 1
	WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS `update_filtered_secret_airborne_disease`;
DELIMITER $$
CREATE PROCEDURE update_filtered_secret_airborne_disease(IN sys_date date,
									                ID char(3),
                                                    turn_number int)
BEGIN
	UPDATE filtered_game_states
    SET secret_airborne_disease = secret_airborne_disease + 1
	WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS `update__secret_poison_gas`;
DELIMITER $$
CREATE PROCEDURE update_secret_poison_gas(IN sys_date date,
									         ID char(3),
                                             turn_number int)
BEGIN
	UPDATE game_states
    SET secret_poison_gas = secret_poison_gas + 1
	WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS `update_filtered_secret_poison_gas`;
DELIMITER $$
CREATE PROCEDURE update_filtered_secret_poison_gas(IN sys_date date,
									                ID char(3),
                                                    turn_number int)
BEGIN
	UPDATE filtered_game_states
    SET secret_poison_gas = secret_poison_gas + 1
	WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS `update_overland_speed`;
DELIMITER $$
CREATE PROCEDURE update_overland_speed (IN sys_date date,
									       ID char(3),
                                           turn_number int,
                                           new_overland_speed decimal(3,1))
BEGIN
	UPDATE game_states
    SET overland_speed = new_overland_speed
    WHERE sys_date = system_date AND ID = character_ID AND turn_number = turn;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS `update_filtered_overland_speed`;
DELIMITER $$
CREATE PROCEDURE update_filtered_overland_speed (IN sys_date date,
									       ID char(3),
                                           turn_number int,
                                           new_overland_speed decimal(3,1))
BEGIN
	UPDATE filtered_game_states
    SET overland_speed = new_overland_speed
    WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
END$$
DELIMITER ;

/*Delete Operations*/
DROP PROCEDURE IF EXISTS `delete_filtered_game_state`;
DELIMITER $$
CREATE PROCEDURE delete_filtered_game_state(IN sys_date date,
											   ID char(3),
                                               turn_number int)
BEGIN
	DELETE FROM filtered_game_states
    WHERE system_date = sys_date AND character_ID = ID AND turn = turn_number;
END$$
DELIMITER ;