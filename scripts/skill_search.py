#!/usr/bin/env python3
import os
import sys
import re
import argparse
from pathlib import Path

def search_skills(query, skills_dir):
    """
    Robust text-based skill search.
    Scans SKILL.md files and scores them based on the query.
    """
    query_terms = query.lower().split()
    results = []
    
    # Default to global skills if local not found, or passed arg
    search_path = Path(skills_dir)
    
    if not search_path.exists():
        print(f"Error: Skills directory not found at {search_path}", file=sys.stderr)
        return []

    # --- POTENTIAL GEMINI EMBEDDING INTEGRATION ---
    # if os.environ.get("GEMINI_API_KEY"):
    #     import google.generativeai as genai
    #     # 1. Generate embedding for query
    #     # 2. Compare against pre-computed skill embeddings
    #     # 3. Return semantic matches
    #     pass
    # ---------------------------------------------

    for skill_file in search_path.glob("**/SKILL.md"):
        try:
            content = skill_file.read_text(encoding="utf-8").lower()
            skill_name = skill_file.parent.name
            score = 0
            
            # 1. Exact Name Match (Highest)
            if query.lower() == skill_name.lower():
                score += 100
            
            # 2. Name Partial Match
            if query.lower() in skill_name.lower():
                score += 50
                
            # 3. Terms in Name
            for term in query_terms:
                if term in skill_name.lower():
                    score += 20
            
            # 4. Terms in Content
            matches = 0
            for term in query_terms:
                count = content.count(term)
                if count > 0:
                    matches += 1
                    score += min(count, 5) * 2 # Cap frequency bonus
            
            # Bonus for having all terms
            if matches == len(query_terms):
                score += 30

            if score > 0:
                results.append({
                    "name": skill_name,
                    "path": str(skill_file),
                    "score": score
                })
        except Exception as e:
            continue

    # Sort by score desc
    return sorted(results, key=lambda x: x['score'], reverse=True)[:5] # Top 5

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for skills.")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--dir", default="../skills", help="Skills directory")
    args = parser.parse_args()

    hits = search_skills(args.query, args.dir)
    
    if not hits:
        print("No matching skills found.")
        sys.exit(0)
        
    print(f"Found {len(hits)} skills for '{args.query}':")
    for hit in hits:
        print(f"- {hit['name']} (Score: {hit['score']})")
