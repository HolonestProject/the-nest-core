# The Nest: Holographic Phase-Space Memory Engine

> "Conventional AI records data in rows. The Nest records data in interference patterns."

## 1. The Core Philosophy
The Nest is a **Vector Symbolic Architecture (VSA)** library designed to solve the "Catastrophic Forgetting" problem in modern AI.

Instead of storing memories as text strings or static embeddings, The Nest uses **Quit Logic (Phase Space)**. It treats every piece of data—text, image, or emotion—as a complex phasor on the unit circle.

### Why Phase Space?
In binary logic ($1+1=2$), adding data increases size. In Phase Space ($1 \angle 0^\circ + 1 \angle 180^\circ = 0$), adding data creates **interference**. This allows for:
* **Infinite Superposition:** You can stack 1,000 memories into a single 1024-dimensional vector.
* **Destructive Interference:** Noise cancels itself out naturally.
* **Constructive Interference:** Repeated patterns (wisdom) amplify naturally.

## 2. The Physics Engine (`nest_holography.py`)
The core engine operates on **Complex128** arrays (1024 dimensions).

### The Math
Every concept is mapped to a vector $z$ where:
$$z = e^{i\theta}$$
*(Where $\theta$ is the phase angle 0, $\pi/2$, $\pi$, or $3\pi/2$)*.

### Operations
* **Binding (Multiplication):** $A \otimes B$. Used to attach attributes (e.g., "Color" attached to "Car").
* **Bundling (Addition):** $A + B$. Used to store multiple memories in one slot.
* **Resonance (Dot Product):** $|A \cdot B|$. Used to recall if a specific memory exists inside a bundle.

## 3. The Trinity Anchors (Initial Conditions)
To prevent the "Cold Start" problem where a blank system has no reference frame, The Nest is seeded with three immutable **Phase Anchors**. These are fixed vectors that serve as the system's "Instincts."

### A. Reflex (Survival Layer)
* **Definition:** Hard-coded phase patterns that represent system priority.
* **The "JOLT" Vector:** A high-frequency signal used to override normal processing. In a biological context, this is "Pain" or "Alert."

### B. Emotion (Valence Layer)
* **Definition:** A coordinate system mapping Valence (Good/Bad) and Arousal (High/Low) to phase angles.
* **Function:** Acts as "Gravity." High-Arousal events generate vectors with higher mass, ensuring they sink deeper into long-term storage (Concept Formation).

### C. Thought (Authentication Layer)
* **Definition:** Rotation keys used to tag the *source* of a memory.
* **SOMA Channel ($0^\circ$):** Represents empirical data (Sensors/Camera). "I saw this."
* **PNEUMA Channel ($90^\circ$):** Represents trusted axioms (User Truth). "I know this."
* **Logic:** By rotating the vector $90^\circ$, the system can distinguish between *seeing* a fire (Soma) and *knowing* fire is hot (Pneuma).

## 4. Storage & Retrieval Flow

### Crystallization (Write)
The `nest_metabolism.py` module handles the "Crystallization" of data.
1.  **Input:** Text or Image (32x32 pixel grid).
2.  **Transmutation:** Converted to Phase Vector.
3.  **Weighting:** Multiplied by its Emotional Mass (0.0 to 1.0).
4.  **Storage:** Saved as a `.npy` crystal in the requested directory.

### Resonance (Read)
The `nest_recall.py` module does not "search" text. It "vibrates" the memory bank.
1.  **Query:** Converted to Phase Vector.
2.  **Scan:** The query vector is dot-producted against every crystal in the bank.
3.  **Result:** Memories with a Resonance Score $> 0.15$ are returned.

## 5. System Topology
The Nest is strictly the **Mechanism**. It takes orders, it does not make decisions.

```mermaid
graph TD
    User[Client Logic] --> |"Save This"| Scribe[nest_metabolism.py]
    User --> |"Find This"| Mnemosyne[nest_recall.py]
    
    subgraph "The Nest Engine"
        Physics[nest_holography.py]
        Retina[nest_vision.py]
        Lexicon[Phase Lexicon]
    end
    
    Scribe --> Physics
    Mnemosyne --> Physics
    
    Physics --> |Phase Vector| Disk[(.npy Storage)]
    Retina --> |32x32 Phase Grid| Physics