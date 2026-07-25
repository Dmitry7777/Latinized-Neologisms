"""
AI_Latinized_Neologisms.py — Full Integrated Version
Incorporates all new prefixes, origins, suffixes, and transformation rules.
"""

import re

# ============================================================
# 1. DATA STRUCTURES (from user's latest specification)
# ============================================================

PREFIXES = [
    "a-","ab-","ac-","ad-","aero-","af-","ag-","agro-","air-",
    "al-","am-","an-","ar-","art-","as-","at-","auto-","az-",
    "bene-","beni-","beno-","bi-",
    "car-","circum-","co-","coach-","coch-","col-","com-","con-",
    "contra-","cor-","cuch-",
    "de-","deo-","deter-","di-","dif-","dis-",
    "e-","ec-","ef-","el-","electro-","em-","en-","ex-","exer-",
    "exter-","extra-","extro-",
    "fem-","fer-","ferra-","ferro-",
    "geo-",
    "hex-","homo-","hyper-","hypo-",
    "il-","im-","in-","infra-","infro-","inter-","intra-","intro-","ir-","it-",
    "la-","le-","ligne-","liqu-","lo-","loco-","luc-","lud-","ludo-",
    "male-","mali-","malo-","mani-","manu-","meta-","micro-","mini-",
    "mis-","mono-","multi-",
    "negra-","negro-","neo-","neuro-","nix-","nova-","novi-","novo-",
    "ob-","omni-","op-","os-",
    "per-","poly-","pre-","prima-","primo-","pro-","pseudo-","psycho-",
    "que-",
    "re-","retro-",
    "san-","se-","semi-","sept-","ser-","sexo-","sexto-","sin-","sono-",
    "stereo-","su-","sub-","suf-","suno-","sup-","super-","supra-","sur-","sus-",
    "techno-","tele-","theo-","trans-","tri-","tuss-",
    "ultra-","ultro-","un-","uni-"
]

AFFIXES = ["ab-","ob-","sub-","suf-","sup-"]  # same as before

LATINIZED_ORIGINS = [
    "-act-","-alm-","-alph-","-alt-","-alta-","-alto-",
    "-ama-","-amar-","-ami-","-amigo-","-amo-","-amor-","-amour-",
    "-anim-","-aqu-","-aqua-","-argent-","-aud-","-audi-","-aug-",
    "-aure-","-av-","-avi-","-avia-","-aviate-","-az-",
    "-bail-","-bark-","-bay-","-ben-","-bic-","-bien-","-bon-","-buc-","-burg-",
    "-cab-","-cad-","-cal-","-calor-","-cam-","-can-","-cap-","-car-","-cargo-","-cart-",
    "-ceed-","-cent-","-cento-","-cer-","-cere-","-cess-","-chid-","-chil-",
    "-cir-","-cis-","-claim-","-clear-","-cogn-","-com-","-communicate-",
    "-cor-","-cora-","-cord-","-count-","-cour-","-cred-","-cry-","-crypt-",
    "-cuc-","-cur-","-cuss-","-cut-",
    "-dar-","-dart-","-deco-","-dent-","-dic-","-dict-","-dom-","-dorm-",
    "-duc-","-duce-","-duct-","-duo-","-dur-",
    "-ech-","-eg-","-equ-","-exist-",
    "-fact-","-farm-","-fect-","-fem-","-fer-","-fic-","-figur-","-figure-",
    "-firm-","-fix-","-form-","-fuc-","-fug-","-fus-","-fuse-",
    "-gat-","-gel-","-gene-","-ger-","-gic-","-grad-","-gress-","-gust-","-gyr-",
    "-hiberne-",
    "-ject-",
    "-la-","-labor-","-lace-","-lact-","-lam-","-lat-","-late-","-lax-",
    "-le-","-lect-","-lic-","-lict-","-liqu-","-list-","-lo-","-lob-",
    "-loc-","-locate-","-loct-","-lor-","-luc-","-luce-","-luct-",
    "-lud-","-lude-","-lune-","-lup-","-lust-","-luv-","-lux-",
    "-mal-","-mar-","-maraca-","-mart-","-mas-","-merc-","-mes-",
    "-mic-","-mil-","-milo-","-mit-","-mol-","-mor-","-mort-",
    "-much-","-mune-","-mut-","-mute-",
    "-nar-","-nat-","-nect-","-nev-","-nic-","-niev-","-noc-",
    "-nono-","-nor-","-norm-","-nos-","-nov-","-nur-",
    "-octo-","-ol-","-ola-","-olla-","-op-","-or-","-ord-",
    "-ore-","-origin-","-oss-","-ov-","-ovra-","-oz-",
    "-par-","-part-","-ped-","-pede-","-pel-","-perr-","-pes-","-pese-",
    "-pess-","-phobia-","-pic-","-pict-","-place-","-plant-","-plate-",
    "-play-","-plic-","-pluv-","-porc-","-port-","-pose-","-pot-",
    "-press-","-prior-","-puls-","-pur-",
    "-quad-","-qual-","-quant-","-quare-","-quase-","-quay-",
    "-quer-","-quest-","-quinto-","-quire-","-quot-",
    "-ram-","-rap-","-rect-","-rim-","-rom-","-rot-","-rub-","-rum-",
    "-sal-","-salt-","-salut-","-salute-","-san-","-sanct-","-sang-","-sangu-",
    "-scence-","-scent-","-scri-","-scribe-","-script-","-sect-",
    "-sen-","-sent-","-sept-","-septo-","-ser-","-sert-","-sexto-",
    "-sign-","-sist-","-site-","-sof-","-sol-","-soph-","-spade-","-spect-",
    "-stance-","-stant-","-struct-","-sum-","-sumpt-",
    "-tain-","-tall-","-tect-","-tend-","-tens-","-tent-","-terr-","-terra-",
    "-test-","-text-","-tor-","-tort-","-tra-","-tri-","-trio-","-tro-","-tru-","-turn-",
    "-ult-","-urb-","-urban-",
    "-vac-","-val-","-vect-","-vency-","-vend-","-vent-","-ver-",
    "-verb-","-vern-","-vers-","-verse-","-vert-","-vest-",
    "-vib-","-vic-","-vict-","-vid-","-vil-","-vinc-","-vio-",
    "-vip-","-vis-","-vit-","-viv-","-viz-","-volv-","-vot-",
    "-xen-","-xer-","-xero-","-xyl-",
    "-yel-","-yok-",
    "-zon-","-zor-","-zorr-","-zurr-"
]

