import os
import json
import numpy as np

# --- CONFIG ---
NEST_PATH = "nest_data"
# Using your existing file names
REFLEX_SOURCE = os.path.join(NEST_PATH, "GENESIS_REACTION_STANDARD.txt")
EMOTION_SOURCE = os.path.join(NEST_PATH, "GENESIS_EMOTION_STANDARD.txt")
THOUGHT_SOURCE = os.path.join(NEST_PATH, "GENESIS_THOUGHT_STANDARD.txt")

REFLEX_OUT = os.path.join(NEST_PATH, "reflex_storage")
EMOTION_OUT = os.path.join(NEST_PATH, "emotion_storage")
THOUGHT_OUT = os.path.join(NEST_PATH, "thought_storage")

QUIT_DIMENSION = 1024

os.makedirs(REFLEX_OUT, exist_ok=True)
os.makedirs(EMOTION_OUT, exist_ok=True)
os.makedirs(THOUGHT_OUT, exist_ok=True)

def binary_string_to_bytes(binary_line):
    clean_line = binary_line.split("#")[0].strip()
    parts = clean_line.split()
    if len(parts) != 7: return None
    return [int(p, 2) for p in parts]

def generate_hologram(byte_values, salt):
    """
    Generates the Waveform. 
    Salt distinguishes Reflex (1), Emotion (2), Thought (3), Sense (4), Spirit (5).
    """
    seed = sum(byte_values) * salt
    rng = np.random.default_rng(seed)
    # Using Complex Phasors (e^i*theta) for true Holographic property
    phases = rng.uniform(0, 2 * np.pi, QUIT_DIMENSION) 
    return np.exp(1j * phases)

def compile_file(source_path, output_path, type_label):
    print(f"--- COMPILING {type_label} ---")
    if not os.path.exists(source_path):
        print(f"Skipping {type_label}: Source file not found at {source_path}")
        return

    with open(source_path, 'r') as f:
        lines = f.readlines()

    count = 0
    for line in lines:
        line = line.strip()
        if not line or line.startswith("GENESIS") or line.startswith("=") or line.startswith("FORMAT") or line.startswith("#"):
            continue

        byte_values = binary_string_to_bytes(line)
        if not byte_values: continue
            
        description = line.split("#")[1].strip() if "#" in line else "Unknown"

        # --- DYNAMIC SALT & TYPE LOGIC ---
        salt = 1
        prefix = "X"
        
        # 1. Base Type assignment
        if type_label == "REFLEX": 
            salt = 1
            prefix = "R"
        elif type_label == "EMOTION": 
            salt = 2
            prefix = "E"
        elif type_label == "THOUGHT": 
            # Check for Special Groups inside the Thought File
            group_id = byte_values[1]
            
            if group_id == 9: # SOMA (Body/Senses)
                salt = 4
                prefix = "S" # Sense
            elif group_id == 10: # PNEUMA (Spirit/ESP)
                salt = 5
                prefix = "P" # Pneuma
            else: # Standard Thought
                salt = 3
                prefix = "T"
            
        # 2. Generate Hologram
        wave = generate_hologram(byte_values, salt)
        
        # 3. Save Hologram
        # We use prefix+UUID for the filename (e.g., P040.npy)
        item_id = f"{prefix}{byte_values[0]:03d}"
        save_path = os.path.join(output_path, f"{item_id}.npy")
        np.save(save_path, wave)
        
        # 4. Construct Metadata
        meta_data = {
            "id": item_id,
            "uuid": byte_values[0],
            "description": description,
            "raw_bytes": byte_values,
            "flow_pattern": [byte_values[4], byte_values[5], byte_values[6]]
        }

        # --- CONTEXT SPECIFIC FIELDS ---
        if type_label == "REFLEX":
            meta_data["category"] = "HARDWARE_REACTION"
            meta_data["target_hardware"] = byte_values[1] 
            meta_data["force_intensity"] = byte_values[2]
            
        elif type_label == "EMOTION":
            meta_data["category"] = "CHEMICAL_STATE"
            meta_data["focus"] = byte_values[1]
            meta_data["valence"] = byte_values[2]
            
        elif type_label == "THOUGHT":
            group_id = byte_values[1]
            
            # BRANCH 1: SOMA (Senses)
            if group_id == 9:
                meta_data["category"] = "SOMA_SENSOR"
                meta_data["physics"] = "ENCAPSULATION" # Wrapper Logic
                meta_data["io_port"] = "INPUT_STREAM"
                
            # BRANCH 2: PNEUMA (ESP)
            elif group_id == 10:
                meta_data["category"] = "PNEUMA_MODE"
                meta_data["physics"] = "INJECTION"     # Truth Logic
                meta_data["validation"] = "QI_RESONANCE"
                
            # BRANCH 3: STANDARD LOGIC
            else:
                meta_data["category"] = "THOUGHT_PRIMITIVE"
                meta_data["physics"] = "SUPERPOSITION" # Mixing Logic
                meta_data["class"] = byte_values[1]
                meta_data["op_code"] = byte_values[2]

        # Save JSON
        json_path = save_path.replace(".npy", ".meta.json")
        with open(json_path, 'w') as f:
            json.dump(meta_data, f, indent=4)
            
        print(f"   [+] Compiled {item_id}: {description} [{meta_data['category']}]")
        count += 1
    print(f"   >>> Total {count} items compiled for {type_label}.")

if __name__ == "__main__":
    print("INITIALIZING GENESIS COMPILER v2.0...")
    compile_file(REFLEX_SOURCE, REFLEX_OUT, "REFLEX")
    print()
    compile_file(EMOTION_SOURCE, EMOTION_OUT, "EMOTION")
    print()
    compile_file(THOUGHT_SOURCE, THOUGHT_OUT, "THOUGHT")
    print("\n--- NEST ARCHITECTURE BUILT ---")