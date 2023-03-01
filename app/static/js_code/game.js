// Game UI starts here
const canvas = document.querySelector("canvas");
const canvContext = canvas.getContext("2d");

canvas.width = 1024;
canvas.height = 576;
const gravity = 0.2;

canvContext.fillRect(0, 0, canvas.width, canvas.height);


// Used to redraw everything on the screen
function update_ui(update_ui_all_players){
  console.log("Drawing new scene " + update_ui_all_players);
  // Reset UI background 
  canvContext.fillStyle = "black";
  canvContext.fillRect(0, 0, canvas.width, canvas.height);
  background.draw()
  for (let index_player = 0; index_player < update_ui_all_players.length; index_player++){
    update_ui_all_players[index_player].draw();
  }
}

// Messages from Server Begins Here 
// Setup Global vars for all players, EventSource
const background = new backgroundSprite({
  position: {
    x: 0,
    y: 0
  },
  imageSrc: 'static/images/background_1.png'
})

let array_of_all_players = Array()
function GetUpdatePlayerDataInput(update_player_data_input) {
  // Parse incoming data [{"player_user_name", "player_coordinates": {"x", "y"}, "player_activity", "player_status", "player_inventory"},..]
  // Loop every element from incoming data
  for (let index_player = 0; index_player < update_player_data_input.length; index_player++){
    // Get data for player: name, position[x,y], activity(attacking, def..), status(health), inventory(future feature)
    player_name = update_player_data_input[index_player].player_user_name;
    player_position = update_player_data_input[index_player].player_coordinates;
    if (player_name.slice(0, 4) != "wall"){
      // Check if we have any players, if not -> add first user as new player (Sprite)
      let player_id_inside_array = array_of_all_players.findIndex(player => player.player_id === player_name);
      if (player_id_inside_array > -1) {
        console.log("Updating Player: " + player_name)
        array_of_all_players[player_id_inside_array].update({
          player_position: {x: player_position.x, y: player_position.y}, 
        });
      } else {
            // If there is no matching name in the player list, create new player (Sprite) and add it to the list
            console.log("Adding Player")
            array_of_all_players.push(new Sprite({
              player_id: player_name, 
              player_position: {x: player_position.x, y: player_position.y}, 
            }))
        }
    } else {
      // Add walls layout
      player_dimensions = update_player_data_input[index_player].player_dimensions
      let player_id_inside_array = array_of_all_players.findIndex(player => player.player_id === player_name);
      if (player_id_inside_array > -1) {
        array_of_all_players[player_id_inside_array].update({
          wall_position: player_position, wall_dimensions: player_dimensions 
        });
      } else {
        array_of_all_players.push(new wallSprite({
          player_id: player_name, 
          wall_position: {x: player_position.x, y: player_position.y}, 
          wall_dimensions: {x: player_dimensions.x, y: player_dimensions.y}
        }))
      }
     }
  }
}

// Detect and send movement starts here

window.addEventListener("keydown", async (event) => {
  let key_pressed = event.key 
  const sendOnKey = await fetch('/listen', {
    method: "POST",
    body: key_pressed
  })

  const response = await fetch('/listen');
  const response_for_all_players = await response.json();
  console.log(response_for_all_players)
  GetUpdatePlayerDataInput(update_player_data_input=response_for_all_players)
  update_ui(update_ui_all_players=array_of_all_players)
})

