import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// News-image entry: copy the pre-rendered front page to the output dir.
// Paths resolve relative to this script file, never the working directory.
const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const bytes = readFileSync(src);

// Validate the PNG before copying: magic bytes, then the IHDR chunk.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("entry.png is not a PNG (bad magic bytes)");
}
if (bytes.length < 33 || bytes.toString("ascii", 12, 16) !== "IHDR") {
  throw new Error("entry.png has no IHDR chunk");
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
const bitDepth = bytes[24];
const colourType = bytes[25];
if (width !== 1024 || height !== 1024) {
  throw new Error(`IHDR dimensions ${width}x${height}, expected 1024x1024`);
}
if (bitDepth !== 8 || colourType !== 2) {
  throw new Error(`unexpected PNG format: bit depth ${bitDepth}, colour type ${colourType}`);
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
writeFileSync(dest, bytes);
const digest = createHash("sha256").update(bytes).digest("hex");
console.log(`wrote ${dest} (${bytes.length} bytes, sha256 ${digest})`);
