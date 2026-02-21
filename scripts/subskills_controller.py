#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import argparse
from pathlib import Path

# Path configuration
PROJECT_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
SKILLS_DIR = PROJECT_ROOT.parent / "skills"
CACHE_PATH = PROJECT_ROOT / ".subskills_cache.json"

def run_script(script_name, args):
    cmd = [sys.executable, str(SCRIPTS_DIR / script_name)] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.returncode

def load_cache():
    if CACHE_PATH.exists():
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)

def orchestrate(objective):
    print(f"--- SKILL ORCHESTRATOR: KNOWLEDGE CACHE ACTIVE ---")
    print(f"Objective: {objective}")
    
    cache = load_cache()
    discovered_skills = []
    
    # 1. CACHE RECALL (CACHE CHECK)
    if objective in cache:
        print("\n[PHASE 0: CACHE RECALL - Match found in local library]")
        discovered_skills = cache[objective]
        for skill in discovered_skills:
            print(f"  ✨ Identified: {skill}")
    else:
        # 2. DISCOVERY PHASE
        keywords = objective.lower().split()
        print("\n[PHASE 1: DISCOVERY]")
        search_terms = keywords[:3] 
        
        for term in search_terms:
            if len(term) < 3: continue
            out, code = run_script("skill_search.py", [term, "--dir", str(SKILLS_DIR)])
            if "Found" in out:
                for line in out.splitlines():
                    if line.startswith("- "):
                        skill_name = line.split("(")[0].strip("- ").strip()
                        if skill_name not in discovered_skills:
                            discovered_skills.append(skill_name)
                            print(f"  ✅ Found: {skill_name}")

        # 3. GENERATION PHASE (FALLBACK)
        if not discovered_skills:
            print("\n[PHASE 2: GENERATION - Fallback triggered]")
            new_skill_name = "-".join(keywords[:2])
            print(f"  🔨 Generating new skill: {new_skill_name}")
            out, code = run_script("skill_forge.py", [new_skill_name, objective, "--dir", str(SKILLS_DIR)])
            discovered_skills.append(new_skill_name)
            print(f"  ✅ {out.strip()}")

        # Update Cache
        cache[objective] = discovered_skills
        save_cache(cache)

    # 4. DISPATCH PREP (MANIFEST GENERATION)
    manifest_path = PROJECT_ROOT / ".manifest.json"
    manifest = {
        "required_skills": discovered_skills,
        "execution_brief": objective
    }
    
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print("\n--- SEQUENCE COMPLETE ---")
    print(f"STATUS: SUCCESS")
    print(f"MANIFEST_PATH: {manifest_path}")
    print(f"SUMMARY: Prepared {len(discovered_skills)} skills via Knowledge Cache.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deterministic SubSkills Orchestrator with Persistent Skill Cache.")
    parser.add_argument("objective", help="The complex task to execute")
    args = parser.parse_args()

    orchestrate(args.objective)
