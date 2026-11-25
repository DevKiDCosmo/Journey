import sys

# ==============================================================================
# 1. STRICT SLOT ORDER & VERB AGGLUTINATION DICTIONARY
# ==============================================================================
SLOT_ORDER = [
    "voice",
    "concreteness",
    "existence",
    "entropy",
    "aktionsart",
    "aspect",
    "negation",
    "mood",
    "evidential_cmd",
    "decay",
]

VERB_DICTIONARY = {
    "voice": {
        "act":       {"char": "發", "name": "Active",            "usage": "Intentional action from 源 (default/zero-marked in everyday)"},
        "pass":      {"char": "受", "name": "Passive",           "usage": "Action received/undergone by subject"},
        "env":       {"char": "然", "name": "Environmental",     "usage": "Spontaneous/ambient event in 境 or via 媒"},
        "caus":      {"char": "使", "name": "Causative",         "usage": "Agent causes another (與) to perform action"},
        "perm":      {"char": "許", "name": "Permissive",        "usage": "Agent allows another to perform action"},
        "caus_pass": {"char": "使受", "name": "Causative-Passive", "usage": "Being forced/made to perform action"},
    },
    "concreteness": {
        "conc":      {"char": "形", "name": "Concrete",          "usage": "Physical world / tangible action"},
        "abs":       {"char": "念", "name": "Abstract",          "usage": "Mental, metaphorical, or conceptual action"},
    },
    "existence": {
        "create":    {"char": "生", "name": "Creation",          "usage": "Brings something new into existence"},
        "state":     {"char": "在", "name": "State",             "usage": "Maintains/interacts with existing state (default/zero-marked)"},
        "cease":     {"char": "滅", "name": "Cessation",         "usage": "Removes, erases, or destroys out of existence"},
    },
    "entropy": {
        "rev":       {"char": "還", "name": "Reversible",        "usage": "Resulting state can be undone/restored"},
        "irrev":     {"char": "斷", "name": "Irreversible",      "usage": "Resulting state is permanent/entropic"},
    },
    "aktionsart": {
        "inch":      {"char": "始", "name": "Inchoative",        "usage": "Sudden onset / entry into action"},
        "delim":     {"char": "暫", "name": "Delimitative",      "usage": "Performed for a brief, bounded span"},
        "semelf":    {"char": "閃", "name": "Semelfactive",      "usage": "Single, instantaneous burst (implies 終 in compact)"},
        "iter":      {"char": "復", "name": "Iterative",         "usage": "Repeated/habitual over time (implies 流 in compact)"},
        "perdur":    {"char": "續", "name": "Perdurative",       "usage": "Sustained continuously across a span (implies 流 in compact)"},
        "exhaust":   {"char": "盡", "name": "Exhaustive",        "usage": "Driven to absolute limit (implies 終 in compact)"},
    },
    "aspect": {
        "ipfv":      {"char": "流", "name": "Imperfective",      "usage": "Ongoing, open, unbounded process"},
        "pfv":       {"char": "終", "name": "Perfective",        "usage": "Single, bounded, completed whole"},
    },
    "negation": {
        "neg":       {"char": "不", "name": "Negation",          "usage": "Negates the verbal complex"},
    },
    "mood": {
        "real":      {"char": "實", "name": "Indicative",        "usage": "Factual reality (default/zero-marked in everyday)"},
        "subj":      {"char": "假", "name": "Subjunctive",       "usage": "Hypothetical / counterfactual"},
        "opt":       {"char": "願", "name": "Optative",          "usage": "Wish or blessing ('May X happen!')"},
        "cohort":    {"char": "偕", "name": "Cohortative",       "usage": "First-person plural urging ('Let us X!')"},
        "dub":       {"char": "恐", "name": "Dubitative",        "usage": "Epistemic doubt ('might / perhaps')"},
        "pot":       {"char": "能", "name": "Potential",         "usage": "Ability / possibility ('can')"},
        "vol":       {"char": "欲", "name": "Volitional",        "usage": "Personal desire / intention ('want to')"},
    },
    "evidential_cmd": {
        "vis":       {"char": "見", "name": "Direct Visual",     "usage": "Witnessed firsthand with eyes"},
        "sens":      {"char": "感", "name": "Direct Non-Visual", "usage": "Perceived via hearing, touch, smell, etc."},
        "hear":      {"char": "聞", "name": "Hearsay",           "usage": "Learned secondhand ('allegedly')"},
        "infer":     {"char": "推", "name": "Inferential",       "usage": "Deduced from evidence ('must have')"},
        "know":      {"char": "知", "name": "Assumptive",        "usage": "General knowledge / established fact"},
        "mir":       {"char": "驚", "name": "Mirative",          "usage": "Sudden/surprising discovery ('Oh, it turns out...')"},
        "imp":       {"char": "命", "name": "Imperative",        "usage": "Direct command"},
    },
    "decay": {
        "trans":     {"char": "露", "name": "Transient Truth",   "usage": "True only at this fleeting moment"},
        "decay":     {"char": "朽", "name": "Decaying Truth",    "usage": "True now, but actively becoming obsolete"},
        "invar":     {"char": "恆", "name": "Invariant Truth",   "usage": "Timeless, mathematical, or structural truth"},
    },
}

