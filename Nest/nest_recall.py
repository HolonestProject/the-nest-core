import os
import json
import numpy as np
from datetime import datetime

# --- CONFIG ---
NEST_PATH = "nest_data"
MEMORY_PATH = os.path.join(NEST_PATH, "memory_bank")
QUIT_DIMENSION = 1024

class GenesisRecall:
    def __init__(self):
        print(f"[{datetime.now()}] RECALL SYSTEM: Online.")
        print(f"[{datetime.now()}] SEARCH MODE: Holographic Resonance")
        
        self.memories = []
        self._load_all_memories()

    def _generate_vector(self, text):
        """
        MUST match the Encoder in nest_metabolism.py exactly.
        If the hash doesn't match, the resonance will be 0.
        """
        seed = hash(text) % (2**32)
        rng = np.random.default_rng(seed)
        dna_bases = rng.integers(0, 4, QUIT_DIMENSION)
        phases = dna_bases * (np.pi / 2)
        return np.exp(1j * phases)

    def _load_all_memories(self):
        """
         recursively scans nest_data/memory_bank/YYYY-MM-DD/ for crystals.
        """
        if not os.path.exists(MEMORY_PATH):
            print("WARNING: Memory Bank empty. Run nest_metabolism.py first.")
            return

        print("Scanning Temporal Lobe (Memory Bank)...")
        count = 0
        
        # Walk through all date folders
        for root, dirs, files in os.walk(MEMORY_PATH):
            for file in files:
                if file.endswith(".npy"):
                    full_path = os.path.join(root, file)
                    meta_path = full_path.replace(".npy", ".meta.json")
                    
                    # Load Wave
                    wave = np.load(full_path)
                    
                    # Load Meta
                    try:
                        with open(meta_path, 'r') as f:
                            meta = json.load(f)
                    except:
                        meta = {"state_snapshot": {"content_summary": "CORRUPTED"}}

                    self.memories.append({
                        "id": file,
                        "wave": wave,
                        "meta": meta
                    })
                    count += 1
        
        print(f"System loaded {count} holographic memories.")

    def search(self, query_text, threshold=0.15):
        """
        THE RESONANCE ENGINE
        """
        print(f"\n--- SEARCHING FOR: '{query_text}' ---")
        
        # 1. Create the Query Hologram
        query_wave = self._generate_vector(query_text)
        
        results = []
        
        for mem in self.memories:
            # 2. Calculate Resonance (Dot Product)
            # The stored wave is a composite (Content + Emotion + Reflex).
            # The Query is just Content.
            # Because Content has the highest weight (1.0), it will dominate the dot product.
            raw_dot = np.vdot(query_wave, mem["wave"])
            resonance = np.abs(raw_dot) / QUIT_DIMENSION
            
            if resonance > threshold:
                results.append((resonance, mem))

        # 3. Sort by Strength
        results.sort(key=lambda x: x[0], reverse=True)

        # 4. Display Results
        if not results:
            print("No resonance found. The Queen does not recall this.")
            return

        print(f"Found {len(results)} matches:\n")
        
        for score, data in results[:3]: # Show top 3
            meta = data["meta"]
            snapshot = meta.get("state_snapshot", {})
            channel = meta.get("input_channel", "UNKNOWN")
            
            # DECODE THE EXPERIENCE TYPE
            type_tag = "[DATA]"
            if "SOMA" in channel:
                type_tag = "[BODY/SENSE]"
            elif "PNEUMA" in channel:
                type_tag = "[SPIRIT/ESP]"
            
            print(f"MATCH ({score:.2f}) | {type_tag}")
            print(f"   Date: {meta.get('readable_time', 'Unknown')}")
            print(f"   Content: \"{snapshot.get('content_summary')}\"")
            print(f"   Emotion: {snapshot.get('active_emotion')}")
            
            # If Pneuma, show the validation
            if meta.get("pneuma_signature"):
                print(f"   >>> PNEUMA SEAL VERIFIED (Direct Truth Injection)")
                
            # If Soma, show the file path
            if meta.get("soma_reference"):
                print(f"   >>> REF: {meta.get('soma_reference')}")
            
            print("-" * 30)

if __name__ == "__main__":
    recall = GenesisRecall()
    
    # INTERACTIVE LOOP
    while True:
        q = input("\nQuery the Nest (or 'q' to quit): ")
        if q.lower() == 'q': break
        recall.search(q)