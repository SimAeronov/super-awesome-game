from pydantic import BaseModel, validator, root_validator
from random import randint
from typing import Union, Optional, Dict, Tuple
from utils.game_exceptions import playerUserNameError, playerMissingDataError, gameAttributesDataError

# Setup new player model
class Player(BaseModel):
    player_user_name: str
    player_coordinates: Dict[str,int]
    player_dimensions: Optional[Dict[str,int]] = None
    player_win_coord: Optional[Tuple[int, int]] = None

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

    @root_validator(pre=True)
    def validate_player_or_curtain(cls, values): # type: ignore
        if values["player_user_name"][:7] == "curtain":
            values["player_win_coord"] = None
        else: 
            values["_player_win_coord"] = (randint(0, 1024), randint(0, 576))

        return values # type: ignore


    class Config:
        """Pydantic config class"""
        anystr_lower = True
        # exclude = {"_player_win_coord"}
    

class GameAttributes(BaseModel):
    game_map_name: str
    game_state: str

    @root_validator(pre=True)
    @classmethod
    def check_all_game_data_is_entered(cls, values:'dict[str, Union[str, int]]'):
        """ Validate that all data is provided before proceeding"""
        if "game_map_name" not in values or "game_state" not in values:
            raise gameAttributesDataError(message="Error, game attributes should include name of map and status of game")
        return values