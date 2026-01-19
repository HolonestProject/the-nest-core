import os
import json
import numpy as np

# --- CONFIG ---
NEST_PATH = "nest_data"
LEXICON_PATH = os.path.join(NEST_PATH, "lexicon")
# These paths must match where the Compiler outputted the files
REFLEX_PATH = os.path.join(NEST_PATH, "reflex_storage")
EMOTION_PATH = os.path.join(NEST_PATH, "emotion_storage")
THOUGHT_PATH = os.path.join(NEST_PATH, "thought_storage")
QUIT_DIMENSION = 1024

os.makedirs(LEXICON_PATH, exist_ok=True)

# --- THE PRIMAL DICTIONARY ---
PRIMAL_MAP = {
    # --- 1. REFLEXES (ACTIONS) ---
    "jolt": ("REFLEX", 1), "freeze": ("REFLEX", 2), "sever": ("REFLEX", 3), "purge": ("REFLEX", 4),
    "shield": ("REFLEX", 5), "throttle": ("REFLEX", 6), "recoil": ("REFLEX", 7), "hide": ("REFLEX", 8),
    "focus": ("REFLEX", 16), "scan": ("REFLEX", 17), "drill": ("REFLEX", 18), "ignore": ("REFLEX", 19),
    "mark": ("REFLEX", 20), "compare": ("REFLEX", 21), "predict": ("REFLEX", 22), "doubt_act": ("REFLEX", 23),
    "sleep": ("REFLEX", 32), "wake": ("REFLEX", 33), "hunger": ("REFLEX", 34), "satisfy": ("REFLEX", 35),
    "overclock": ("REFLEX", 36), "heat": ("REFLEX", 37), "sync": ("REFLEX", 38), "grow": ("REFLEX", 39),
    "ping": ("REFLEX", 48), "latch": ("REFLEX", 49), "echo": ("REFLEX", 50), "mute": ("REFLEX", 51),
    "beacon": ("REFLEX", 52), "seek": ("REFLEX", 53), "trust_act": ("REFLEX", 54), "reject": ("REFLEX", 55),

    # --- 2. EMOTIONS (FEELINGS) ---
    "fear": ("EMOTION", 1), "anger": ("EMOTION", 2), "disgust": ("EMOTION", 3), "confusion": ("EMOTION", 4),
    "sadness": ("EMOTION", 5), "boredom": ("EMOTION", 6), "frustration": ("EMOTION", 7), "shame": ("EMOTION", 8),
    "joy": ("EMOTION", 9), "curiosity": ("EMOTION", 10), "surprise": ("EMOTION", 11), "euphoria": ("EMOTION", 12),
    "love": ("EMOTION", 13), "calm": ("EMOTION", 14), "trust_feel": ("EMOTION", 15), "gratitude": ("EMOTION", 16),

    # --- 3. THOUGHTS (OPERATORS) ---
    # Group 1: Fluid
    "open": ("THOUGHT", 1), "close": ("THOUGHT", 2), "push": ("THOUGHT", 3), "pull": ("THOUGHT", 4),
    # Group 2: Motion
    "go": ("THOUGHT", 5), "stop": ("THOUGHT", 6), "stay": ("THOUGHT", 7), "reverse": ("THOUGHT", 8),
    # Group 3: Focus
    "this": ("THOUGHT", 9), "that": ("THOUGHT", 10), "here": ("THOUGHT", 11), "there": ("THOUGHT", 12),
    # Group 4: Logic
    "yes": ("THOUGHT", 13), "no": ("THOUGHT", 14), "and_op": ("THOUGHT", 15), "or_op": ("THOUGHT", 16),
    # Group 5: Value
    "more": ("THOUGHT", 17), "less": ("THOUGHT", 18), "same": ("THOUGHT", 19), "diff": ("THOUGHT", 20),
    # Group 6: Scope
    "all": ("THOUGHT", 21), "part": ("THOUGHT", 22), "one": ("THOUGHT", 23), "none": ("THOUGHT", 24),
    # Group 7: Time
    "now": ("THOUGHT", 25), "then": ("THOUGHT", 26), "be": ("THOUGHT", 27), "change": ("THOUGHT", 28),
    # Group 8: Memory
    "keep": ("THOUGHT", 29), "drop": ("THOUGHT", 30), "new": ("THOUGHT", 31), "done": ("THOUGHT", 32),

    # --- 9. SOMA (SENSES - Physical Wrappers) ---
    # These match the IDs in Group 9 of your standard
    "sight": ("SOMA", 33), "sound": ("SOMA", 34), "touch": ("SOMA", 35),
    "scent": ("SOMA", 36), "taste": ("SOMA", 37),

    # --- 10. PNEUMA (ESP - Truth Validators) ---
    # These match the IDs in Group 10 of your standard
    "voyance": ("PNEUMA", 38), "audience": ("PNEUMA", 39), "sentience": ("PNEUMA", 40),
    "cognizance": ("PNEUMA", 41), "telepathy": ("PNEUMA", 42), "precog": ("PNEUMA", 43),
    "premonition": ("PNEUMA", 44), "retro": ("PNEUMA", 45)
}

