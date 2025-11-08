# recipe_finder.py
# Simple ingredient-based recipe finder for a small hackathon submission.
# Usage:
#  - Run: python recipe_finder.py   (then follow prompts)
#  - Or: python recipe_finder.py eggs,milk,tomato  (comma-separated ingredients as argument)
#
# The script contains a small sample recipe database. It matches recipes by ingredient overlap
# and prints full and partial matches sorted by match percentage.
import sys
import json
from typing import List, Dict, Tuple

SAMPLE_RECIPES = [
    {"name": "Pancakes", "ingredients": ["flour","milk","egg","baking powder","salt","butter"]},
    {"name": "Omelette", "ingredients": ["egg","salt","pepper","butter","onion"]},
    {"name": "Tomato Pasta", "ingredients": ["pasta","tomato","garlic","olive oil","salt","basil"]},
    {"name": "Grilled Cheese", "ingredients": ["bread","cheese","butter"]},
    {"name": "Veggie Salad", "ingredients": ["lettuce","tomato","cucumber","olive oil","salt","lemon"]},
    {"name": "French Toast", "ingredients": ["bread","egg","milk","butter","cinnamon"]},
]

def normalize(ing: str) -> str:
    return ing.strip().lower()

def parse_input(arg: str) -> List[str]:
    parts = [p.strip() for p in arg.split(",") if p.strip()]
    return [normalize(p) for p in parts]

def score_recipe(available: List[str], recipe: Dict) -> Tuple[float, int, int]:
    r_ings = [normalize(i) for i in recipe["ingredients"]]
    available_set = set(available)
    matched = sum(1 for i in r_ings if i in available_set)
    total = len(r_ings)
    score = matched / total if total else 0.0
    return score, matched, total

def find_matches(available: List[str], recipes: List[Dict]) -> Dict:
    full = []
    partial = []
    for r in recipes:
        score, matched, total = score_recipe(available, r)
        entry = {"name": r["name"], "matched": matched, "total": total, "score": round(score,3), "missing": total-matched, "ingredients": r["ingredients"]}
        if matched == total:
            full.append(entry)
        elif matched > 0:
            partial.append(entry)
    # sort partial by score desc, then matched desc
    partial.sort(key=lambda x: (-x["score"], -x["matched"], x["name"]))
    full.sort(key=lambda x: (-x["score"], -x["matched"], x["name"]))
    return {"full_matches": full, "partial_matches": partial}

def pretty_print(result: Dict):
    print("\n=== Full matches (you can fully make these) ===")
    if result["full_matches"]:
        for r in result["full_matches"]:
            print(f'- {r["name"]} (matches: {r["matched"]}/{r["total"]})')
    else:
        print("No full matches found.")
    print("\n=== Partial matches (ranked) ===")
    if result["partial_matches"]:
        for r in result["partial_matches"]:
            pct = int(r["score"]*100)
            print(f'- {r["name"]}: {pct}% ({r["matched"]}/{r["total"]}) -- missing {r["missing"]} ingredient(s)')
            print(f'    Ingredients: {", ".join(r["ingredients"])}')
    else:
        print("No partial matches found.")

def main():
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
        available = parse_input(user_input)
    else:
        raw = input("Enter your available ingredients (comma-separated), e.g. eggs,milk,tomato:\n> ")
        available = parse_input(raw)
    if not available:
        print("No ingredients provided. Exiting.")
        return
    print(f"Available (normalized): {', '.join(available)}")
    result = find_matches(available, SAMPLE_RECIPES)
    pretty_print(result)

if __name__ == '__main__':
    main()
