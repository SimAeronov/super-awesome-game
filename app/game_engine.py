from pydantic import BaseModel, validator, root_validator
from typing import Union, List, Optional, Any, Dict
from random import randint

# Add Exceptions for New Player creation
class playerUserNameError(Exception):
    """Error raised when player name is less then 3 characters"""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class playerMissingDataError(Exception):
    """Error raised when data is missing when trying to init a player"""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


# Setup new player model
class Player(BaseModel):
    player_user_name: str
    player_coordinates: Dict[str,int]
    player_dimensions: Optional[Dict[str,int]] = None


    # Make sure that user has: Name, x/y_coordinates, Status(Health). 
    # Also username should be more than 3 chars and to avoid duplicate names -> lower case
    @root_validator(pre=True)
    @classmethod
    def check_all_data_is_entered(cls, values:'dict[str, Union[str, int]]'):
        """ Validate that all data is provided before proceeding"""
        if "player_user_name" not in values or "player_coordinates" not in values:
            raise playerMissingDataError(message="Please make sure that all required data is present")
        return values


    @validator("player_user_name")
    @classmethod
    def player_user_name_valid(cls, value:str):
        """Validator to check whether user name is less then 3 chars"""
        if len(value) < 3:
            raise playerUserNameError(value=value, message="User name too short!")
        return value
    
    class Config:
        """Pydantic config class"""
        anystr_lower = True


# Create Game class
class Game:
    """
        Initiate Game, use player_input(pressed_key) to update players, use update_players_ui() to retrieve ui data
    """
    __slots__ = ("_all_players", "_canvasWidth", "_canvasHeight")

    def __init__(self) -> None:
        self._all_players: List[Player] = list()
        self._canvasWidth: int = 1024
        self._canvasHeight: int = 576
    
    def player_input(self,pressed_key: str, user_id: Optional[str] = "simple_user"):
        self.updateWalls()
        user_id = user_id.lower() # type: ignore
        pressed_key = pressed_key.lower()
        print(f"Keyy: {pressed_key}")
        if not self._all_players:
            self._all_players.append(Player(player_user_name=user_id, player_coordinates={"x": randint(0, 1024), "y": randint(0, 576)}))
            return
        if user_id not in [player.player_user_name for player in self._all_players]:
            self._all_players.append(Player(player_user_name=user_id, player_coordinates={"x": randint(0, 1024), "y": randint(0, 576)}))
            return
        user_id_to_update = [player.player_user_name for player in self._all_players].index(user_id)

        if pressed_key == "a" and self._all_players[user_id_to_update].player_coordinates["x"] > 0:
            self._all_players[user_id_to_update].player_coordinates["x"] -= 10
        if pressed_key == "d" and self._all_players[user_id_to_update].player_coordinates["x"]+25 < self._canvasWidth:
            self._all_players[user_id_to_update].player_coordinates["x"] += 10
        if pressed_key == "w" and self._all_players[user_id_to_update].player_coordinates["y"] > 0:
            self._all_players[user_id_to_update].player_coordinates["y"] -= 10
        if pressed_key == "s" and self._all_players[user_id_to_update].player_coordinates["y"]+25 < self._canvasHeight:
            self._all_players[user_id_to_update].player_coordinates["y"] += 10
        
    def update_players_ui(self):
        list_of_players: List[Any] = list()
        for player in self._all_players:
            list_of_players.append(player.dict())
        return list_of_players

    def generateWalls(self) -> List[Player]:
        list_of_walls: List[Player] = list()
        for inex_of_wall in range(40):
            wall_coord_x = randint(0, 1024)
            wall_coord_y = randint(0, 576)
            wall_dim_x = randint(100, 300)
            wall_dim_y = randint(100, 300)
            list_of_walls.append(Player(player_user_name=f"wall_{inex_of_wall}",
                                         player_coordinates={"x": wall_coord_x, "y": wall_coord_y},
                                           player_dimensions={"x": wall_dim_x, "y": wall_dim_y}))
        return list_of_walls

    def updateWalls(self):
        list_of_walls = self.generateWalls()
        for wall in list_of_walls:
            index_of_walls = next((index_wall for index_wall, player in enumerate(self._all_players) if player.player_user_name == wall.player_user_name), -1)
            if index_of_walls > -1:
                self._all_players[index_of_walls] = wall
            else:
                self._all_players.append(wall)



# NewGame = Game()
# NewGame.player_input(user_id="Boicho", pressed_key="w")
# NewGame.player_input(user_id="Borko", pressed_key="w")
# print(NewGame.update_players_ui())