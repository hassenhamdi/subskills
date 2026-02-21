#!/usr/bin/env python3
import os
import sys
import json
import argparse
from pathlib import Path

def generate_skill(skill_name, requirements, skills_dir):
    """
    Generates a new skill following standard technical norms.
    """
    skill_path = Path(skills_dir) / skill_name
    skill_path.mkdir(parents=True, exist_ok=True)
    
    md_content = f"""---
name: {skill_name}
description: {requirements[:100]}...
---

# {skill_name.replace('-', ' ').title()}

## Purpose
{requirements}

## Instructions
1. Use this skill when working on tasks related to {skill_name}.
2. Follow the established protocols for this domain.
3. Ensure all changes are verified with tests.

## Reusable Patterns
- Pattern 1: [Placeholder]
- Pattern 2: [Placeholder]

## Verification
- Run: [Test Command Placeholder]
"""
    
    (skill_path / "SKILL.md").write_text(md_content)
    
    # Create standard sub-directories
    (skill_path / "scripts").mkdir(exist_ok=True)
    (skill_path / "tests").mkdir(exist_ok=True)
    
    return str(skill_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a new technical skill.")
    parser.add_argument("name", help="Skill name")
    parser.add_argument("reqs", help="Skill requirements/description")
    parser.add_argument("--dir", default="skills", help="Skills directory")
    args = parser.parse_args()

    path = generate_skill(args.name, args.reqs, args.dir)
    print(f"Skill '{args.name}' successfully generated at {path}")
