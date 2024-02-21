import json
import os
import sys
from os.path import realpath
from pathlib import Path
import shutil
import cv2
from pyzbar.pyzbar import decode
from pyzbar.wrapper import ZBarSymbol


debug_output = True


def scan_barcodes(image_name, min_barcode, max_barcode) -> [str]:
    image_path = f"images/in/{image_name}"
    img = cv2.imread(image_path)
    barcodes = decode(img, symbols=[ZBarSymbol.CODE128])
    barcode_results = []
    if barcodes:
        handle_barcodes(image_name, min_barcode, max_barcode, barcodes, barcode_results)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        manipulation_result = manipulate_image(img, image_name, min_barcode, max_barcode, barcode_results, 80)
        if manipulation_result:
            return barcode_results
        manipulation_result = manipulate_image(img, image_name, min_barcode, max_barcode, barcode_results, 100)
        if manipulation_result:
            return barcode_results
        manipulation_result = manipulate_image(img, image_name, min_barcode, max_barcode, barcode_results, 128)
        if manipulation_result:
            return barcode_results
        manipulation_result = manipulate_image(img, image_name, min_barcode, max_barcode, barcode_results, 160)
        if manipulation_result:
            return barcode_results
        if debug_output: print(f"{child.name}: no barcode found.")
        manual_input(img, barcode_results)
    return barcode_results


def manual_input(img, barcode_results):
    cv2.imshow('bw image', img)
    cv2.waitKey()
    ans = input("number: ")
    print(ans)


def manipulate_image(img, image_name, min_barcode, max_barcode, barcode_results, threshold):
    result_img = None
    if threshold != -1:
        ret, result_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    barcodes = decode(result_img, symbols=[ZBarSymbol.CODE128])
    if barcodes:
        handle_barcodes(image_name, min_barcode, max_barcode, barcodes, barcode_results)
        return True
    else:
        # print(f"{child.name}: still no barcode found.")
        # cv2.imshow('bw image', img)
        # cv2.imshow('monochrome image', result_img)
        # cv2.waitKey()
        return False


def handle_barcodes(image_name, min_barcode, max_barcode, barcodes, barcode_results):
    for barcode in barcodes:
        # if debug_output: print(barcode)
        # noinspection PyTestUnpassedFixture
        barcode_text = barcode.data.decode("utf-8")
        if validate_barcode(image_name, barcode_text, min_barcode, max_barcode):
            barcode_results.append(barcode_text)


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
    if len(sys.argv) >= 3:
        min_barcode_int = int(sys.argv[1])
        max_barcode_int = int(sys.argv[2])
    print(f'minimum valid barcode: {min_barcode_int}')
    print(f'maximum valid barcode: {max_barcode_int}')
    if len(sys.argv) != 3:
        print(f'to adjust these, run script with parameters: ... main.py <min_int> <max_int>')

    script_path, script_name = os.path.split(realpath(__file__))
    path_input = f'{script_path}/images/in/'
    os.makedirs(path_input, exist_ok=True)
    path_output = f'{script_path}/images/out/'
    os.makedirs(path_output, exist_ok=True)
    path_error = f'{script_path}/images/error/'
    os.makedirs(path_error, exist_ok=True)
    path_json = f'{script_path}/images/'

    result_multiple = False
    barcode_map = dict()
    previous_result = "unknown"
    barcode_map[previous_result] = [0, []]
    for index, child in enumerate(sorted(Path(path_input).iterdir())):
        if child.is_file():
            results = scan_barcodes(child.name, min_barcode_int, max_barcode_int)
            # print(results)
            if len(results) > 1:
                result_multiple = True
            if result_multiple is True and len(results) != 1:
                shutil.copyfile(f"{path_input}{child.name}", f"{path_error}{child.name}")
                continue
            if len(results) == 1:
                result_multiple = False
                previous_result = results[0]
                if barcode_map.get(results[0]) is None:
                    barcode_map[previous_result] = [0, []]
            barcode_map[previous_result][0] += 1
            barcode_map[previous_result][1].append(child.name)
            # print(barcode_map[previous_result])
            shutil.copyfile(f"{path_input}{child.name}", f"{path_output}{previous_result}-{barcode_map[previous_result][0]}.jpg")
    json_str = json.dumps(barcode_map)
    with open(f'{path_json}output.json', "w") as json_file:
        json_file.write(json_str)
    print(f"finished. found {len(barcode_map)-1} barcodes.")
