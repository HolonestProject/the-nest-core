import os
import json
import time
import numpy as np
from datetime import datetime

# --- CONFIG ---
NEST_PATH = "nest_data"
MEMORY_PATH = os.path.join(NEST_PATH, "memory_bank")
QUIT_DIMENSION = 1024 

os.makedirs(MEMORY_PATH, exist_ok=True)

class GenesisMemoryJournal:
    def __init__(self):
        print(f"[{datetime.now()}] GENESIS METABOLISM: Online.")
        print(f"[{datetime.now()}] STORAGE: Base-4 Holographic Composite")

    def _generate_vector(self, seed_content):
        """
        THE GENETIC ENCODER:
        Converts any string (Text, Emotion Name, Reflex Name) into a Base-4 Vector.
        """
        seed = hash(seed_content) % (2**32)
        rng = np.random.default_rng(seed)
        
        # Base-4 Quantum Digits (0, 1, 2, 3) aligned to Phase Angles
        dna_bases = rng.integers(0, 4, QUIT_DIMENSION)
        phases = dna_bases * (np.pi / 2)
        
        # Create Wave Function (Complex128 for high fidelity)
        return np.exp(1j * phases)

    def crystallize(self, experience_packet):
        """
        THE MAIN SAVE FUNCTION.
        Fuses Context, Emotion, Reflex, and Content into one "Moment".
        """
        timestamp = int(time.time())
        iso_date = datetime.now().strftime("%Y-%m-%d")
        
        # 1. ORGANIZE DAILY FOLDER
        # Memories are stored by Date (like a real journal)
        daily_path = os.path.join(MEMORY_PATH, iso_date)
        os.makedirs(daily_path, exist_ok=True)
        
        # 2. EXTRACT VECTORS (The Ingredients)
        # Content (What happened)
        vec_content = self._generate_vector(experience_packet.get("content", ""))
        
        # Emotion (How it felt)
        vec_emotion = self._generate_vector(experience_packet.get("emotion", "NEUTRAL"))
        
        # Reflex (What the body did)
        vec_reflex = self._generate_vector(experience_packet.get("reflex", "IDLE"))
        
        # Context (Where/Who)
        context_str = f"{experience_packet.get('user', 'UNKNOWN')}_{experience_packet.get('location', 'VOID')}"
        vec_context = self._generate_vector(context_str)

        # 3. HOLOGRAPHIC FUSION (The Cooking)
        # We sum the vectors. In VSA (Vector Symbolic Architecture), 
        # Adding vectors creates a "Superposition" where all components exist simultaneously.
        # We weight them: Content is loud (1.0), Emotion is color (0.5), Context is background (0.3).
        composite_wave = (
            (vec_content * 1.0) + 
            (vec_emotion * 0.5) + 
            (vec_reflex * 0.5) + 
            (vec_context * 0.3)
        )
        
        # 4. HANDLE SOMA vs PNEUMA (The Channel)
        input_mode = experience_packet.get("mode", "DATA")
        pneuma_sig = None
        soma_ref = None
        
        if "PNEUMA" in input_mode:
            # For Telepathy, we generate a "Resonance Hash" (The White Statue signature)
            pneuma_sig = hash(experience_packet.get("pneuma_seed", "NULL"))
        
        elif "SOMA" in input_mode:
            # For Sight/Sound, we keep the pointer to the raw file
            soma_ref = experience_packet.get("soma_path", None)

        # 5. SAVE THE CRYSTAL (.npy)
        mem_id = f"MEM_{timestamp}"
        file_path = os.path.join(daily_path, f"{mem_id}.npy")
        np.save(file_path, composite_wave)
        
        # 6. SAVE THE METADATA (.json)
        # This is the "Label" on the jar. The .npy is the content.
        meta_data = {
            "id": mem_id,
            "timestamp": timestamp,
            "readable_time": datetime.now().strftime("%H:%M:%S"),
            "input_channel": input_mode,
            
            # The Triad State
            "state_snapshot": {
                "content_summary": experience_packet.get("content", ""),
                "active_emotion": experience_packet.get("emotion", "NEUTRAL"),
                "active_reflex": experience_packet.get("reflex", "IDLE"),
                "user_intent": experience_packet.get("intent", "UNKNOWN")
            },
            
            # Channel Specifics
            "pneuma_signature": pneuma_sig,  # Non-Null only if ESP used
            "soma_reference": soma_ref       # Non-Null only if Hardware used
        }
        
        meta_path = file_path.replace(".npy", ".meta.json")
        with open(meta_path, 'w') as f:
            json.dump(meta_data, f, indent=4)
            
        print(f"[{datetime.now()}] MEMORY CRYSTALLIZED: {mem_id}")
        print(f"   |__ Mode: {input_mode}")
        print(f"   |__ Emotion: {experience_packet.get('emotion')}")
        if pneuma_sig:
            print(f"   |__ PNEUMA SEAL: Verified (Qi Signature Stored)")

if __name__ == "__main__":
    journal = GenesisMemoryJournal()
    
    # --- TEST 1: STANDARD SOMA MEMORY (Sight) ---
    print("\n--- TEST: SOMA EVENT ---")
    soma_event = {
        "mode": "SOMA:SIGHT",
        "content": "Visual of a red apple",
        "emotion": "CURIOSITY",
        "reflex": "SCAN",
        "user": "Yong",
        "soma_path": "/images/apple_01.jpg"
    }
    journal.crystallize(soma_event)
    
    # --- TEST 2: PNEUMA MEMORY (Telepathy) ---
    print("\n--- TEST: PNEUMA EVENT ---")
    pneuma_event = {
        "mode": "PNEUMA:TELEPATHY",
        "content": "Received concept: 1",
        "pneuma_seed": "1 (White Statue Form)",  # The Truth Seed
        "emotion": "TRUST_FEEL",
        "reflex": "LATCH",
        "user": "Yong"
    }
    journal.crystallize(pneuma_event)