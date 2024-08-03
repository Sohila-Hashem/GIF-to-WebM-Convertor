import os
import sys
import shutil
import subprocess
from PIL import Image

videos_format = ["webm", "mp4", "mov", "gif"]
images_format = ["png", "jpg", "jpeg", "webp"]

def main():    
    source_folder = sys.argv[1]
    output_folder = sys.argv[2]
    from_format = sys.argv[3]
    to_format = sys.argv[4]
    action_after_end = sys.argv[5]

    # utils
    def replace_file(source_path, output_path, file_to_move):
            shutil.replace(f'{source_path}/{file_to_move}.{from_format}', f'{output_path}/{file_to_move}.{to_format}')

    def move_file(output_path, file_to_move):
            os.move(f'{output_path}/{file_to_move}.{to_format}')

    supported_actions = {
        "replace": replace_file,
        "move": move_file, 
        "rp": replace_file, 
        "mv": move_file
    }

    is_action_provided = action_after_end in supported_actions
    source_path = os.path.join(os.path.dirname(__file__), source_folder)
    output_path = os.path.join(os.path.dirname(__file__), output_folder)

    if not (os.path.exists(source_path)):
        print("Source path not found!")
        return
    
    if (not from_format or not to_format):
        print("Please provide source and target format!")
        return

    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)

    # checking if the source and target format are supported video formats in the output folder
    if from_format in videos_format and to_format in videos_format:
        for video in os.listdir(source_path):
            if video.endswith(from_format):
                # check if the converted video already exists
                if os.path.exists(f'{output_folder}/{video.split(".")[0]}.{to_format}'):
                    print (f"{video.split('.')[0]}.{to_format} already exists!")
                else:
                    subprocess.run(f'ffmpeg -i {source_folder}/{video} -c vp9 -b:v 0 -crf 41 {output_folder}/{video.split(".")[0]}.{to_format}')
                    if (is_action_provided):
                        supported_actions[action_after_end](output_path, video.split(".")[0], source_path=source_folder)
    # checking if the source and target format are supported image formats
    elif from_format in images_format and to_format in images_format:
        for image in os.listdir(source_path):
            if image.endswith(from_format):
                # check if the converted image already exists in the output folder
                if os.path.exists(f'{output_folder}/{image.split(".")[0]}.{to_format}'):
                    print (f"{image.split('.')[0]}.{to_format} already exists!")
                else:
                    im = Image.open(f'{source_folder}/{image}')
                    im.save(f'{output_folder}/{image.split(".")[0]}.{to_format}')
                    if (is_action_provided):
                        supported_actions[action_after_end](output_path, image.split(".")[0], source_path=source_folder)
    else:
        print("Please provide valid/supported source and target format!")
        return
    

    print("Done!")

if __name__ == "__main__":
    main()