import re

# 1. DATA STRUCTURES (from your provided lists)
PREFIXES = ["a-","ab-","ac-","ad-","af-","ag-","al-","am-","an-","ar-","as-","at-","pre-","e-","ec-","ef-","ex-","en-","em-","in-","il-","ir-","im-","it-","mis-","re-","pro-","per-","le-","lo-","la-","co-","com-","con-","cor-","col-","inter-","intro-","intra-","de-","di-","dis-","su-","sub-","suf-","sup-","bene-","beni-","male-","mali-","ultra-","ultro-","extra-","extro-","nulti-","mono-","bi-","hex-","sexto-","stereo-","hypo-","trans-","super-","supra-","uni-","tele-","contra-","op-","ob-","retro-","infro-","infra-","ferra-","ferro-","ligne-","agro-","ludo-","poly-","un-","multi-","semi-","mini-","homo-","primo-","prima-","san-","loco-","liqu-","tuss-","coch-","cuch-","coach-","se-","car-","os-","micro-","neo-","deo-","theo-","meta-","electro-","techno-","sin-","que-","deter-","exter-","exer-","aero-","air-","pseudo-","psycho-"]

AFFIXES = [ # As you defined them, distinct from prefixes in combination logic
    "ab-","ob-","sub-","suf-","sup-" # A representative sample based on your algo logic
]

LATINIZED_ORIGINS = ["-lect-","-port-","-part-","-pose-","-pede-","-dict-","-rect-","-cuss-","-lude-","-terr-","-terra-","-lor-","-tor-","-act-","-fact-","-luce-","-cargo-","-le-","-lo-","-la-","-qual-","-aviate-","-lax-","-claim-","-tend-","-tent-","-tens-","-cent-","-bay-","-maraca-","-fect-","-bail-","-sign-","-ami-","-amigo-","-verb-","-ver-","-vent-","-vest-","-vency-","-urban-","-bon-","-bien-","-mit-","-mune-","-mute-","-lune-","-oss-","-perr-","-prior-","-lob-","-cab-","-ovra-","-can-","-sist-","-gat-","-late-","-quire-","-quest-","-verse-","-vert-","-turn-","-tort-","-press-","-lace-","-lact-","-cur-","-cir-","-cor-","-cora-","-gene-","-mol-","-mil-","-aqua-","-sol-","-salt-","-salute-","-play-","-place-","-cere-","-alto-","-alt-","-alph-","-aure-","-ore-","-argent-","-origin-","-val-","-cap-","-test-","-tect-","-clear-","-bark-","-text-","-duo-","-trio-","-quad-","-quinto-","-sexto-","-septo-","-octo-","-nono-","-deco-","-cento-","-milo-","-vend-","-quay-","-quase-","-quare-","-quer-","-count-","-form-","-farm-","-firm-","-figure-","-amo-","-amor-","-amour-","-locate-","-qual-","-fuse-","-struct-","-plant-","-communicate-","-san-","-pict-","-lust-","-spade-","-liqu-","-duce-","-duct-","-car-","-par-","-cart-","-dar-","-dart-","-mar-","-mart-","-nar-","-sert-","-vern-","-ola-","-olla-","-scent-","-scence-","-sangu-","-tain-","-anim-","-cogn-","-bic-","-dic-","-fic-","-gic-","-lic-","-mic-","-nic-","-sanct-","-buc-","-duc-","-fuc-","-vac-","-vic-","-ama-","-vict-","-fix-","-chid-","-chil-","-dent-","-sent-","-calor-","-hiberne-","-luct-","-loct-","-lict-"]

