import os
import json
import time
import numpy as np
from datetime import datetime

# --- QUIT CONSTANTS ---
# We use 1024 "Quits" (Base-4 Quantum Digits) per memory.
# This aligns perfectly with biological sequence length.
QUIT_DIMENSION = 1024 

class QuitNest:
    def __init__(self, nest_path="nest_data"):
        self.root_path = nest_path
        self.hot_path = os.path.join(nest_path, "hot_quits")
        
        os.makedirs(self.hot_path, exist_ok=True)
        
        print(f"[{datetime.now()}] QUIT-NEST: Online.")
        print(f"[{datetime.now()}] ARCHITECTURE: Base-4 Holographic (A/T/C/G)")

    def _text_to_quits(self, text):
        """
        THE GENETIC ENCODER:
        Converts text into 'Quits' (4 distinct quantum states).
        This mimics DNA strands.
        """
        # 1. Generate a deterministic seed from the text
        seed = hash(text) % (2**32)
        rng = np.random.default_rng(seed)
        
        # 2. Generate random integers 0, 1, 2, 3 (The 4 DNA bases)
        dna_bases = rng.integers(0, 4, QUIT_DIMENSION)
        
        # 3. Map these to Quantum Phases (0, 90, 180, 270 degrees)
        # 0 -> 0     (Right)
        # 1 -> pi/2  (Up)
        # 2 -> pi    (Left)
        # 3 -> 3pi/2 (Down)
        phases = dna_bases * (np.pi / 2)
        
        # 4. Create the Wave Function
        quit_vector = np.exp(1j * phases)
        
        return quit_vector

    def ingest(self, raw_data):
        """
        Phase 1: Ingestion.
        Encodes experience into a Quit-Stream.
        """
        timestamp = int(time.time())
        
        # Encode
        quit_wave = self._text_to_quits(raw_data["content"])
        
        # Weighting (Amplitude)
        amplitude = raw_data.get("weight", 1.0)
        weighted_wave = quit_wave * amplitude
        
        # Save as .npy
        filename = f"quit_{timestamp}.npy"
        file_path = os.path.join(self.hot_path, filename)
        np.save(file_path, weighted_wave)
        
        # Metadata
        meta_path = file_path.replace(".npy", ".meta.json")
        with open(meta_path, 'w') as f:
            json.dump(raw_data, f)
            
        print(f"[{datetime.now()}] NEST: Crystallized Memory -> {filename}")
        print(f"   L_ Structure: {QUIT_DIMENSION} Quits")

if __name__ == "__main__":
    nest = QuitNest()
    
    # Test Ingestion
    test_memory = {
        "content": "The Queen breathes in Base-4.",
        "weight": 10.0
    }
    nest.ingest(test_memory)