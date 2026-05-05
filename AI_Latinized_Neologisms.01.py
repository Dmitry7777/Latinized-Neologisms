import re

# ============================================================
# 1. COMPLETE ALPHABETICAL DATA STRUCTURES
# ============================================================

PREFIXES = [
    "a-", "ab-", "ac-", "ad-", "aero-", "af-", "ag-", "agro-", "air-",
    "al-", "am-", "an-", "ar-", "as-", "at-",
    "bene-", "beni-", "bi-",
    "car-", "co-", "coach-", "coch-", "col-", "com-", "con-", "contra-", "cor-", "cuch-",
    "de-", "deo-", "deter-", "di-", "dif-", "dis-",
    "e-", "ec-", "ef-", "el-", "electro-", "em-", "en-", "ex-", "exer-", "exter-", "extra-", "extro-",
    "ferra-", "ferro-",
    "hex-", "homo-", "hypo-",
    "il-", "im-", "in-", "infra-", "infro-", "inter-", "intra-", "intro-", "ir-", "it-",
    "la-", "le-", "ligne-", "liqu-", "lo-", "loco-", "luc-", "lud-", "ludo-",
    "male-", "mali-", "meta-", "micro-", "mini-", "mis-", "mono-", "multi-",
    "neo-", "nulti-",
    "ob-", "op-", "os-",
    "per-", "poly-", "pre-", "prima-", "primo-", "pro-", "pseudo-", "psycho-",
    "que-",
    "re-", "retro-",
    "san-", "se-", "semi-", "sexto-", "sin-", "stereo-", "su-", "sub-", "suf-", "sup-",
    "super-", "supra-", "sus-", "sur-",
    "techno-", "tele-", "theo-", "trans-", "tuss-",
    "ultra-", "ultro-", "un-", "uni-"
]

AFFIXES = [
    "ab-", "ob-", "sub-", "suf-", "sup-"
]

