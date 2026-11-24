// News image entry for make.fun bounty news-image-20261124.
// Node 22, standard library only, no network.
// Writes the entry image (entry.png beside this file) to the output
// directory as entry.png, byte for byte, so the program is fully
// deterministic: two runs produce identical output.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
