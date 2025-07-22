import json
import random
from datetime import datetime
import os


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


fileSizeFilterTypes = [
    { "condition": "LESS_THAN", "data": "200K" },
    { "condition": "BETWEEN", "data": "5M_10M" },
    { "condition": "IS", "data": "1G" },
    { "condition": "GREATER_THAN_EQUAL", "data": "1024B" },
    { "condition": "GREATER_THAN", "data": "512M" },
]

stringPatternFilterTypes = [
    { "condition": "STARTS_WITH", "data": "abc" },
    { "condition": "CONTAINS", "data": "xyz" },
    { "condition": "IS", "data": "xyz" },
    { "condition": "ENDS_WITH", "data": "xyz" },
]

filterEnums = [
    "DIRECTORY_NAME",
    "FILE_NAME",
    "FILE_LAST_MODIFIED",
    "FILE_LAST_ACCESSED",
    "FILE_MOVED",
    "FILE_CATEGORY",
    "FILE_EXTENSION",
    "FILE_SIZE",
    "FILE_GROUP",
    "FILE_OWNER",
    "TAGS",
]

# Load date templates from files and organize by condition

def load_clean_templates(folder_path):
    templates_by_condition = {
        "BETWEEN": [],
        "AFTER": [],
        "BEFORE": []
    }

    for fname in os.listdir(folder_path):
        lower = fname.lower()
        if "between" in lower:
            cond = "BETWEEN"
        elif "after" in lower:
            cond = "AFTER"
        elif "before" in lower:
            cond = "BEFORE"
        else:
            continue

        with open(os.path.join(folder_path, fname)) as f:
            try:
                templates = json.load(f)  # Load as a list
                for template in templates:
                    cleaned = template.strip()
                    if cleaned and '{' in cleaned and '}' in cleaned:
                        templates_by_condition[cond].append(cleaned)
            except json.JSONDecodeError as e:
                print(f"⚠️ Could not parse {fname} as JSON: {e}")


    return templates_by_condition

date_template_dir = "server/raw_train_json"
date_templates_by_condition = load_clean_templates(date_template_dir)

# [DO NOT REMOVE] will use these later after creating example templates for them

# size_templates = [
#     "files {cond_str} size {val_str}",
#     "files with size {cond_str} {val_str}",
# ]

# string_templates = [
#     "files where the group {cond_str} '{val_str}'",
#     "owned by users whose name {cond_str} '{val_str}'",
#     "in directories that {cond_str} '{val_str}'",
# ]

# tag_templates = [
#     "files tagged with '{val_str}'",
#     "files having tag '{val_str}'"
# ]

# exclusion_templates = [
#     "exclude {val_str} from results",
#     "omit {val_str} filter",
# ]

def generate_query_and_schema():
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

    nl_parts = []

    # --- Date Filter ---
    field = random.choice(["lastModified", "lastAccessed", "moved"])
    filt = random.choice(dateFilterTypes)
    if "data" in filt:
        start, end = filt["data"].split("_")
        cond = "BETWEEN"
        # from_str = ts_to_date(start)
        # to_str = ts_to_date(end)
        val_str = f"{start} and {end}"
        schema[field].append({ "condition": cond, "data": filt["data"] })
        template = random.choice(date_templates_by_condition[cond])
        nl_parts.append(template.format(**{"from": start, "to": end, "val_str": val_str}))
    else:
        ts = filt["date"]
        cond = filt["condition"]
        schema[field].append({ "condition": cond, "date": ts })
        template = random.choice(date_templates_by_condition[cond])
        nl_parts.append(template.format(val_str=ts))


    # [DO NOT REMOVE] will use these later after creating example templates for them

    # # --- File Size ---
    # filt = random.choice(fileSizeFilterTypes)
    # cond_str = filt["condition"].replace("_", " ").lower()
    # val_str = filt["data"].replace("_", " to ")
    # schema["fileSizes"].append(filt)
    # nl_parts.append(random.choice(size_templates).format(cond_str=cond_str, val_str=val_str))

    # # --- String Pattern (one or more)
    # field = random.choice(["fileGroups", "fileOwners", "directoryName"])
    # filt = random.choice(stringPatternFilterTypes)
    # cond_str = filt["condition"].replace("_", " ").lower()
    # val_str = filt["data"]
    # schema[field].append(filt)
    # nl_parts.append(random.choice(string_templates).format(cond_str=cond_str, val_str=val_str))

    # # --- Tags
    # tags = random.sample(["important", "archive", "confidential", "backup"], k=2)
    # schema["filterTags"]["condition"] = "IN"
    # schema["filterTags"]["tags"] = tags
    # nl_parts.append(random.choice(tag_templates).format(val_str=", ".join(tags)))

    # # --- Exclusions
    # ex = random.sample(filterEnums, k=2)
    # schema["exclusions"] = ex
    # nl_parts.append(random.choice(exclusion_templates).format(val_str=", ".join(ex).replace("_", " ").lower()))

    # # --- File types
    # schema["selectedFileTypes"] = random.sample([".txt", ".pdf", ".docx"], k=2)
    # nl_parts.append(f"limit to {', '.join(schema['selectedFileTypes'])} files")

    # Final NL
    natural_query = " ".join(nl_parts)

    return {
        "input": natural_query,
        "output": schema
    }

# Generate multiple
examples = [generate_query_and_schema() for _ in range(1000)]

# Save as .jsonl
with open("date_templates_schema_dataset.jsonl", "w") as f:
    for ex in examples:
        f.write(json.dumps(ex) + "\n")

print("✅ 1000 query-schema pairs written to 'dates_templates_schema_dataset_new.jsonl'")