SUFFIXES = {
    "noun_act_sg": ["-ion", "-tion", "-sion", "-vion", "-gion"],
    "noun_act_pl": ["-ions", "-tions", "-sions", "-vions", "-gions"],
    "noun_state_sg": ["-tude", "-ality", "-idity", "-lty", "-gency"],
    "noun_state_pl": ["-tudes", "-alities", "-idities", "-lties", "-gencies"],
    "noun_agent_male_sg": ["-or", "-tor", "-dor", "-lor"],
    "noun_agent_male_pl": ["-ors", "-tors", "-dors", "-lors"],
    "noun_agent_female_sg": ["-ess", "-ness", "-ress", "-gess"],
    "noun_agent_female_pl": ["-esses", "-nesses", "-resses", "-gesses"],
    "noun_agent_neutral_sg": ["-ore", "-ue", "-gue", "-re", "-aire"],
    "noun_agent_neutral_pl": ["-ores", "-ues", "-gues", "-res", "-aires"],
    "noun_diminutive_sg": ["-ette", "-cle"],
    "noun_diminutive_pl": ["-ettes", "-cles"],
    "noun_other_sg": ["-geon", "-ary", "-ory", "-tory", "-tary", "-ite", "-ipe"],
    "noun_other_pl": ["-aries", "-ories", "-tories", "-taries", "-ites", "-ipes"],
    "noun_fem_nonhuman_sg": ["-rix", "-trix"],
    "noun_fem_nonhuman_pl": ["-rixes", "-trixes"],
    "adj": ["-al", "-ous", "-id", "-ive", "-able", "-cular", "-culous", "-ant", "-gent", "-lt"],
    "adj_derived": ["-mentary"],
    "adv": ["-ally", "-ously", "-culously", "-ively", "-gently"],
    "verb_simple": [  # base forms, conjugated forms added in generation
        "-ate", "-ates", "-ated", "-ating",
        "-ify", "-ifies", "-ified", "-ifying",
        "-ip", "-ips", "-ipped", "-ipping",
        # all the -bate, -cate, etc. series from your original verb_special
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
    ]
}

# ============================================================
# 2. ASSIMILATION & CONJUNCTION RULES
# ============================================================

# Conjunction vowel between origin and suffix when needed
def get_conjunction(origin_clean, suffix):
    """Return the appropriate conjunction vowel (-a-, -i-, etc.) for a given origin+suffix pair.
    Based on user's examples: -cuc- + -i- + -ate; -farm- + -a- + -tion; etc.
    We implement a heuristic: if origin ends in a consonant cluster, use '-a-'; for -cuc- special case '-i-'.
    A full table would be needed; here we simplify with a dictionary."""
    # Special cases from your document
    special = {
        "cuc": "i",
        "farm": "a",
        "firm": "a",
        "form": "a"
    }
    clean = origin_clean.lower()
    if clean in special:
        return special[clean]
    # Default: if origin ends with two consonants, use 'a' to ease pronunciation
    if re.search(r'[bcdfghjklmnpqrstvwxyz]{2}$', clean):
        return "a"
    return ""  # no conjunction vowel needed

