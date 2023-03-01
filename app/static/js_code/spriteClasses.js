class backgroundSprite{
    constructor({position, imageSrc}){
      this.position = position
      this.image = new Image()
      this.image.src = imageSrc
    }
    
    draw() {
      canvContext.drawImage(this.image,this.position.x, this.position.y)
    }
  
  }
  
  class wallSprite{
    constructor ({player_id, wall_position, wall_dimensions}){
      this.player_id = player_id;
      this.wall_position = wall_position;
      this.wall_dimensions = wall_dimensions;
    }
  
    draw() {
      canvContext.fillStyle = "black";
      canvContext.fillRect(this.wall_position.x, this.wall_position.y, this.wall_dimensions.x, this.wall_dimensions.y)
    }
  
    update({wall_position, wall_dimensions}) {
      this.wall_position.x = wall_position.x;
      this.wall_position.y = wall_position.y;
      this.wall_dimensions.x = wall_dimensions.x
      this.wall_dimensions.y = wall_dimensions.y
  
    }
  }
  
  class Sprite {
    constructor({player_id, player_position}) {
      this.player_id = player_id;
      this.player_position = player_position;
    }
  
    draw() {
      canvContext.fillStyle = "red";
      console.log("will be drawing with: " + this.player_position.x + " " + this.player_position.y);
      canvContext.fillRect(this.player_position.x, this.player_position.y, 20, 20)
    }
  
    update({player_position}) {
      this.player_position.x = player_position.x;
      this.player_position.y = player_position.y;
  
    }
  }