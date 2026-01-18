import os
import json
import numpy as np

# --- CONFIG ---
NEST_PATH = "nest_data"
REFLEX_SOURCE = os.path.join(NEST_PATH, "genesis_reaction_standard.txt")
EMOTION_SOURCE = os.path.join(NEST_PATH, "genesis_emotion_standard.txt")

REFLEX_OUT = os.path.join(NEST_PATH, "reflex_storage")
EMOTION_OUT = os.path.join(NEST_PATH, "emotion_storage")

QUIT_DIMENSION = 1024

os.makedirs(REFLEX_OUT, exist_ok=True)
os.makedirs(EMOTION_OUT, exist_ok=True)

def binary_string_to_bytes(binary_line):
    clean_line = binary_line.split("#")[0].strip()
    parts = clean_line.split()
    if len(parts) != 7: return None
    return [int(p, 2) for p in parts]

def generate_hologram(byte_values, salt):
    """
    Generates the Waveform. 
    Salt is added to distinguish an Emotion from a Reflex even if bytes are similar.
    """
    seed = sum(byte_values) * salt
    rng = np.random.default_rng(seed)
    phases = rng.integers(0, 4, QUIT_DIMENSION) * (np.pi / 2)
    return np.exp(1j * phases)

def compile_file(source_path, output_path, type_label):
    print(f"--- COMPILING {type_label} ---")
    if not os.path.exists(source_path):
        print(f"Skipping {type_label}: Source file not found.")
        return

    with open(source_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("GENESIS") or line.startswith("=") or line.startswith("FORMAT") or line.startswith("#"):
            continue

        byte_values = binary_string_to_bytes(line)
        if not byte_values: continue
            
        description = line.split("#")[1].strip() if "#" in line else "Unknown"

        # 1. Generate Hologram (Reflexes use salt 1, Emotions use salt 2)
        salt = 1 if type_label == "REFLEX" else 2
        wave = generate_hologram(byte_values, salt)
        
        # 2. Save Hologram
        id_prefix = "R" if type_label == "REFLEX" else "E"
        item_id = f"{id_prefix}{byte_values[0]:03d}"
        
        save_path = os.path.join(output_path, f"{item_id}.npy")
        np.save(save_path, wave)
        
        # 3. Save Definition (Context Aware)
        meta_data = {
            "id": item_id,
            "description": description,
            "raw_bytes": byte_values
        }

        # Apply specific labeling based on type
        if type_label == "REFLEX":
            meta_data["hardware_target"] = byte_values[1]
            meta_data["initial_strength"] = byte_values[2]
            meta_data["direction"] = byte_values[3]
        elif type_label == "EMOTION":
            meta_data["focus_layer"] = byte_values[1]
            meta_data["valence"] = byte_values[2]
            meta_data["arousal"] = byte_values[3]
        
        # Both share the Flow Envelope (Last 3 bytes)
        meta_data["quit_flow"] = [byte_values[4], byte_values[5], byte_values[6]]

        # Save JSON
        json_path = save_path.replace(".npy", ".meta.json")
        with open(json_path, 'w') as f:
            json.dump(meta_data, f, indent=4)
            
        print(f"   [+] Compiled {item_id}: {description}")

if __name__ == "__main__":
    compile_file(REFLEX_SOURCE, REFLEX_OUT, "REFLEX")
    print()
    compile_file(EMOTION_SOURCE, EMOTION_OUT, "EMOTION")
    print("\n--- COMPILATION COMPLETE ---")