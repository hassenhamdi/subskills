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
MANIFEST_PATH = PROJECT_ROOT / ".manifest.json"

def run_command(cmd):
    """Executes a shell command and captures output."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout, 0
    except subprocess.CalledProcessError as e:
        return e.stderr, e.returncode

def load_cache():
    if CACHE_PATH.exists():
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)

def orchestrate(objective):
    # 1. DISCOVERY / GENERATION PHASE
    cache = load_cache()
    discovered_skills = []
    
    if objective in cache:
        discovered_skills = cache[objective]
    else:
        # Robust Text Search
        keywords = objective.lower().split()
        search_terms = keywords[:3]
        for term in search_terms:
            if len(term) < 3: continue
            # Call internal search script logic directly or via subprocess
            out, code = run_command([sys.executable, str(SCRIPTS_DIR / "skill_search.py"), term, "--dir", str(SKILLS_DIR)])
            if "Found" in out:
                for line in out.splitlines():
                    if line.startswith("- "):
                        skill_name = line.split("(")[0].strip("- ").strip()
                        if skill_name not in discovered_skills:
                            discovered_skills.append(skill_name)

        # Fallback to Generation
        if not discovered_skills:
            new_skill_name = "-".join(keywords[:2])
            out, code = run_command([sys.executable, str(SCRIPTS_DIR / "skill_forge.py"), new_skill_name, objective, "--dir", str(SKILLS_DIR)])
            discovered_skills.append(new_skill_name)

        # Record in Cache
        cache[objective] = discovered_skills
        save_cache(cache)

    # 2. MANIFEST GENERATION
    manifest = {
        "required_skills": discovered_skills,
        "execution_brief": objective
    }
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)

    # 3. DYNAMIC EXECUTOR ACTIVATION
    # We use the 'gemini hire' command to launch the executor subagent.
    # The prompt instructs it to use the manifest we just created.
    executor_prompt = f"MANIFEST_PATH: {MANIFEST_PATH}"
    
    # We use 'gemini hire' to start the subagent session.
    # Note: We use '--non-interactive' to ensure it returns the final report to the script.
    hire_cmd = [
        "gemini", "hire", "dynamic-executor", 
        "--prompt", executor_prompt,
        "--non-interactive"
    ]
    
    report, exit_code = run_command(hire_cmd)

    # 4. FINAL REPORTING TO MAIN AGENT
    if exit_code == 0:
        print(f"--- SKILL ORCHESTRATION: PIPELINE SUCCESS ---")
        print(f"SUMMARY: Identified {len(discovered_skills)} skills.")
        print(f"EXECUTOR REPORT:\n{report}")
    else:
        print(f"--- SKILL ORCHESTRATION: PIPELINE FAILURE ---")
        print(f"ERROR: Executor failed with code {exit_code}")
        print(f"DETAILS: {report}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deterministic Master Pipeline.")
    parser.add_argument("objective", help="The complex task to execute")
    args = parser.parse_args()

    orchestrate(args.objective)
