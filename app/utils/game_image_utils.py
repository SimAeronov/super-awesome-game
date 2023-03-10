import cv2
from random import randint
from typing import Tuple, List
from os import listdir, path, remove

#NOTE: Add variable for all system paths so that I don't have to edit it everywhere when I switch to the server
#NOTE: Bad practice with returning print() for exception handling, update to log ASAP
def generate_image_for_player(name_of_map:str = "map_0", name_of_player:str = "defaultSprite") -> Tuple[int, int]:
    name_of_player_for_image = f"{name_of_player}-{name_of_map}"
    image_open_path = path.join(r"app/static/images/" + name_of_map)
    image_save_path = path.join(r"app/static/images/" + name_of_player_for_image)
    
    image = cv2.imread(image_open_path)
    target_x = randint(0, 576)
    target_y = randint(0, 1024)
    crop_image = image[target_y:target_y+30, target_x:target_x+30]
    cv2.imwrite(image_save_path, crop_image)
    return(target_x, target_y)

def clear_generated_images(list_of_all_maps:List[str], name_of_map:str):
    # Make shallow copy
    list_of_all_required_images = list_of_all_maps.copy()
    list_of_all_required_images.extend(["defaultSprite.png", "map_0.png", "puzzle_img.png"])
    for image_name in listdir(r"app/static/images/"):
        if image_name not in list_of_all_required_images and image_name[image_name.rfind("-")+1:] != name_of_map:
            file_to_be_deleted: str = path.join(r"app/static/images/" + image_name)
            if path.isfile(file_to_be_deleted):
                remove(file_to_be_deleted)
            else:
                print(f"Error: '{file_to_be_deleted}' Not found")