LATINIZED_ORIGINS = [
    # A
    "-act-",      # do, drive, act
    "-alm-",      # nourish, soul
    "-alph-",     # alpha, first
    "-alt-",      # high, deep
    "-alta-",     # high (feminine)
    "-alto-",     # high (masculine)
    "-ama-",      # love
    "-amar-",     # love, bitter
    "-ami-",      # friend, love
    "-amigo-",    # friend
    "-amo-",      # love
    "-amor-",     # love
    "-amour-",    # love (French)
    "-anim-",     # soul, life, spirit
    "-aqua-",     # water
    "-argent-",   # silver
    "-audi-",     # hear
    "-aure-",     # gold, golden
    "-avi-",      # bird, fly
    "-avia-",     # bird, flight
    "-aviate-",   # fly
    
    # B
    "-bail-",     # carry, give
    "-bark-",     # boat, tree covering
    "-bay-",      # bay, berry
    "-bic-",      # two, twice
    "-bien-",     # good, well
    "-bon-",      # good
    "-buc-",      # cheek, mouth
    
    # C
    "-cab-",      # cabin, take
    "-cad-",      # fall
    "-cal-",      # heat, beauty
    "-calor-",    # heat
    "-can-",      # sing, dog
    "-cap-",      # head, take, seize
    "-car-",      # car, cart, dear
    "-cargo-",    # load, burden
    "-cart-",     # card, chart
    "-cent-",     # hundred
    "-cento-",    # hundred
    "-cer-",      # wax, perceive
    "-cere-",     # wax, grain
    "-chid-",     # child (variant)
    "-chil-",     # child (variant)
    "-cir-",      # circle, ring
    "-claim-",    # cry out, shout
    "-clear-",    # clear, bright
    "-cogn-",     # know, learn
    "-communicate-", # share, make common
    "-cor-",      # heart
    "-cora-",     # heart, core
    "-count-",    # count, number
    "-cur-",      # care, run, course
    "-cuss-",     # strike, shake
    
    # D
    "-dar-",      # give
    "-dart-",     # dart, throw
    "-deco-",     # ten, decoration
    "-dent-",     # tooth
    "-dic-",      # say, declare
    "-dict-",     # say, speak
    "-duc-",      # lead
    "-duce-",     # lead
    "-duct-",     # lead, draw
    "-duo-",      # two
    
    # F
    "-fact-",     # make, do
    "-farm-",     # firm, fixed
    "-fect-",     # make, do
    "-fem-",      # woman, feminine
    "-fic-",      # make, do
    "-figure-",   # shape, form
    "-firm-",     # firm, strengthen
    "-fix-",      # fasten, attach
    "-form-",     # shape, form
    "-fuc-",      # paint, makeup
    "-fuse-",     # pour, melt
    
    # G
    "-gat-",      # gate, go
    "-gel-",      # ice, freeze
    "-gene-",     # birth, kind, race
    "-gic-",      # drive, knowledge
    "-gust-",     # taste
    
    # H
    "-hiberne-",  # winter
    
    # L
    "-la-",       # place, feminine article
    "-lace-",     # entice, net
    "-lact-",     # milk
    "-late-",     # carry, bear
    "-lax-",      # loose, slack
    "-le-",       # gather, read, place
    "-lect-",     # read, choose, gather
    "-lic-",      # permit, entice
    "-lict-",     # leave, abandon
    "-liqu-",     # liquid, flow
    "-list-",     # desire, list
    "-lo-",       # place, speech
    "-lob-",      # lobe, throw
    "-locate-",   # place, locate
    "-loct-",     # place, location
    "-lor-",      # lord, pale
    "-luce-",     # light
    "-luct-",     # struggle, wrestle
    "-lude-",     # play, mock
    "-lune-",     # moon
    "-lup-",      # wolf
    "-lust-",     # light, desire, shine
    
    # M
    "-mal-",      # bad, evil
    "-mar-",      # sea
    "-maraca-",   # rattle, instrument
    "-mart-",     # war, Mars
    "-mas-",      # male, masculine
    "-mes-",      # middle, month
    "-mic-",      # small
    "-mil-",      # thousand, soldier
    "-milo-",     # thousand
    "-mit-",      # send, let go
    "-mol-",      # mill, grind, soft
    "-mor-",      # die, death, custom
    "-mort-",     # death
    "-much-",     # many, much
    "-mune-",     # service, duty, wall
    "-mute-",     # change, silent
    
    # N
    "-nar-",      # tell, story
    "-nev-",      # snow, nerve
    "-nic-",      # victory
    "-nono-",     # ninth
    "-nor-",      # know, north, rule
    "-nos-",      # we, us, nose
    
    # O
    "-octo-",     # eight
    "-ola-",      # small, oil
    "-olla-",     # pot, jar
    "-ore-",      # mouth, gold, mountain
    "-origin-",   # beginning, source
    "-oss-",      # bone
    "-ovra-",     # work, egg
    
    # P
    "-par-",      # equal, appear, prepare
    "-part-",     # part, divide
    "-pede-",     # foot
    "-perr-",     # through, very
    "-pese-",     # weigh, hang
    "-pic-",      # picture, paint
    "-pict-",     # paint, picture
    "-place-",    # place, please
    "-plant-",    # plant, sole
    "-plate-",    # flat, plate
    "-play-",     # play, fold
    "-port-",     # carry, gate
    "-pose-",     # place, put
    "-press-",    # press, push
    "-prior-",    # former, before
    
    # Q
    "-quad-",     # four
    "-qual-",     # what kind, quality
    "-quare-",    # square
    "-quase-",    # as if, shake
    "-quay-",     # wharf, key
    "-quer-",     # complain, seek
    "-quest-",    # seek, ask
    "-quinto-",   # fifth
    "-quire-",    # seek, ask
    
    # R
    "-ram-",      # branch
    "-rect-",     # straight, right, rule
    "-rim-",      # edge, crack
    "-rom-",      # Rome, Roman
    "-rot-",      # wheel, turn
    
    # S
    "-salt-",     # salt, leap
    "-salut-",    # health, greeting
    "-salute-",   # health, safety
    "-san-",      # health, holy
    "-sanct-",    # holy, sacred
    "-sangu-",    # blood
    "-scence-",   # growing, becoming
    "-scent-",    # climbing, smelling
    "-sen-",      # old, elder
    "-sent-",     # feel, perceive
    "-septo-",    # seven
    "-ser-",      # serve, join, series
    "-sert-",     # join, connect
    "-sexto-",    # sixth
    "-sign-",     # mark, sign
    "-sist-",     # stand, cause to stand
    "-site-",     # place, position
    "-sol-",      # sun, alone, comfort
    "-spade-",    # shovel, sword
    "-stance-",   # stand, position
    "-stant-",    # stand, standing
    "-struct-",   # build
    
    # T
    "-tain-",     # hold, touch
    "-tect-",     # cover, roof
    "-tend-",     # stretch, strive
    "-tens-",     # stretch, tension
    "-tent-",     # stretch, hold
    "-terr-",     # earth, land
    "-terra-",    # earth, land
    "-test-",     # witness, test
    "-text-",     # weave, text
    "-tor-",      # twist
    "-tort-",     # twist, turn
    "-trio-",     # three
    "-turn-",     # turn
    
    # U
    "-urban-",    # city
    
    # V
    "-vac-",      # empty
    "-val-",      # strong, worth
    "-vency-",    # come, arrive
    "-vend-",     # sell
    "-vent-",     # wind, come
    "-ver-",      # true, spring
    "-verb-",     # word
    "-vern-",     # spring, slave
    "-vers-",     # turn
    "-verse-",    # turn
    "-vert-",     # turn
    "-vest-",     # clothing
    "-vib-",      # shake, vibrate
    "-vic-",      # conquer, change, village
    "-vict-",     # conquer, victory
    "-vid-",      # see
    "-vil-",      # cheap, town
    "-vio-",      # way, path
    "-vip-",      # important person
    "-vis-",      # see
    "-vit-",      # life, vine
    "-viv-",      # live, alive
    "-viz-",      # see, sight
    
    # Z
    "-zor-",      # dawn, fox
    "-zorr-",     # fox
]