# ==============================================================================
# 2. PORTMANTEAU (FUSED) COMBINATIONS DICTIONARY
# ==============================================================================
PORTMANTEAU_DICTIONARY = [
    {"pattern": "為然念在流不", "fused": "非", "meaning": "Negative Copula ('is not')"},
    {"pattern": "為然念流不",   "fused": "非", "meaning": "Negative Copula ('is not', zero-marked 在)"},
    {"pattern": "然形生",       "fused": "化", "meaning": "Naturally manifests / physically comes into being"},
    {"pattern": "然形滅",       "fused": "亡", "meaning": "Naturally perishes / fades out of existence"},
    {"pattern": "不命",         "fused": "勿", "meaning": "Prohibitive ('Do not X!')"},
    {"pattern": "終不",         "fused": "未", "meaning": "Has not yet / did not complete"},
    {"pattern": "流不",         "fused": "弗", "meaning": "Does not / is not currently"},
    {"pattern": "不能",         "fused": "莫", "meaning": "Cannot / unable to"},
    {"pattern": "能不",         "fused": "莫", "meaning": "Cannot / unable to"},
    {"pattern": "不欲",         "fused": "厭", "meaning": "Does not want to / refuses to"},
    {"pattern": "欲不",         "fused": "厭", "meaning": "Does not want to / refuses to"},
]

# Build reverse lookup: tag -> slot_name
TAG_TO_SLOT = {
    tag: slot
    for slot, entries in VERB_DICTIONARY.items()
    for tag in entries
}