# Prefix assimilation: con-, col-, com-, etc., and il-, im-, in-, ir-, it-
def assimilate_prefix(prefix_clean, word_part):
    """Apply assimilation rules. Return the correctly modified prefix string."""
    if prefix_clean in ["con", "col", "com", "cor", "co"]:
        first_letter = word_part[0].lower()
        if first_letter == 'l': return "col"
        if first_letter in 'bmp': return "com"
        if first_letter == 'r': return "cor"
        if first_letter in 'aeiou' or first_letter in 'ghj': return "co"
        return "con"  # default
    if prefix_clean in ["il", "im", "in", "ir", "it"]:
        first = word_part[0].lower()
        if prefix_clean == "il" and first == 'l': return "il"
        if prefix_clean == "im" and first in 'mp': return "im"
        if prefix_clean == "in" and first not in 'lmnr': return "in"
        if prefix_clean == "ir" and first == 'r': return "ir"
        if prefix_clean == "it" and first in 'et': return "it"
        # fallback
        return prefix_clean
    # For dis-/dif-: dif- before f
    if prefix_clean == "dis":
        if word_part[0].lower() == 'f': return "dif"
        return "dis"
    if prefix_clean == "dif":
        return "dif"  # already assimilated form
    return prefix_clean  # no change

# ============================================================
# 3. TRANSFORMATION FUNCTIONS (NOUN→ADJ, ADV, VERB)
# ============================================================

def noun_act_to_adj(noun):
    """Convert -ion noun to adjective (-ive, -ble)."""
    # Remove common endings and add new suffix
    for end in ["ion", "tion", "sion", "vion", "lion", "gion"]:
        if noun.endswith(end):
            stem = noun[:-len(end)]
            # Choose -ive or -ble based on context; default -ive
            return stem + "ive"
    return noun

def noun_act_to_adv(noun):
    adj = noun_act_to_adj(noun)
    return adj + "ly"

def noun_act_to_verb(noun, suffix_type="ate"):
    """Convert -ion noun to simplified verb. Example: -tion -> -ate."""
    for end in ["tion", "sion", "ion", "vion"]:
        if noun.endswith(end):
            stem = noun[:-len(end)]
            if end == "tion": return stem + "ate"
            if end == "sion": return stem + "de"  # as per your example: -sion -> -de
            if end == "ion": return stem + "e"    # generic
            if end == "vion": return stem + "ve"
    return noun

# ============================================================
# 4. RECOGNITION (Updated for new data)
# ============================================================

def tokenize_and_tag(word):
    original_word = word
    detected_affix = None
    for affix in sorted(AFFIXES, key=len, reverse=True):
        if word.startswith(affix) and len(word) > len(affix)+3:
            detected_affix = affix
            word = word[len(affix):]
            break

    detected_prefix = None
    for prefix in sorted(PREFIXES, key=len, reverse=True):
        clean_prefix = prefix.rstrip("-")
        if word.startswith(clean_prefix):
            temp = word[len(clean_prefix):]
            # Check if temp starts with a known origin (possibly with conjunction vowel)
            for origin in LATINIZED_ORIGINS:
                clean_origin = origin.replace("-", "")
                # Allow optional conjunction vowel (a, i, e)
                match = re.match(rf"([aie])?{re.escape(clean_origin)}", temp)
                if match:
                    detected_prefix = prefix
                    # Remove the prefix and any conjunction vowel used
                    conjunction = match.group(1) if match.group(1) else ""
                    word = temp[len(conjunction):]  # will be removed later with origin stripping
                    break
        if detected_prefix:
            break

    detected_origin = None
    detected_suffix = None
    pos_tag = None
    # strip leading conjunction vowel if present
    word_trimmed = re.sub(r'^[aie]', '', word, count=1) if re.match(r'^[aie]', word) else word

    for origin in sorted(LATINIZED_ORIGINS, key=len, reverse=True):
        clean_origin = origin.replace("-", "")
        if word_trimmed.startswith(clean_origin):
            remaining = word_trimmed[len(clean_origin):]
            for cat, suffixes in SUFFIXES.items():
                for sfx in sorted(suffixes, key=len, reverse=True):
                    if remaining == sfx:
                        detected_origin = origin
                        detected_suffix = sfx
                        pos_tag = cat
                        break
                if detected_suffix:
                    break
            break

    if detected_origin and detected_suffix:
        base = detected_origin.replace("-", "") + detect_suffix_base(detected_suffix)
        return {
            "status": "recognized",
            "morphemes": {"affix": detected_affix, "prefix": detected_prefix,
                          "origin": detected_origin, "suffix": detected_suffix},
            "base_form": base,
            "pos": pos_tag,
            "algorithm_path": f"{'[Affix] + ' if detected_affix else ''}{'[Prefix] + ' if detected_prefix else ''}[{detected_origin}] + [{detected_suffix}]"
        }
    return {"status": "unrecognized", "original": original_word}