SUFFIXES = {
    "noun_act": ["-ion", "-tion", "-sion", "-vion"],
    "noun_state": ["-tude", "-ality"],
    "adj": ["-al", "-ous", "-id", "-ive", "-mentary"],
    "adv": ["-ally", "-ously", "-culously"],
    "male_agent": ["-or", "-tor", "-dor", "-lor"],
    "female_agent": ["-ess", "-ness", "-ress", "-gess"],
    "neutral_agent": ["-ore", "-ue", "-gue", "-re"],
    "fem_non_human_agent": ["-rix"],
    "verb_simple": [
        "-ate", "-ates", "-ated", "-ating",
        "-ify", "-ifies", "-ified", "-ifying"
    ],
    "verb_special": [
        "-rate", "-rates", "-rated", "-rating",
        "-gate", "-gates", "-gated", "-gating",
        "-late", "-lates", "-lated", "-lating",
        "-bate", "-bates", "-bated", "-bating",
        "-cate", "-cates", "-cated", "-cating",
        "-date", "-dates", "-dated", "-dating",
        "-mate", "-mates", "-mated", "-mating",
        "-nate", "-nates", "-nated", "-nating",
        "-iate", "-iates", "-iated", "-iating",
        "-pate", "-pates", "-pated", "-pating",
        "-sate", "-sates", "-sated", "-sating",
        "-tate", "-tates", "-tated", "-tating",
        "-vate", "-vates", "-vated", "-vating"
    ],
    "noun_diminutive": ["-ette"],
    "noun_other": ["-cle", "-geon"],
    "adj_derived": ["-cular", "-culous"]
}

# ============================================================
# 2. PHASE 1 & 2: DECONSTRUCTION & VALIDATION (RECOGNITION)
# ============================================================

def tokenize_and_tag(word):
    """Recognizes the morphological components of a valid neologism."""
    original_word = word
    
    # --- Step A: Strip known affixes (outermost layer) ---
    detected_affix = None
    for affix in sorted(AFFIXES, key=len, reverse=True):
        if word.startswith(affix) and len(word) > len(affix) + 3:
            detected_affix = affix
            word = word[len(affix):]
            break
            
    # --- Step B: Strip known prefixes (middle layer) ---
    detected_prefix = None
    for prefix in sorted(PREFIXES, key=len, reverse=True):
        # Handle both hyphenated and non-hyphenated prefixes
        clean_prefix = prefix.rstrip("-")
        if word.startswith(clean_prefix) and len(word) > len(clean_prefix) + 3:
            # Check if remaining part could contain a valid origin
            temp_word = word[len(clean_prefix):]
            for origin in LATINIZED_ORIGINS:
                clean_origin = origin.replace("-", "")
                if temp_word.startswith(clean_origin):
                    detected_prefix = prefix
                    word = temp_word
                    break
        if detected_prefix:
            break

    # --- Step C: Identify Latinized Origin and Suffix ---
    detected_origin = None
    detected_suffix = None
    pos_tag = None

    for origin in sorted(LATINIZED_ORIGINS, key=len, reverse=True):
        clean_origin = origin.replace("-", "")
        if word.startswith(clean_origin):
            remaining = word[len(clean_origin):]
            
            # Find the suffix in the remaining part
            for category, suffixes in SUFFIXES.items():
                for suffix in sorted(suffixes, key=len, reverse=True):
                    if remaining == suffix:
                        detected_origin = origin
                        detected_suffix = suffix
                        pos_tag = category
                        break
                if detected_suffix:
                    break
            break

    # --- Step D: Validate and Assemble the Parse ---
    if detected_origin and detected_suffix:
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
    if suffix.endswith("ies"): return suffix[:-3] + "y"
    if suffix.endswith("ing"): return suffix[:-3]
    if suffix.endswith("ed"): return suffix[:-2]
    if suffix.endswith("s"): return suffix[:-1]
    return suffix

