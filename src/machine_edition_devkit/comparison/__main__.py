from pathlib import Path
import sys
from machine_edition_devkit.comparison import ComparisonHarness

def main():
    harness = ComparisonHarness()
    
    if len(sys.argv) > 1 and sys.argv[1] == "inspect":
        print("Comparison Source:", harness.source_inventory["source_name"])
        print(f"Tracked Facts: {len(harness.source_inventory['facts'])}")
        for f in harness.source_inventory["facts"]:
            print(f"  [{f['fact_id']}] {f['subject']}: \"{f['statement'][:60]}...\"")
    elif len(sys.argv) > 1 and sys.argv[1] == "matrix":
        matrix = harness.get_property_matrix()
        print(f"{'Property':<34} {'PDF':<18} {'EPUB':<18} {'Naive RAG':<18} {'Machine Edition'}")
        print("-" * 110)
        for prop, values in matrix.items():
            print(f"{prop:<34} {values['PDF'][:16]:<18} {values['EPUB'][:16]:<18} {values['Naive RAG'][:16]:<18} {values['Machine Edition']}")
    else:
        results = harness.run_all()
        print(harness.render_summary_table(results))

if __name__ == "__main__":
    main()