SUFFIXES = {
    "noun_act": ["-ion", "-tion", "-sion", "-vion"],
    "noun_state": ["-tude", "-ality"],
    "adj": ["-al", "-ous", "-id", "-ive", "-mentary"],
    "adv": ["-ally", "-ously", "-culously"],
    "male_agent": ["-or", "-tor", "-dor", "-lor"],
    "female_agent": ["-ess", "-ness", "-ress", "-gess"],
    "neutral_agent": ["-ore", "-ue", "-gue", "-re"],
    "fem_non_human_agent": ["-rix"],
    "verb_simple": [ # Generic verb endings not in the massive list, or the -ate family
        "-ate", "-ates", "-ated", "-ating",
        "-ify", "-ifies", "-ified", "-ifying"
    ],
    "verb_special": [ # The large list of patterned verbs
        "-rate", "-gate", "-late", "-bate", "-cate", "-date", "-mate",
        "-nate", "-iate", "-pate", "-sate", "-tate", "-vate"
    ],
    "noun_diminutive": ["-ette"],
    "noun_other": ["-cle", "-geon"],
    "adj_derived": ["-cular", "-culous"]
}

# 2. PHASE 1 & 2: DECONSTRUCTION & VALIDATION (RECOGNITION)

def tokenize_and_tag(word):
    """Recognizes the morphological components of a valid neologism."""
    original_word = word
    
    # --- Step A: Strip known affixes (outermost layer) ---
    detected_affix = None
    for affix in sorted(AFFIXES, key=len, reverse=True):
        if word.startswith(affix):
            detected_affix = affix
            word = word[len(affix):]
            break
            
    # --- Step B: Strip known prefixes (middle layer) ---
    detected_prefix = None
    for prefix in sorted(PREFIXES, key=len, reverse=True):
        if word.startswith(prefix[:-1]): # Handle hyphenated prefix "pre-"
             temp_word = word[len(prefix)-1:]
        elif word.startswith(prefix):
            temp_word = word[len(prefix):]
        else:
            continue
            
        # Check if the remaining part starts with a known latinized origin
        for origin in LATINIZED_ORIGINS:
            # Clean origin of its leading dash for matching
            clean_origin = origin.replace("-", "")
            if temp_word.startswith(clean_origin):
                detected_prefix = prefix
                word = temp_word
                break
        if detected_prefix:
            break

    # If no prefix found by origin-check, check direct prefix stripping as fallback
    if not detected_prefix:
        for prefix in sorted(PREFIXES, key=len, reverse=True):
            if word.startswith(prefix):
                detected_prefix = prefix
                word = word[len(prefix):]
                break

    # --- Step C: Identify Latinized Origin and Suffix ---
    detected_origin = None
    detected_suffix = None
    pos_tag = None

    # Sort origins by length descending to match longest possible first
    for origin in sorted(LATINIZED_ORIGINS, key=len, reverse=True):
        clean_origin = origin.replace("-", "")
        if word.startswith(clean_origin):
            remaining = word[len(clean_origin):]
            
            # Now find the suffix in the remaining part
            for category, suffixes in SUFFIXES.items():
                for suffix in sorted(suffixes, key=len, reverse=True):
                    if remaining == suffix:
                        detected_origin = origin
                        detected_suffix = suffix
                        pos_tag = category
                        break
                if detected_suffix:
                    break
            
            # Handle verb conjugations (-ates, -ated, -ating) vs base (-ate)
            if not detected_suffix:
                for v_cat in ["verb_simple", "verb_special"]:
                    for suffix in sorted(SUFFIXES[v_cat], key=len, reverse=True):
                        if remaining == suffix or (suffix.endswith("e") and remaining == suffix + "s") or \
                           (suffix.endswith("e") and remaining == suffix + "d") or \
                           (suffix.endswith("y") and remaining == suffix[:-1] + "ies"):
                            # Simplified check for illustration
                            if remaining in SUFFIXES[v_cat]:
                                detected_origin = origin
                                detected_suffix = remaining
                                pos_tag = "verb"
                                break
                    if detected_suffix:
                        break
            break

    # --- Step D: Validate and Assemble the Parse ---
    if detected_origin and detected_suffix:
        # Reconstruct the base form
        base_form = detected_origin.replace("-", "") + detect_suffix_base(detected_suffix)
        
        return {
            "status": "recognized",
            "morphemes": {
                "affix": detected_affix,
                "prefix": detected_prefix,
                "latinized_origin": detected_origin,
                "suffix": detected_suffix
            },
            "base_form": base_form,
            "pos": pos_tag,
            "algorithm_path": f"{'[Affix] + ' if detected_affix else ''}{'[Prefix] + ' if detected_prefix else ''}[{detected_origin}] + [{detected_suffix}]"
        }
    else:
        return {"status": "unrecognized", "original": original_word}

