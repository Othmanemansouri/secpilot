#!/usr/bin/env python3
"""
Parser SARIF → JSON pour les résultats Semgrep

Lit le fichier SARIF généré par Semgrep et produit un JSON
structuré utilisable par le script LLM fix suggester.
"""

import json
import sys
from pathlib import Path


def parse_sarif(sarif_path: str) -> dict:
    """Extrait les violations depuis un fichier SARIF Semgrep"""

    sarif_file = Path(sarif_path)
    if not sarif_file.exists():
        print(f"Fichier SARIF non trouvé : {sarif_path}", file=sys.stderr)
        return {"source": "semgrep", "total_findings": 0, "findings": []}

    with open(sarif_file, encoding="utf-8") as f:
        sarif = json.load(f)

    findings = []

    for run in sarif.get("runs", []):
        rules_index = {
            rule["id"]: rule
            for rule in run.get("tool", {}).get("driver", {}).get("rules", [])
        }

        for result in run.get("results", []):
            rule_id = result.get("ruleId", "unknown")
            rule_info = rules_index.get(rule_id, {})

            # Extraire la localisation
            location = {}
            if result.get("locations"):
                loc = result["locations"][0].get("physicalLocation", {})
                location = {
                    "file": loc.get("artifactLocation", {}).get("uri", ""),
                    "line": loc.get("region", {}).get("startLine", 0),
                    "snippet": loc.get("region", {}).get("snippet", {}).get("text", ""),
                }

            # Extraire la sévérité
            level = result.get("level", "warning")
            severity_map = {"error": "CRITIQUE", "warning": "HAUTE", "note": "MOYENNE"}
            severity = severity_map.get(level, "INCONNUE")

            # Extraire les métadonnées métier
            properties = rule_info.get("properties", {})
            metadata = {
                "business_rule": properties.get("business_rule", ""),
                "domain": properties.get("domain", ""),
                "category": properties.get("category", ""),
            }

            finding = {
                "rule_id": rule_id,
                "severity": severity,
                "message": result.get("message", {}).get("text", ""),
                "file": location.get("file", ""),
                "line": location.get("line", 0),
                "snippet": location.get("snippet", ""),
                "metadata": metadata,
            }
            findings.append(finding)

    # Regrouper par sévérité
    by_severity = {
        "CRITIQUE": [f for f in findings if f["severity"] == "CRITIQUE"],
        "HAUTE": [f for f in findings if f["severity"] == "HAUTE"],
        "MOYENNE": [f for f in findings if f["severity"] == "MOYENNE"],
    }

    # Regrouper par domaine
    by_domain = {}
    for f in findings:
        domain = f["metadata"].get("domain") or "general"
        by_domain.setdefault(domain, []).append(f)

    output = {
        "source": "semgrep",
        "total_findings": len(findings),
        "by_severity": {k: len(v) for k, v in by_severity.items()},
        "by_domain": {k: len(v) for k, v in by_domain.items()},
        "findings": findings,
    }

    return output


def main():
    if len(sys.argv) < 2:
        print("Usage: parse_semgrep_findings.py <semgrep.sarif> [output.json]")
        sys.exit(1)

    sarif_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "semgrep-findings.json"

    data = parse_sarif(sarif_path)

    Path(output_path).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Semgrep : {data['total_findings']} violation(s) détectée(s)")
    for severity, count in data["by_severity"].items():
        if count:
            print(f"  {severity} : {count}")
    for domain, count in data["by_domain"].items():
        if count:
            print(f"  Domaine {domain} : {count}")

    print(f"Résultats écrits dans : {output_path}")


if __name__ == "__main__":
    main()
