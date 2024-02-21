import os
import sys
from os.path import realpath
from pathlib import Path
import shutil
import cv2
from pyzbar.pyzbar import decode
from pyzbar.wrapper import ZBarSymbol


debug_output = True


def scan_barcodes(image_name, min_barcode_int, max_barcode_int) -> [str]:
    image_path = f"images/in/{image_name}"
    image = cv2.imread(image_path)
    barcodes = decode(image, symbols=[ZBarSymbol.CODE128])
    barcode_results = []
    if barcodes:
        for barcode in barcodes:
            # if debug_output: print(barcode)
            # noinspection PyTestUnpassedFixture
            barcode_text = barcode.data.decode("utf-8")
            if validate_barcode(image_name, barcode_text, min_barcode_int, max_barcode_int):
                barcode_results.append(barcode_text)
    else:
        if debug_output: print(f"{child.name}: no barcode found.")
    return barcode_results


def validate_barcode(filename, barcode_text, min_int, max_int) -> bool:
    if barcode_text.isdigit():
        if min_int < int(barcode_text) < max_int:
            if debug_output: print(f"{filename}: result: '{barcode_text}'.")
            return True
        else:
            if debug_output: print(f"{filename}: result: '{barcode_text}' not in range.")
    else:
        if debug_output: print(f"{filename}: result: '{barcode_text}' no int.")
    return False


if __name__ == "__main__":
    min_barcode_int = 1000000
    max_barcode_int = 7000000
    if len(sys.argv) >= 2:
        min_barcode_int = sys.argv[1]
    if len(sys.argv) >= 3:
        max_barcode_int = sys.argv[2]
    print(f'minimum valid barcode: {min_barcode_int}')
    print(f'maximum valid barcode: {max_barcode_int}')
    print(f'to adjust these, run script with parameters: ... main.py <min_int> <max_int>')

    script_path, script_name = os.path.split(realpath(__file__))
    path_input = f'{script_path}/images/in/'
    path_output = f'{script_path}/images/out/'
    os.makedirs(path_input, exist_ok=True)
    os.makedirs(path_output, exist_ok=True)
    previous_result = None
    reset_count = 0
    for child in sorted(Path(path_input).iterdir()):
        if child.is_file():
            results = scan_barcodes(child.name, 1000000, 7000000)
            if len(results) == 1:
                previous_result = results[0]
                reset_count = 0
            elif len(results) >= 2:
                previous_result = results[0]
                reset_count = 0
                for result in results[1:]:
                    previous_result += f"_{result}"
            reset_count += 1
            shutil.copyfile(f"{path_input}{child.name}", f"{path_output}{previous_result}-{reset_count}.jpg")
