from typing import List, Optional, Any, Tuple, Dict
from random import randint, choice
from utils.game_entity_classes import Player, GameAttributes
from utils.game_image_utils import generate_image_for_player, clear_generated_images
from utils.extensions import db
from menu_interfaces.menus import users
from sqlalchemy import func

# Create Game class
class Game:
    """
        Initiate Game, use player_input(pressed_key) to update players, use update_players_ui() to retrieve ui data
    """
    __slots__ = ("_all_players", "_canvasWidth", "_canvasHeight", "_nameOfMap", "_game_state", "list_of_all_maps")

    def __init__(self) -> None:
        self._all_players: List[Player] = list()
        self._canvasWidth: int = 1024
        self._canvasHeight: int = 576
        # In the future turn this to data from database
        self.list_of_all_maps: List[str] = ["map_1.png", "map_2.png", "map_3.png", "map_4.png", "map_5.png",
                                            "map_6.png", "map_7.png", "map_8.png", "map_9.png", "map_10.png",
                                            "map_11.png", "map_12.png", "map_13.png", "map_14.png", "map_15.png"
                                            ]
        self._nameOfMap: str = choice(self.list_of_all_maps)
        self._game_state: str = "Playing"
        
    
    def player_input(self,pressed_key: str, user_id: Optional[str] = "simple_user"):
        """ 
            Main method that is used to update the internal state of the game via input as user_id and pressed_key
        """
        self.updateCurtains()
        user_id = user_id.lower() # type: ignore
        pressed_key = pressed_key.lower()
        if user_id not in [player.player_user_name for player in self._all_players]:
            self._all_players.append(Player(player_user_name=user_id,
                                             player_coordinates={"x": randint(0, 1024), "y": randint(0, 576)},
                                             player_win_coord=generate_image_for_player(name_of_map=self._nameOfMap, name_of_player=user_id)
                                             ))
            return
        user_id_to_update = [player.player_user_name for player in self._all_players].index(user_id)

        if self.checkIfPlayerWon(player_coords=self._all_players[user_id_to_update].player_coordinates,
                               player_win_coords=self._all_players[user_id_to_update].player_win_coord): # type: ignore
            if self._game_state == "Playing":
                found_user = users.query.filter(func.lower(users.user_name) == self._all_players[user_id_to_update].player_user_name).first() # type: ignore 
                found_user.player_score += 1 # type: ignore 
                db.session.commit() # type: ignore 
            self._game_state = "Winner: " + self._all_players[user_id_to_update].player_user_name

        if pressed_key == "a" and self._all_players[user_id_to_update].player_coordinates["x"] > 0:
            self._all_players[user_id_to_update].player_coordinates["x"] -= 10
        if pressed_key == "d" and self._all_players[user_id_to_update].player_coordinates["x"]+25 < self._canvasWidth:
            self._all_players[user_id_to_update].player_coordinates["x"] += 10
        if pressed_key == "w" and self._all_players[user_id_to_update].player_coordinates["y"] > 0:
            self._all_players[user_id_to_update].player_coordinates["y"] -= 10
        if pressed_key == "s" and self._all_players[user_id_to_update].player_coordinates["y"]+25 < self._canvasHeight:
            self._all_players[user_id_to_update].player_coordinates["y"] += 10
        
    def update_players_ui(self):
        """
            Method used to return the current state of the game, check for reset or win condition
        """
        list_of_players: List[Any] = list()
        list_of_players.append(GameAttributes(game_map_name=self._nameOfMap, game_state=self._game_state).dict())
        if self._game_state == "Reset":
            self._game_state = "Playing"
        for player in self._all_players:
            list_of_players.append(player.dict(exclude={"player_win_coord"}, exclude_none=True))
        return list_of_players

    def generateCurtains(self) -> List[Player]:

        list_of_curtains: List[Player] = list()
        for inex_of_curtain in range(3):
            curtain_coord_x = randint(0, 1024)
            curtain_coord_y = randint(0, 576)
            curtain_dim_x = randint(100, 300)
            curtain_dim_y = randint(100, 300)
            list_of_curtains.append(Player(player_user_name=f"curtain_{inex_of_curtain}",
                                         player_coordinates={"x": curtain_coord_x, "y": curtain_coord_y},
                                           player_dimensions={"x": curtain_dim_x, "y": curtain_dim_y}))
        return list_of_curtains

    def updateCurtains(self):
        list_of_curtains = self.generateCurtains()
        for curtain in list_of_curtains:
            index_of_curtains = next((index_curtains for index_curtains, player in enumerate(self._all_players) if player.player_user_name == curtain.player_user_name), -1)
            if index_of_curtains > -1:
                self._all_players[index_of_curtains] = curtain
            else:
                self._all_players.append(curtain)

    # Gotta fix the types for player_coords and player_win_coords
    def checkIfPlayerWon(self, player_coords:Dict[str,int], player_win_coords:Tuple[int, int]):
        if player_coords["x"] > player_win_coords[0] - 15 and player_coords["x"] < player_win_coords[0] + 15:
            if player_coords["y"] > player_win_coords[1] - 15 and player_coords["y"] < player_win_coords[1] + 15:
                return True
        return False
    
    def resetGame(self):
        self._game_state = "Reset"
        self._nameOfMap: str = choice(self.list_of_all_maps)
        self._all_players.clear()
        clear_generated_images(list_of_all_maps=self.list_of_all_maps)


# NewGame = Game()
# NewGame.player_input(user_id="Boicho", pressed_key="w")
# NewGame.player_input(user_id="Boicho", pressed_key="w")
# # NewGame.player_input(user_id="Borko", pressed_key="w")
# print(NewGame.update_players_ui())