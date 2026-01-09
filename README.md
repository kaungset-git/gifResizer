# GIF Batch Resizer

A Python utility that leverages `gifsicle` to batch resize and optimize GIF files. It supports three different methods for handling aspect ratio changes: **Cropping**, **Stretching**, and **Fitting**.

## Features
* **Batch Processing**: Automatically finds all `.gif` files in the current directory.
* **Three Resize Modes**:
    1.  **Center and Crop**: Scales the GIF to cover the target area and crops the excess (ideal for filling a specific frame).
    2.  **Stretch**: Force-resizes the GIF to the exact dimensions provided.
    3.  **Original Aspect Ratio**: Resizes the GIF to fit *within* the dimensions while keeping its proportions.
* **Automatic Optimization**: Uses `gifsicle -O3` for the best possible file size compression.

## Prerequisites

You must have **gifsicle** installed on your system.

* **macOS**: `brew install gifsicle`
* **Ubuntu/Debian**: `sudo apt-get install gifsicle`
* **Windows**: Download the binary from the [gifsicle website](https://www.lcdf.org/gifsicle/) and add it to your System PATH.

## Usage

1.  Place the `resizer.py` script into the folder containing your GIFs.
2.  Run the script:
    ```bash
    python resizer.py
    ```
3.  Enter your desired width and height.
4.  Choose your aspect ratio handling method.
5.  Find your processed GIFs in the newly created subfolder (`Crop`, `Stretch`, or `OgAspectRatio`).

## Requirements
- Python 3.x
- `gifsicle` command-line tool
