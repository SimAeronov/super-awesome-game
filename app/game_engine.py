from pydantic import BaseModel, validator, root_validator
from typing import Union, List, Optional, Any, Dict

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
    player_activity: str
    player_status: int
    player_inventory: str

    # Make sure that user has: Name, x/y_coordinates, Status(Health). 
    # Also username should be more than 3 chars and to avoid duplicate names -> lower case
    @root_validator(pre=True)
    @classmethod
    def check_all_data_is_entered(cls, values:'dict[str, Union[str, int]]'):
        """ Validate that all data is provided before proceeding"""
        if "player_user_name" not in values or "player_coordinates" not in values or "player_status" not in values:
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
    __slots__ = "_all_players"

    def __init__(self) -> None:
        self._all_players: List[Player] = list()
    
    def player_input(self,pressed_key: str, user_id: Optional[str] = "simple_user"):
        user_id = user_id.lower() # type: ignore
        pressed_key = pressed_key.lower()
        if not self._all_players:
            self._all_players.append(Player(player_user_name=user_id, player_coordinates={"x": 0, "y": 0}, 
                                            player_activity="idle", player_status=100, player_inventory="empty"
                                            ))
            return
        if user_id not in [player.player_user_name for player in self._all_players]:
            self._all_players.append(Player(player_user_name=user_id, player_coordinates={"x": 0, "y": 0}, 
                                            player_activity="idle", player_status=100, player_inventory="empty"
                                            ))
            return
        user_id_to_update = [player.player_user_name for player in self._all_players].index(user_id)

        if pressed_key == "a":
            self._all_players[user_id_to_update].player_coordinates["x"] -= 10
        if pressed_key == "d":
            self._all_players[user_id_to_update].player_coordinates["x"] += 10
        # self._all_players[user_id_to_update].player_coordinates_y = y_coordinates
        
    def update_players_ui(self):
        list_of_players: List[Any] = list()
        for player in self._all_players:
            list_of_players.append(player.dict())
        return list_of_players

# NewGame = Game()
# NewGame.player_input(user_id="Boicho", pressed_key="w")
# NewGame.player_input(user_id="Borko", pressed_key="w")
# print(NewGame.update_players_ui())