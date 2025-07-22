import json
import os
import random

# --- Constants ---

dateFilterTypes = [
    { "condition": "BETWEEN", "data": "01 Jan 2021_31 Dec 2021" },
    { "condition": "AFTER", "date": "01 Jan 2022" },
    { "condition": "BEFORE", "date": "01 Jan 2021" },
    { "condition": "BETWEEN", "data": "15 Feb 2023_15 Mar 2023" },
    { "condition": "AFTER", "date": "01 Jun 2024" },
    { "condition": "BEFORE", "date": "31 Dec 2020" },
    { "condition": "BETWEEN", "data": "01 Apr 2025_30 Apr 2025" },
    { "condition": "AFTER", "date": "20 Jul 2025" },
]

# --- Load templates grouped by condition ---

def load_clean_templates(folder_path):
    templates_by_condition = {
        "BETWEEN": [],
        "AFTER": [],
        "BEFORE": []
    }

    for fname in os.listdir(folder_path):
        lower = fname.lower()
        cond = None

        if "between" in lower:
            cond = "BETWEEN"
        elif "after" in lower:
            cond = "AFTER"
        elif "before" in lower:
            cond = "BEFORE"

        if cond is None:
            continue

        full_path = os.path.join(folder_path, fname)
        try:
            with open(full_path, encoding="utf-8") as f:
                templates = json.load(f)
                for template in templates:
                    cleaned = template.strip()
                    if cleaned and '{' in cleaned and '}' in cleaned:
                        templates_by_condition[cond].append(cleaned)
        except json.JSONDecodeError as e:
            print(f"⚠️ Skipping file {fname} due to JSON error: {e}")
        except Exception as e:
            print(f"⚠️ Skipping file {fname} due to unexpected error: {e}")

    return templates_by_condition

# --- Example generation: one per template ---

def generate_examples_once_per_template(templates_by_condition):
    examples = []
    for cond, templates in templates_by_condition.items():
        # pick only matching filters
        valid_filters = [f for f in dateFilterTypes if f["condition"] == cond]

        for template in templates:
            filt = random.choice(valid_filters)
            schema = {
                "lastModified": [],
                "lastAccessed": [],
                "moved": [],
                "selectedFileTypes": [],
                "fileExtensions": [],
                "fileSizes": [],
                "fileGroups": [],
                "fileOwners": [],
                "directoryName": [],
                "filterTags": {
                    "condition": None,
                    "tags": []
                },
                "exclusions": [],
                "includeMoveData": True
            }

            # randomly choose a field
            field = random.choice(["lastModified", "lastAccessed", "moved"])
            try:
                if cond == "BETWEEN":
                    start, end = filt["data"].split("_")
                    val_str = f"{start} and {end}"
                    schema[field].append({ "condition": cond, "data": filt["data"] })
                    input_text = template.format(**{"from": start, "to": end, "val_str": val_str})
                else:
                    date = filt["date"]
                    schema[field].append({ "condition": cond, "date": date })
                    input_text = template.format(val_str=date)

                examples.append({
                    "input": input_text,
                    "output": schema
                })
            except Exception as e:
                print(f"⚠️ Skipping template due to error: {e}")

    return examples

# --- Run everything ---

date_template_dir = "./raw_train_json"
date_templates_by_condition = load_clean_templates(date_template_dir)
all_examples = generate_examples_once_per_template(date_templates_by_condition)

# --- Save output ---

output_path = "date_templates_one_per_template.jsonl"
with open(output_path, "w") as f:
    for ex in all_examples:
        f.write(json.dumps(ex) + "\n")

print(f"✅ Generated {len(all_examples)} examples and saved to {output_path}")
