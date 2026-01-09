import os
import subprocess
import sys
import re
import shutil

def check_gifsicle_installed():
    if shutil.which("gifsicle") is None:
        print("Error: 'gifsicle' is not found on your system.")
        input("Press Enter to exit...")
        sys.exit(1)

def get_gif_dimensions(filepath):
    try:
        result = subprocess.run(
            ["gifsicle", "--info", filepath],
            capture_output=True, text=True
        )
        match = re.search(r'(\d+)x(\d+)', result.stdout)
        if match:
            return int(match.group(1)), int(match.group(2))
    except Exception as e:
        print(f"Error reading dimensions for {filepath}: {e}")
    return None, None

def process_gifs():
    check_gifsicle_installed()
    
    current_folder = os.getcwd()
    gif_files = [f for f in os.listdir(current_folder) if f.lower().endswith(".gif")]

    if not gif_files:
        print("No .gif files found in this folder!")
        input("Press Enter to exit...")
        return

    try:
        target_w = int(input("Enter target Width (px): "))
        target_h = int(input("Enter target Height (px): "))
    except ValueError:
        print("Invalid number entered.")
        return

    print("\nHow should we handle Aspect Ratio mismatches?")
    print("1. Center and Crop")
    print("2. Stretch")
    print("3. Force Keep Original Aspect Ratio")
    
    choice = input("Enter choice (1-3): ").strip()

    # Determine Folder Name and File Suffix based on choice
    if choice == "1":
        folder_name = "Crop"
        method_suffix = "_Crop"
    elif choice == "2":
        folder_name = "Stretch"
        method_suffix = "_Stretch"
    elif choice == "3":
        folder_name = "OgAspectRatio"
        method_suffix = "_OgAspectRatio"
    else:
        print("Invalid choice.")
        return

    # Create the new directory if it doesn't exist
    output_dir = os.path.join(current_folder, folder_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created folder: {folder_name}")

    optimization = "-O3" 

    for filename in gif_files:
        # Avoid processing files already inside the output directories 
        # (Though listdir here only sees files in the root)
        print(f"Processing: {filename}...")
        
        name_part, ext = os.path.splitext(filename)
        output_filename = f"{name_part}{method_suffix}{ext}"
        
        input_path = os.path.join(current_folder, filename)
        output_path = os.path.join(output_dir, output_filename)

        command = []

        if choice == "2": # Stretch
            command = ["gifsicle", optimization, "--resize", f"{target_w}x{target_h}", input_path, "-o", output_path]
        
        elif choice == "3": # Keep Ratio
            command = ["gifsicle", optimization, "--resize-fit", f"{target_w}x{target_h}", input_path, "-o", output_path]
            
        elif choice == "1": # Center and Crop
            orig_w, orig_h = get_gif_dimensions(input_path)
            if not orig_w or not orig_h:
                continue

            scale_ratio = max(target_w / orig_w, target_h / orig_h)
            new_w, new_h = round(orig_w * scale_ratio), round(orig_h * scale_ratio)
            off_x, off_y = (new_w - target_w) // 2, (new_h - target_h) // 2
            
            command = [
                "gifsicle", optimization,
                "--resize", f"{new_w}x{new_h}",
                "--crop", f"{target_w}x{target_h}+{off_x}+{off_y}",
                input_path, "-o", output_path
            ]

        try:
            subprocess.run(command, check=True)
            print(f" -> Saved to {folder_name}/{output_filename}")
        except subprocess.CalledProcessError:
            print(f" -> Error processing {filename}")

    print(f"\nFinished! All files are located in the '{folder_name}' folder.")

if __name__ == "__main__":
    process_gifs()
