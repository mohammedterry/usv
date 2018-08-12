import re

def singularise(word):
    lower = word.lower()
    for w in singular_uninflected:
        if w.endswith(lower):
            return word
    for w in singular_uncountable:
        if w.endswith(lower):
            return word
    for w in singular_ie:
        if lower.endswith(w+"s"):
            return w
    for w in singular_s:
        if lower.endswith(w + 'es'):
            return w
    for w in singular_irregular:
        if lower.endswith(w):
            return re.sub('(?i)'+w+'$', singular_irregular[w], word)
    for rule in singular_rules:
        suffix, inflection = rule
        match = suffix.search(word)
        if match:
            groups = match.groups()
            for k in range(0, len(groups)):
                if groups[k] == None:
                    inflection = inflection.replace('\\'+str(k+1), '')
            return suffix.sub(inflection, word)
    return word

re_vowel = re.compile(r"a|e|i|o|u|y", re.I)
VOWELS = "aeiouy"

singular_rules = [
    ['(?i)(.)ae$', '\\1a'],
    ['(?i)(.)itis$', '\\1itis'],
    ['(?i)(.)eaux$', '\\1eau'],
    ['(?i)(quiz)zes$', '\\1'],
    ['(?i)(matr)ices$', '\\1ix'],
    ['(?i)(ap|vert|ind)ices$', '\\1ex'],
    ['(?i)^(ox)en', '\\1'],
    ['(?i)(alias|status)es$', '\\1'],
    ['(?i)([octop|vir])i$', '\\1us'],
    ['(?i)(cris|ax|test)es$', '\\1is'],
    ['(?i)(shoe)s$', '\\1'],
    ['(?i)(o)es$', '\\1'],
    ['(?i)(bus)es$', '\\1'],
    ['(?i)([m|l])ice$', '\\1ouse'],
    ['(?i)(x|ch|ss|sh)es$', '\\1'],
    ['(?i)(m)ovies$', '\\1ovie'],
    ['(?i)(.)ombies$', '\\1ombie'],
    ['(?i)(s)eries$', '\\1eries'],
    ['(?i)([^aeiouy]|qu)ies$', '\\1y'],
    # Certain words ending in -f or -fe take -ves in the plural (lives, wolves).
    ["([aeo]l)ves$", "\\1f"],
    ["([^d]ea)ves$", "\\1f"],
    ["arves$", "arf"],
    ["erves$", "erve"],
    ["([nlw]i)ves$", "\\1fe"],
    ['(?i)([lr])ves$', '\\1f'],
    ["([aeo])ves$", "\\1ve"],
    ['(?i)(sive)s$', '\\1'],
    ['(?i)(tive)s$', '\\1'],
    ['(?i)(hive)s$', '\\1'],
    ['(?i)([^f])ves$', '\\1fe'],
    # -es suffix.
    ['(?i)(^analy)ses$', '\\1sis'],
    ['(?i)((a)naly|(b)a|(d)iagno|(p)arenthe|(p)rogno|(s)ynop|(t)he)ses$', '\\1\\2sis'],
    ['(?i)(.)opses$', '\\1opsis'],
    ['(?i)(.)yses$', '\\1ysis'],
    ['(?i)(h|d|r|o|n|b|cl|p)oses$', '\\1ose'],
    ['(?i)(fruct|gluc|galact|lact|ket|malt|rib|sacchar|cellul)ose$', '\\1ose'],
    ['(?i)(.)oses$', '\\1osis'],
    # -a
    ['(?i)([ti])a$', '\\1um'],
    ['(?i)(n)ews$', '\\1ews'],
    ['(?i)s$', ''],
]

singular_uninflected = [
    "aircraft", "antelope", "bison", "bream", "breeches", "britches", "carp", "cattle", "chassis",
    "clippers", "cod", "contretemps", "corps", "debris", "diabetes", "djinn", "eland",
    "elk", "flounder", "gallows", "georgia", "graffiti", "headquarters", "herpes", "high-jinks",
    "homework", "innings", "jackanapes", "mackerel", "measles", "mews", "moose", "mumps", "news",
    "offspring", "pincers", "pliers", "proceedings", "rabies", "salmon", "scissors", "series",
    "shears", "species", "swine", "swiss", "trout", "tuna", "whiting", "wildebeest"
]
singular_uncountable = [
    "advice", "bread", "butter", "cannabis", "cheese", "electricity", "equipment", "fruit", "furniture",
    "garbage", "gravel", "happiness", "information", "ketchup", "knowledge", "love", "luggage",
    "mathematics", "mayonnaise", "meat", "mustard", "news", "progress", "research", "rice", "sand",
    "software", "understanding", "water"
]
singular_ie = [
    "algerie", "auntie", "beanie", "birdie", "bogie", "bombie", "bookie", "collie", "cookie", "cutie",
    "doggie", "eyrie", "freebie", "goonie", "groupie", "hankie", "hippie", "hoagie", "hottie",
    "indie", "junkie", "laddie", "laramie", "lingerie", "meanie", "nightie", "oldie", "^pie",
    "pixie", "quickie", "reverie", "rookie", "softie", "sortie", "stoolie", "sweetie", "techie",
    "^tie", "toughie", "valkyrie", "veggie", "weenie", "yuppie", "zombie"
]
singular_s = [
        "acropolis", "aegis", "alias", "asbestos", "bathos", "bias", "bus", "caddis", "canvas",
        "chaos", "christmas", "cosmos", "dais", "digitalis", "epidermis", "ethos", "gas", "glottis",
        "ibis", "lens", "mantis", "marquis", "metropolis", "pathos", "pelvis", "polis", "rhinoceros",
        "sassafras", "trellis"
]

singular_irregular = {
            "men": "man",
         "people": "person",
       "children": "child",
          "sexes": "sex",
           "axes": "axe",
          "moves": "move",
          "teeth": "tooth",
          "geese": "goose",
           "feet": "foot",
            "zoa": "zoon",
       "atlantes": "atlas",
        "atlases": "atlas",
         "beeves": "beef",
       "brethren": "brother",
       "children": "child",
        "corpora": "corpus",
       "corpuses": "corpus",
           "kine": "cow",
    "ephemerides": "ephemeris",
        "ganglia": "ganglion",
          "genii": "genie",
         "genera": "genus",
       "graffiti": "graffito",
         "helves": "helve",
         "leaves": "leaf",
         "loaves": "loaf",
         "monies": "money",
      "mongooses": "mongoose",
         "mythoi": "mythos",
      "octopodes": "octopus",
          "opera": "opus",
         "opuses": "opus",
           "oxen": "ox",
          "penes": "penis",
        "penises": "penis",
    "soliloquies": "soliloquy",
         "testes": "testis",
        "trilbys": "trilby",
         "turves": "turf",
         "numena": "numen",
       "occipita": "occiput",
            "our": "my",
}

for rule in singular_rules:
    rule[0] = re.compile(rule[0])