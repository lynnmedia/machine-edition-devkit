/**
 * Minimal TypeScript/JavaScript consumer example demonstrating offline consumption
 * of a Machine Edition v0.1 package without proprietary SDK dependencies.
 */

import * as fs from "node:fs";
import * as path from "node:path";

interface Manifest {
  package_id: string;
  title: string;
  version: string;
  provenance_file?: string;
  human_readable_entrypoint?: string;
}

interface MeaningUnit {
  id: string;
  record_type: string;
  version: string;
  resolution_level: string;
  title: string;
  claim: string;
  provenance_id: string;
  scope: string;
}

interface ProvenanceRecord {
  id: string;
  record_type: string;
  source_title: string;
  source_url?: string;
  source_scope: string;
}

export function consumeMachineEdition(packageDir: string) {
  const manifestPath = path.join(packageDir, "manifest.json");
  if (!fs.existsSync(manifestPath)) {
    throw new Error(`Missing manifest: ${manifestPath}`);
  }

  const manifest: Manifest = JSON.parse(fs.readFileSync(manifestPath, "utf-8"));
  console.log(`Loaded Package: ${manifest.title} (${manifest.package_id} v${manifest.version})`);

  // Read Provenance Records
  const provFile = path.join(packageDir, manifest.provenance_file || "provenance.jsonl");
  const provenanceMap = new Map<string, ProvenanceRecord>();
  if (fs.existsSync(provFile)) {
    const lines = fs.readFileSync(provFile, "utf-8").split("\n").filter((l) => l.trim().length > 0);
    for (const line of lines) {
      const rec: ProvenanceRecord = JSON.parse(line);
      provenanceMap.set(rec.id, rec);
    }
  }

  // Read Meaning Units
  const muFile = path.join(packageDir, "meaning-units.jsonl");
  const meaningUnits: MeaningUnit[] = [];
  if (fs.existsSync(muFile)) {
    const lines = fs.readFileSync(muFile, "utf-8").split("\n").filter((l) => l.trim().length > 0);
    for (const line of lines) {
      const rec: MeaningUnit = JSON.parse(line);
      meaningUnits.push(rec);
    }
  }

  console.log(`Parsed ${meaningUnits.length} meaning units.`);

  if (meaningUnits.length > 0) {
    const sampleUnit = meaningUnits[0];
    console.log(`Sample Unit [${sampleUnit.id} - ${sampleUnit.resolution_level}]: "${sampleUnit.title}"`);
    console.log(`Claim: ${sampleUnit.claim}`);

    const prov = provenanceMap.get(sampleUnit.provenance_id);
    if (prov) {
      console.log(`Provenance Source: ${prov.source_title} (${prov.source_url})`);
    } else {
      throw new Error(`Unresolved provenance_id: ${sampleUnit.provenance_id}`);
    }
  }

  return { manifest, meaningUnits, provenanceMap };
}

if (require.main === module) {
  const defaultPath = path.resolve(__dirname, "../../specimen/srow/package");
  consumeMachineEdition(defaultPath);
}