def detect_suffix_base(sfx):
    if sfx.endswith("ies"): return sfx[:-3]+"y"
    if sfx.endswith("ing"): return sfx[:-3]
    if sfx.endswith("ed"): return sfx[:-2]
    if sfx.endswith("s") and not sfx.endswith("ss"): return sfx[:-1]
    return sfx

# ============================================================
# 5. GENERATION (with full algorithm)
# ============================================================

def generate_neologism(components):
    """
    components = {
        "origin": "-port-",
        "target_pos": "noun_act_sg",
        "prefix": "trans-",    # optional
        "affix": None,
        "use_conjunction": True,  # apply conjunction vowel if needed
        "simplified_verb": False  # if True, follow simplified verb rules
    }
    """
    origin_clean = components["origin"].replace("-", "")
    suffix_category = components["target_pos"]
    # Choose suffix (default first in list)
    suffix = SUFFIXES[suffix_category][0]

    # Apply conjunction vowel if applicable
    conj = get_conjunction(origin_clean, suffix) if components.get("use_conjunction", True) else ""
    core = origin_clean + conj + suffix

    # Handle prefix (with assimilation)
    prefix_raw = components.get("prefix")
    if prefix_raw:
        prefix_clean = prefix_raw.rstrip("-")
        # Assimilate based on the start of core
        assimilated = assimilate_prefix(prefix_clean, core)
        # The prefix may already include a hyphen; we just use the assimilated form plus a hyphen if needed
        # For simplicity, we concatenate: assimilated + core (but often the prefix is attached directly without hyphen)
        core = assimilated + core  # e.g., "com" + "portation" -> "comportation"

    # Handle affix
    affix_raw = components.get("affix")
    if affix_raw:
        core = affix_raw.rstrip("-") + core

    # Generate a sample sentence (using your simplified verb conjugation)
    pronoun_subj = "Ego"
    pronoun_obj = "is"
    verb_form = core
    # crude verb conjugation: if core ends in 'e', add 's' for 3rd person? but we just use base + "at" for present
    sentence = f"{pronoun_subj} {verb_form}at {pronoun_obj}."

    return {
        "neologism": core,
        "pos": suffix_category,
        "algorithm_path": f"[{affix_raw or ''} + {prefix_raw or ''} + {origin_clean} + {conj} + {suffix}]",
        "sample_sentence": sentence
    }

# ============================================================
# 6. DEMONSTRATION & VERIFICATION
# ============================================================
if __name__ == "__main__":
    print("="*60)
    print("DATA VERIFICATION")
    print(f"Prefixes: {len(PREFIXES)}")
    print(f"Origins:  {len(LATINIZED_ORIGINS)}")
    print(f"Suffix categories: {len(SUFFIXES)}")
    print()

    # Test recognition with new origins
    test_words = [
        "conflation", "disruption", "immortal", "subvention", "transparency",
        "agricolation", "benediction", "circumspection", "diffluence", "exclusion"
    ]
    for w in test_words:
        res = tokenize_and_tag(w)
        if res["status"] == "recognized":
            print(f"✓ {w} -> {res['algorithm_path']}")
        else:
            print(f"✗ {w} unrecognized")

    print("\nGENERATION EXAMPLES")
    # Example 1: simplified verb with conjunction
    gen = generate_neologism({
        "origin": "-cuc-",
        "target_pos": "verb_simple",
        "prefix": None,
        "use_conjunction": True
    })
    print(f"Verb: {gen['neologism']} ({gen['algorithm_path']}) -> {gen['sample_sentence']}")

    # Example 2: noun with prefix assimilation
    gen2 = generate_neologism({
        "origin": "-port-",
        "target_pos": "noun_act_sg",
        "prefix": "com-"
    })
    print(f"Noun: {gen2['neologism']} ({gen['algorithm_path']})")

    # Example 3: transform a noun to adjective
    noun = "importation"
    adj = noun_act_to_adj(noun)
    print(f"Transformation: {noun} -> {adj} (adjective)")