# ==============================================================================
# 3. POSITION-STRICT VERB IME ENGINE
# ==============================================================================
class SinoVerbIME:
    def __init__(self):
        self.register = "formal"  # formal | everyday | compact

    def validate_and_map(self, tags: list[str]) -> dict[str, str]:
        """
        Strictly enforces slot order. Raises ValueError if a tag is unknown,
        duplicated in the same slot, or placed out of positional order.
        """
        slots = {}
        last_slot_idx = -1

        for tag in tags:
            if tag not in TAG_TO_SLOT:
                raise ValueError(f"Unknown tag: '{tag}'. Type 'dict' to view valid tags.")

            slot = TAG_TO_SLOT[tag]
            slot_idx = SLOT_ORDER.index(slot)

            if slot_idx == last_slot_idx:
                raise ValueError(
                    f"Slot conflict: '{tag}' belongs to [{slot}], which is already filled by '{slots[slot]}'."
                )
            if slot_idx < last_slot_idx:
                prev_slot = SLOT_ORDER[last_slot_idx]
                raise ValueError(
                    f"Positional error: '{tag}' ([{slot}], pos {slot_idx + 1}) cannot come after "
                    f"[{prev_slot}] (pos {last_slot_idx + 1}). Strict order required."
                )

            slots[slot] = tag
            last_slot_idx = slot_idx

        return slots

    def build_verb(self, root: str, tags: list[str], register: str | None = None) -> str:
        reg = register or self.register
        slots = self.validate_and_map(tags)

        # Convert tags to characters in strict slot order
        chars = {slot: VERB_DICTIONARY[slot][tag]["char"] for slot, tag in slots.items()}

        # --- REGISTER 1: FORMAL / POETIC (Full explicit chain) ---
        if reg == "formal":
            return root + "".join(chars[s] for s in SLOT_ORDER if s in chars)

        # --- REGISTER 2 & 3: EVERYDAY / COMPACT (Zero-mark defaults) ---
        # Special case: check full negative copula before stripping 在
        full_str = root + "".join(chars[s] for s in SLOT_ORDER if s in chars)
        if reg == "compact" and full_str.startswith("為然念在流不"):
            remainder = full_str[len("為然念在流不"):]
            return "非" + remainder

        # Drop everyday defaults: 發 (act), 在 (state), 實 (real)
        if chars.get("voice") == "發":
            del chars["voice"]
        if chars.get("existence") == "在":
            del chars["existence"]
        if chars.get("mood") == "實":
            del chars["mood"]

        # Everyday register: only fuse 不+命 -> 勿
        if reg == "everyday":
            result = root + "".join(chars[s] for s in SLOT_ORDER if s in chars)
            return result.replace("不命", "勿")

        # --- REGISTER 3: COMPACT (Default Aspect + Portmanteau Fusions) ---
        if reg == "compact":
            # Default Aspect on Aktionsart
            akt = chars.get("aktionsart")
            asp = chars.get("aspect")
            if akt in ("閃", "盡") and asp == "終":
                del chars["aspect"]
            elif akt in ("續", "復") and asp == "流":
                del chars["aspect"]

            result = root + "".join(chars[s] for s in SLOT_ORDER if s in chars)

            # Apply portmanteau fusions in priority order
            for rule in PORTMANTEAU_DICTIONARY:
                result = result.replace(rule["pattern"], rule["fused"])

            return result

        raise ValueError(f"Unknown register: {reg}")


# ==============================================================================
# 4. INTERACTIVE CLI (INPUT / OUTPUT)
# ==============================================================================
def print_dictionary():
    print("\n=== VERB AGGLUTINATION DICTIONARY (STRICT SLOT ORDER) ===")
    for idx, slot in enumerate(SLOT_ORDER, 1):
        print(f"\n[{idx}. {slot.upper()}]")
        for tag, info in VERB_DICTIONARY[slot].items():
            print(f"  {tag:<10} -> {info['char']:<2} ({info['name']}): {info['usage']}")
    print("\n=== PORTMANTEAU FUSIONS (COMPACT REGISTER) ===")
    for rule in PORTMANTEAU_DICTIONARY:
        print(f"  {rule['pattern']:<8} -> {rule['fused']}  ({rule['meaning']})")
    print()


def main():
    ime = SinoVerbIME()
    print("=== Extended Sino-Character Verb IME ===")
    print("Commands: 'reg <formal|everyday|compact>' | 'dict' | 'quit'")
    print("Input format: <Root> <tag1> <tag2> ... (strict slot order!)")
    print("Example:      解 act abs cease semelf pfv pot\n")

    while True:
        try:
            raw = input(f"[{ime.register}] > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not raw:
            continue
        if raw.lower() in ("quit", "exit", "q"):
            break
        if raw.lower() == "dict":
            print_dictionary()
            continue
        if raw.lower().startswith("reg "):
            new_reg = raw.split()[1].lower()
            if new_reg in ("formal", "everyday", "compact"):
                ime.register = new_reg
                print(f"Register switched to: {ime.register}")
            else:
                print("Valid registers: formal, everyday, compact")
            continue

        parts = raw.split()
        root, tags = parts[0], parts[1:]

        try:
            output = ime.build_verb(root, tags)
            print(f"  => {output}")
        except ValueError as e:
            print(f"  [ERROR] {e}")


if __name__ == "__main__":
    main()