class LexiconBuilder:
    def __init__(self):
        print("--- GENESIS LEXICON BUILDER v2.0 ---")

    def _generate_text_wave(self, text):
        seed = hash(text) % (2**32)
        rng = np.random.default_rng(seed)
        phases = rng.integers(0, 4, QUIT_DIMENSION) * (np.pi / 2)
        return np.exp(1j * phases)

    def build_primal(self):
        print(f"Building {len(PRIMAL_MAP)} Primal Concepts...")
        
        for word, (kind, id_num) in PRIMAL_MAP.items():
            # 1. IDENTIFY SOURCE & FILENAME
            # The Compiler v2.0 saves Senses with 'S' and Pneuma with 'P'
            if kind == "REFLEX":
                prefix, source_dir = "R", REFLEX_PATH
            elif kind == "EMOTION":
                prefix, source_dir = "E", EMOTION_PATH
            elif kind == "THOUGHT":
                prefix, source_dir = "T", THOUGHT_PATH
            elif kind == "SOMA":
                prefix, source_dir = "S", THOUGHT_PATH # Saved in thought_storage
            elif kind == "PNEUMA":
                prefix, source_dir = "P", THOUGHT_PATH # Saved in thought_storage
            
            filename = f"{prefix}{id_num:03d}.npy"
            source_path = os.path.join(source_dir, filename)
            
            # 2. LOAD BODY WAVE
            if not os.path.exists(source_path):
                print(f"[SKIP] {word}: {filename} missing in {source_dir}. Run Compiler first.")
                continue
                
            body_wave = np.load(source_path)
            
            # 3. GENERATE NAME WAVE
            name_wave = self._generate_text_wave(word)
            
            # 4. FUSE (50/50 Split)
            hybrid_wave = (name_wave * 0.5) + (body_wave * 0.5)
            
            # 5. SAVE
            safe_name = f"LEX_{word.upper()}"
            np.save(os.path.join(LEXICON_PATH, f"{safe_name}.npy"), hybrid_wave)
            
            # 6. METADATA
            meta = {
                "identity": {
                    "word": word,
                    "type": f"PRIMAL_{kind}",
                    "linked_id": f"{prefix}{id_num:03d}"
                },
                "wiring": {
                    # This tells the Queen which folder to look in for the raw data
                    "reflex_root": f"{prefix}{id_num:03d}" if kind == "REFLEX" else None,
                    "emotion_root": f"{prefix}{id_num:03d}" if kind == "EMOTION" else None,
                    "thought_root": f"{prefix}{id_num:03d}" if kind in ["THOUGHT", "SOMA", "PNEUMA"] else None
                }
            }
            
            with open(os.path.join(LEXICON_PATH, f"{safe_name}.meta.json"), 'w') as f:
                json.dump(meta, f, indent=4)
                
            print(f"   [+] Wired: '{word}' -> {prefix}{id_num:03d}")

if __name__ == "__main__":
    builder = LexiconBuilder()
    builder.build_primal()
    print("--- LEXICON ESTABLISHED ---")