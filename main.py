import os
from pathlib import Path
import shutil
import cv2
from pyzbar.pyzbar import decode
from pyzbar.wrapper import ZBarSymbol


def scan_barcodes(image_name) -> [str]:
    image_path = f"images/in/{image_name}"
    image = cv2.imread(image_path)
    barcodes = decode(image, symbols=[ZBarSymbol.CODE128])
    barcode_results = []
    if barcodes:
        for barcode in barcodes:
            print(barcode)
            # noinspection PyTestUnpassedFixture
            barcode_text = barcode.data.decode("utf-8")
            if validate_barcode(image_name, barcode_text):
                barcode_results.append(barcode_text)
    else:
        print(f"{child.name}: no barcode found.")
    return barcode_results


def validate_barcode(filename, barcode_text) -> bool:
    if barcode_text.isdigit():
        if 1000000 < int(barcode_text) < 7000000:
            print(f"{filename}: result: '{barcode_text}'.")
            return True
        else:
            print(f"{filename}: result: '{barcode_text}' not in range.")
    else:
        print(f"{filename}: result: '{barcode_text}' no int.")
    return False


if __name__ == "__main__":
    path = './images/in/'
    previous_result = None
    for child in sorted(Path(path).iterdir()):
        if child.is_file():
            results = scan_barcodes(child.name)
            if len(results) == 1:
                previous_result = results[0]
            elif len(results) >= 2:
                previous_result = results[0]
                for result in results[1:]:
                    previous_result += f"_{result}"
            path_name = f"images/out/{str(previous_result)}/"
            os.makedirs(path_name, exist_ok=True)
            # new_image_path = os.path.join(os.path.dirname(image_path), new_image_name)
            # os.rename(image_path, new_image_path)
            shutil.copyfile(f"{path}{child.name}", f"{path_name}{child.name}")
