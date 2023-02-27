// Game UI starts here
const canvas = document.querySelector("canvas");
const canvContext = canvas.getContext("2d");

canvas.width = 1024;
canvas.height = 576;
const gravity = 0.2;

canvContext.fillRect(0, 0, canvas.width, canvas.height);

class Sprite {
  constructor({player_id, player_position, player_activity, player_status, player_inventory}) {
    this.player_id = player_id;
    this.player_position = player_position;
    this.player_activity = player_activity;
    this.player_status = player_status;
    this.player_inventory = player_inventory;
  }

  draw() {
    canvContext.fillStyle = "red";
    console.log("will be drawing with: " + this.player_position.x + " " + this.player_position.y);
    canvContext.fillRect(this.player_position.x, this.player_position.y, 50, 100);
  }

  update({player_position, player_activity, player_status, player_inventory}) {
    this.player_position.x = player_position.x;
    this.player_position.y = player_position.y;

    // if (this.position.y + this.height + this.velocity.y >= canvas.height){
    //   this.velocity.y = 0
    // } else this.velocity.y += gravity
  }
}

// Used to redraw everything on the screen
function update_ui(update_ui_all_players){
  console.log("Drawing new scene " + update_ui_all_players);
  // Reset UI background 
  canvContext.fillStyle = "black";
  canvContext.fillRect(0, 0, canvas.width, canvas.height);
  for (let index_player = 0; index_player < update_ui_all_players.length; index_player++){
    update_ui_all_players[index_player].draw();
  }
}

// Messages from Server Begins Here 
// Setup Global vars for all players, EventSource
let array_of_all_players = Array()
let eventSource = new EventSource("/listen");
eventSource.addEventListener("message", function(e) {
  console.log(e.data);
}, false)

eventSource.addEventListener("updatePlayers", function(update_player_data_input) {
  // Parse incoming data [{"player_user_name", "player_coordinates": {"x", "y"}, "player_activity", "player_status", "player_inventory"},..]
  let update_player_data = JSON.parse(update_player_data_input.data)
  // Loop every element from incoming data
  for (let index_player = 0; index_player < update_player_data.length; index_player++){
    // Get data for player: name, position[x,y], activity(attacking, def..), status(health), inventory(future feature)
    player_name = update_player_data[index_player].player_user_name;
    player_position = update_player_data[index_player].player_coordinates;
    player_activity = update_player_data[index_player].player_activity;
    player_status = update_player_data[index_player].player_status;
    player_inventory = update_player_data[index_player].player_inventory;
    // Check if we have any players, if not -> add first user as new player (Sprite)
    if (array_of_all_players.length === 0) { 
      console.log("Creting First Player");
      array_of_all_players.push(new Sprite({
        player_id: player_name, 
        player_position: {x: player_position.x, y: player_position.y}, 
        player_activity: player_activity, 
        player_status: player_status,
        player_inventory: player_inventory
      }));
     } else {
      // If there are players already in game loop and find matching player_name -> update this player
      for (let index_of_logged_players = 0; index_of_logged_players < array_of_all_players.length; index_of_logged_players++){
        console.log("Inside Loop Name is: " + array_of_all_players[index_of_logged_players].player_id);
        if (array_of_all_players[index_of_logged_players].player_id == player_name) { 
          console.log("Updating Player")
          array_of_all_players[index_of_logged_players].update({
            player_position: {x: player_position.x, y: player_position.y}, 
            player_activity: player_activity, 
            player_status: player_status,
            player_inventory: player_inventory
          });
          break; 
        } else {
          // If there is no matching name in the player list, create new player (Sprite) and add it to the list
          console.log("Adding Player")
          array_of_all_players.push(new Sprite({
            player_id: player_name, 
            player_position: {x: player_position.x, y: player_position.y}, 
            player_activity: player_activity, 
            player_status: player_status,
            player_inventory: player_inventory
          }))
        }
      }
    }
  }
  update_ui(update_ui_all_players=array_of_all_players)
}, true)

// Detect and send movement starts here

window.addEventListener("keydown", (event) => {
  let key_pressed = event.key 
  const request = new XMLHttpRequest();
  request.open("POST", "#");
  request.send(key_pressed);
})


// const player = new Sprite({
//   position: {
//     x: 0,
//     y: 0
//   },
//   velocity: {
//     x: 0,
//     y: 0
//   }
// })

// player.draw()

// const enemy = new Sprite({
//   position: {
//     x: 400,
//     y: 100
//   },
//   velocity: {
//     x: 0,
//     y: 0
//   }
// })

// enemy.draw()

// function animate() {
//   window.requestAnimationFrame(animate)
//   canvContext.fillStyle = "black"
//   canvContext.fillRect(0, 0, canvas.width, canvas.height)
//   player.update()
//   enemy.update()
// }

// animate()

