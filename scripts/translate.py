import os
from os.path import dirname, join, exists
from ovos_utils.bracket_expansion import expand_options
from googletranslate_neon_plugin import GoogleTranslator

tx = GoogleTranslator()

src_lang = "en-us"
target_langs = ["es-es", "de-de", "fr-fr", "it-it", "pt-pt", "ca-es",
                "da-dk", "gl-es", "hu-hu", "nl-nl", "ru-ru", "sv-se"]

exts = [".voc", ".dialog", ".intent", ".entity"]
res_folder = join(dirname(dirname(__file__)), "locale")

src_files = {}
for root, dirs, files in os.walk(res_folder):
    if src_lang not in root:
        continue
    for f in files:
        if any(f.endswith(e) for e in exts):
            src_files[f] = join(root, f)

for lang in target_langs:
    os.makedirs(join(res_folder, lang), exist_ok=True)

    for name, src in src_files.items():
        dst = join(res_folder, lang, name)
        if exists(dst):
            continue

        tx_lines = []
        with open(src) as f:
            lines = [l for l in f.read().split("\n") if l and not l.startswith("#")]

        for l in lines:
            expanded = expand_options(l)
            for l2 in expanded:
                try:
                    translated = tx.translate(l2, target=lang, source=src_lang)
                    tx_lines.append(translated)
                except:
                    continue

        with open(dst, "w") as f:
            f.write(f"# auto translated from {src_lang} to {lang}\n")
            for translated in set(tx_lines):
                f.write(translated + "\n")
