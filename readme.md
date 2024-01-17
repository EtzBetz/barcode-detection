# About
This python script iterates through all images in `./images/in/`, searches for a barcode in each image and puts the image into a folder `./images/out/<barcode-string>/`.\
If no barcode is found in one image, the image is put into the previous detected barcodes' folder.
# Requirements
- opencv-python
- pyzbar
  - pyzbar needs zbar (c library) installed.
  - on macOS: `brew install zbar`
