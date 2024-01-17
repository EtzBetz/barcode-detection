import os
from pathlib import Path
import shutil
import cv2
from pyzbar.pyzbar import decode

def search_barcode(image_name):
    image_path = f"images/in/{image_name}"
    # print(image_path)
    image = cv2.imread(image_path)
    barcodes = decode(image)
    if barcodes:
        barcode_text = barcodes[0].data.decode("utf-8")
        return barcode_text
        path_name = f"images/out/{str(barcode_text)}/"
        os.makedirs(path_name)
        # new_image_path = os.path.join(os.path.dirname(image_path), new_image_name)
        # os.rename(image_path, new_image_path)
        shutil.copyfile(image_path, f"{path_name}/{image_name}")
        print("Renamed image")
    else:
        return None
        print("No barcode")


if __name__ == "__main__":
    path = './images/in/'
    previous_result = None
    for child in sorted(Path(path).iterdir()):
        if child.is_file():
            print(child.name)
            result = search_barcode(child.name)
            if result is not None:
                if result.isdigit():
                    if 1000000 < int(result) < 7000000:
                        previous_result = int(result)
            path_name = f"images/out/{str(previous_result)}/"
            os.makedirs(path_name, exist_ok=True)
            # new_image_path = os.path.join(os.path.dirname(image_path), new_image_name)
            # os.rename(image_path, new_image_path)
            shutil.copyfile(f"{path}{child.name}", f"{path_name}{child.name}")