# ============================================================
# 3. PHASE 3: CONSTRUCTION (GENERATION)
# ============================================================

def generate_neologism(components):
    """
    Generates a neologism based on the provided algorithm path.
    components = {
        "origin_type": "latinized" | "iberian-romance",
        "origin": "-port-",
        "target_pos": "noun_act",
        "prefix": None,
        "affix": None
    }
    """
    origin = components["origin"].replace("-", "")
    suffix_category = components["target_pos"]
    chosen_suffix = SUFFIXES[suffix_category][0]
    
    core = origin + chosen_suffix
    
    if components.get("prefix"):
        core = components["prefix"].rstrip("-") + core
        
    if components.get("affix"):
        core = components["affix"].rstrip("-") + core
        
    pronoun_subj = "Ego"
    pronoun_obj = "is"
    
    sentence_1 = f"{pronoun_subj} {core}at {pronoun_obj}."
    
    return {
        "neologism": core,
        "pos": suffix_category,
        "algorithm_path": f"[{components.get('affix', '')} + {components.get('prefix', '')} + {origin} + {chosen_suffix}]",
        "sample_sentence": sentence_1
    }

# ============================================================
# 4. VERIFICATION & DEMONSTRATION
# ============================================================

print("=" * 60)
print("DATA STRUCTURES VERIFICATION")
print("=" * 60)
print(f"✓ Prefixes loaded:   {len(PREFIXES)}")
print(f"✓ Affixes loaded:    {len(AFFIXES)}")
print(f"✓ Origins loaded:    {len(LATINIZED_ORIGINS)}")
print(f"✓ Suffix categories: {len(SUFFIXES)}")
print()

# Check for new prefixes
new_prefixes = ["dif-", "el-", "luc-", "sus-", "sur-"]
print("New Prefixes Check:")
for p in new_prefixes:
    status = "✓" if p in PREFIXES else "✗ MISSING"
    print(f"  {status} {p}")
print()

# Check for new origins
new_origins = ["-audi-", "-gel-", "-mort-", "-viv-", "-nev-", "-gust-", "-fem-", "-lup-", "-vib-", "-alm-"]
print("New Origins Check:")
for o in new_origins:
    status = "✓" if o in LATINIZED_ORIGINS else "✗ MISSING"
    print(f"  {status} {o}")
print()

print("=" * 60)
print("MACHINE RECOGNITION TESTS")
print("=" * 60)
test_words = [
    "importation",
    "reporter",
    "subvention",
    "contraversion",
    "benediction",
    "transparency",
    "biodictatory",
    # New test words with new origins
    "inaudible",
    "congelation",
    "immortal",
    "revival",
    "sublunar",
]

for word in test_words:
    result = tokenize_and_tag(word)
    if result["status"] == "recognized":
        print(f"✓ '{word}' → {result['algorithm_path']} ({result['pos']})")
    else:
        print(f"✗ '{word}' → UNRECOGNIZED")

print()
print("=" * 60)
print("NEOLOGISM GENERATION TESTS")
print("=" * 60)

test_generations = [
    {"origin": "-luce-", "target_pos": "adj", "prefix": "trans-"},
    {"origin": "-struct-", "target_pos": "female_agent", "prefix": "con-"},
    {"origin": "-audi-", "target_pos": "adj", "prefix": "in-"},
    {"origin": "-mort-", "target_pos": "adj", "prefix": "im-"},
    {"origin": "-gel-", "target_pos": "noun_act", "prefix": "con-"},
    {"origin": "-lune-", "target_pos": "adj", "prefix": "sub-"},
]

for gen in test_generations:
    result = generate_neologism(gen)
    print(f"✓ {result['algorithm_path']} → '{result['neologism']}' ({result['pos']})")