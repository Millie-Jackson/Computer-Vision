import os
import shutil

# Define the desired structure
folders = [
    "data",
    "reports",
    "resources",
    "modules",
    "scripts"
]

# Mapping for files to move
file_locations = {
    "HandTrackingModule.py": "moduels",
    "PatternAnalysis.py": "scripts",
    "ReportGenerator.py": "scripts",
    "RockPaperScissors.py": "scripts",
    "FingerCounting.py": "scripts",
    "DataAnalysis.py": "scripts",
    "labels.txt": "resources",
    "game_moves.csv": "data"
}

def create_structure():
    
    print("\n Creating project folder structure...")
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"{folder}/")

    print("Organising files...")
    for file, target_folder in file_locations.items():
        if os.path.exists(file):
            target_path = os.path.join(target_folder, file)
            shutil.move(file, target_path)
            print(f"Moved {file} -> {target_path}")
        else:
            print(f"Skipped {file} (not found)")
    
    print("\n Project structure setup complete")



if __name__ == "__main__":

    create_structure()