def detect_suffix_base(suffix):
    """Strips conjugation endings to find the dictionary form."""
    if suffix.endswith("s"): return suffix[:-1]
    if suffix.endswith("ing"): return suffix[:-3]
    if suffix.endswith("ed"): return suffix[:-2] # or -1, depends on base
    if suffix.endswith("ies"): return suffix[:-3] + "y"
    return suffix

# 3. PHASE 3: CONSTRUCTION (GENERATION) FOLLOWING YOUR ALGORITHM

def generate_neologism(components):
    """
    Generates a neologism based on the provided algorithm path.
    components = {
        "origin_type": "latinized" | "iberian-romance",
        "origin": "-port-",
        "target_pos": "noun_act", # Key from SUFFIXES
        "prefix": None, # Optional
        "affix": None   # Optional
    }
    """
    origin = components["origin"].replace("-", "")
    
    # Select suffix based on target part of speech
    suffix_category = components["target_pos"]
    # Simple rule: pick the first suffix in the category, or implement more nuanced selection
    chosen_suffix = SUFFIXES[suffix_category][0] 
    
    # Build the core word
    core = origin + chosen_suffix
    
    # Apply prefix if present
    if components.get("prefix"):
        core = components["prefix"] + core
        
    # Apply affix if present
    if components.get("affix"):
        core = components["affix"] + core
        
    # --- Grammatical Generation (from your syntax rules) ---
    pronoun_subj = "Ego" # Placeholder for "I"
    pronoun_obj = "is"   # Placeholder for "him/her/it"
    indefinite_art = "un"
    noun_sing = "computer" # Use generated word? core + "um"?
    
    # Example sentence generation path 1:
    # Subjective pronounce + simplified regular verb + objective personal pronounce…
    sentence_1 = f"{pronoun_subj} {core}at {pronoun_obj}." # "-at" as simple present
    
    return {
        "neologism": core,
        "pos": suffix_category,
        "algorithm_path": f"[{components.get('affix', '')} + {components.get('prefix', '')} + {origin} + {chosen_suffix}]",
        "sample_sentence": sentence_1
    }

# 4. DEMONSTRATION

print("=== MACHINE RECOGNITION ===")
test_words = [
    "importation",   # im- + -port- + -ation -> noun_act
    "reporter",      # re- + -port- + -er (male agent via -or)
    "subvention",    # sub- (affix) + -vent- + -ion
    "contraversion", # contra- + -vers- + -ion
    "benediction",   # bene- + -dict- + -ion
    "transparency",  # trans- + -par- + -ency (-vency origin)
    "biodictatory"   # bio- (not in list) + -dict- + -atory (not in list) -> unrecognized
]

for word in test_words:
    result = tokenize_and_tag(word)
    if result["status"] == "recognized":
        print(f"✓ '{word}': {result['algorithm_path']} -> {result['base_form']} ({result['pos']})")
    else:
        print(f"✗ '{word}': UNRECOGNIZED")

print("\n=== NEOLOGISM GENERATION ===")
new_coin = generate_neologism({
    "origin_type": "latinized",
    "origin": "-luce-",
    "target_pos": "adj",
    "prefix": "trans-",
    "affix": None
})
print(f"Generated Word: {new_coin['neologism']} ({new_coin['pos']})")
print(f"Algorithm: {new_coin['algorithm_path']}")
print(f"Sample Sentence: {new_coin['sample_sentence']}")

new_coin_2 = generate_neologism({
    "origin_type": "latinized",
    "origin": "-struct-",
    "target_pos": "female_agent",
    "prefix": "con-",
    "affix": None
})
print(f"\nGenerated Word: {new_coin_2['neologism']} ({new_coin_2['pos']})")
print(f"Algorithm: {new_coin_2['algorithm_path']}")