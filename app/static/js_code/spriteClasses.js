// Bad practice with all those global vars, might add 'em to class in the future.
let default_map = "map_0.png"

class backgroundSprite{
    constructor({position, imageSrc}){
      this.position = position
      this.image = new Image()
      this.image.src = imageSrc
    }
    
    draw(map_name) {
      let imageSrc = this.image.src.slice(0, this.image.src.lastIndexOf("/")+1);
      this.image.src = imageSrc + map_name
      canvContext.drawImage(this.image,this.position.x, this.position.y)
    }
  
  }
  
  class curtainSprite{
    constructor ({player_id, curtain_position, curtain_dimensions}){
      this.player_id = player_id;
      this.curtain_position = curtain_position;
      this.curtain_dimensions = curtain_dimensions;
    }
  
    draw() {
      canvContext.fillStyle = "black";
      canvContext.fillRect(this.curtain_position.x, this.curtain_position.y, this.curtain_dimensions.x, this.curtain_dimensions.y)
    }
  
    update({curtain_position, curtain_dimensions}) {
      this.curtain_position.x = curtain_position.x;
      this.curtain_position.y = curtain_position.y;
      this.curtain_dimensions.x = curtain_dimensions.x
      this.curtain_dimensions.y = curtain_dimensions.y
  
    }
  }
  
  class Sprite {
    constructor({player_id, player_position}) {
      this.player_id = player_id;
      this.player_position = player_position;
      this.player_image = new Image()
      this.player_image.src = 'static/images/defaultSprite.png'
    }
  
    draw() {
      let imageSrc = this.player_image.src.slice(0, this.player_image.src.lastIndexOf("/")+1);
      this.player_image.src = imageSrc + this.player_id + "-" + default_map
      canvContext.drawImage(this.player_image,this.player_position.x, this.player_position.y)
    }
  
    update({player_position}) {
      this.player_position.x = player_position.x;
      this.player_position.y = player_position.y;
  
    }
  }