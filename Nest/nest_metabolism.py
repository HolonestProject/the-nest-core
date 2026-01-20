import os
import time
import json
import numpy as np
import nest_holography 

# --- CONFIG ---
DATA_DIR = os.path.expanduser("~/Genesis/nest_data")
REFLEX_DIR = os.path.join(DATA_DIR, "reflex_storage")
EMOTION_DIR = os.path.join(DATA_DIR, "emotion_storage")
LEXICON_DIR = os.path.join(DATA_DIR, "lexicon")

class GenesisMemoryJournal:
    def __init__(self):
        self.physics = nest_holography.HolographicEngine()
        self.lexicon_map = self._load_lexicon_map()

    def _load_lexicon_map(self):
        """
        Loads the map of 'WORD' -> 'FILE_ID' (e.g., 'JOY' -> 'E009')
        This allows us to look up the DNA vectors by name.
        """
        mapping = {}
        if not os.path.exists(LEXICON_DIR):
            return mapping

        # Scan the lexicon folder for .meta.json files
        for filename in os.listdir(LEXICON_DIR):
            if filename.endswith(".meta.json"):
                try:
                    with open(os.path.join(LEXICON_DIR, filename), 'r') as f:
                        meta = json.load(f)
                        word = meta['identity']['word']
                        linked_id = meta['identity']['linked_id'] # e.g., "E009"
                        mapping[word] = linked_id
                except:
                    continue
        return mapping

    def _get_anchor_vector(self, name, anchor_type):
        """
        Retrieves the 'DNA Vector' for a specific Emotion or Reflex.
        """
        # 1. Resolve Name to ID (e.g., "joy" -> "E009")
        name_key = name.lower()
        if name_key not in self.lexicon_map:
            # If unknown, return zero vector (no resonance)
            return np.zeros(1024, dtype=np.complex128)

        file_id = self.lexicon_map[name_key]
        
        # 2. Determine Source Folder
        if anchor_type == "EMOTION":
            path = os.path.join(EMOTION_DIR, f"{file_id}.npy")
        elif anchor_type == "REFLEX":
            path = os.path.join(REFLEX_DIR, f"{file_id}.npy")
        else:
            return np.zeros(1024, dtype=np.complex128)

        # 3. Load Vector
        if os.path.exists(path):
            return np.load(path)
        else:
            return np.zeros(1024, dtype=np.complex128)

    def crystallize(self, event_data, location):
        """
        The Act of Memorizing.
        Fuses Content + Emotion + Reflex into a single Phase Crystal.
        """
        timestamp = time.time()
        content = event_data.get("content", "")
        emotion_name = event_data.get("emotion", "CALM")
        reflex_name = event_data.get("reflex", "IGNORE")
        
        # 1. OBEDIENCE CHECK
        if not os.path.exists(location):
            try:
                os.makedirs(location)
            except OSError:
                return

        # --- THE TRINITY FUSION ---
        
        # A. CONTENT VECTOR (The "What")
        if "visual_vector" in event_data:
            # Resize visual data to fit Physics Dimension
            raw_vec = event_data["visual_vector"]
            target_dim = 1024
            if len(raw_vec) > target_dim:
                vec_content = raw_vec[:target_dim]
            else:
                vec_content = np.pad(raw_vec, (0, target_dim - len(raw_vec)))
        else:
            # Transmute Text
            vec_content = self.physics.text_to_hologram(content)

        # B. EMOTION ANCHOR (The "Heart")
        # We load the actual DNA vector for "JOY", not just a number.
        vec_emotion = self._get_anchor_vector(emotion_name, "EMOTION")
        
        # C. REFLEX ANCHOR (The "Instinct")
        # We load the actual DNA vector for "SCAN", "JOLT", etc.
        vec_reflex = self._get_anchor_vector(reflex_name, "REFLEX")

        # D. SUPERPOSITION (The Mixing)
        # Content is dominant (1.0). Anchors provide context (0.5).
        # In Quit Logic, adding vectors creates a new interference pattern.
        final_hologram = vec_content + (vec_emotion * 0.5) + (vec_reflex * 0.5)

        # --- MASS CALCULATION ---
        # We still need a scalar 'Mass' for sorting, but we can verify it against the vector magnitude if needed.
        # For now, we estimate based on the name (simplified for speed).
        # Ideally, we would read the Arousal from the metadata, but let's stick to the map for now.
        # (You can expand _load_lexicon_map to include Arousal later).
        mass = 0.5 # Default
        if "joy" in emotion_name.lower() or "fear" in emotion_name.lower(): mass = 0.9
        if "calm" in emotion_name.lower(): mass = 0.2

        # 4. CRYSTALLIZE
        crystal = {
            "hologram": final_hologram, # Contains the fused DNA
            "raw_content": content,
            "components": {
                "emotion": emotion_name,
                "reflex": reflex_name
            },
            "mass": mass,
            "timestamp": timestamp,
            "decay_factor": 1.0
        }

        # 5. STORE
        filename = f"{location}/mem_{timestamp}.npy"
        np.save(filename, crystal)
        print(f" >> [SCRIBE] Crystal Fused: {emotion_name} + {reflex_name} -> {os.path.basename(location)}")

    def metabolic_sleep(self, target_folder):
        pass