/** Developer Kit v0.1.0: bounded TypeScript parser for the public SROW specimen.
 * Run with Node.js 22.18+ after validating the package.
 * Code: MIT. Specimen records: CC BY 4.0 within the authorized public scope.
 */

import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const packageDir = join(dirname(fileURLToPath(import.meta.url)), "../specimen/srow/package");
const manifest = JSON.parse(readFileSync(join(packageDir, "manifest.json"), "utf8"));
const provenance = new Set(
  readFileSync(join(packageDir, "provenance.jsonl"), "utf8")
    .split(/\r?\n/)
    .filter(Boolean)
    .map((line) => JSON.parse(line).id)
);
const units = readFileSync(join(packageDir, "meaning-units.jsonl"), "utf8")
  .split(/\r?\n/)
  .filter(Boolean)
  .map((line) => JSON.parse(line))
  .sort((a, b) => a.id.localeCompare(b.id))
  .slice(0, 3)
  .map((unit) => {
    if (!provenance.has(unit.provenance_id)) {
      throw new Error(`Unresolved provenance_id for ${unit.id}`);
    }
    return { id: unit.id, provenance_id: unit.provenance_id };
  });

console.log(JSON.stringify({
  package_id: manifest.package_id,
  version: manifest.version,
  meaning_units: units
}, null, 2));
