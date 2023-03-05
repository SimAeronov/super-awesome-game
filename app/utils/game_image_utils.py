import cv2
from random import randint
from typing import Tuple

def generate_image_for_player(name_of_map:str, name_of_player:str) -> Tuple[int, int]:
    image_open_path = r"app/static/images/" + name_of_map
    image_save_path = r"app/static/images/" + name_of_player + ".png"
    
    image = cv2.imread(image_open_path)
    target_x = randint(0, 576)
    target_y = randint(0, 1024)
    crop_image = image[target_y:target_y+30, target_x:target_x+30]
    cv2.imwrite(image_save_path, crop_image)
    return(target_x, target_y)
