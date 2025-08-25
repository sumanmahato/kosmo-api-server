import langextract as lx
import textwrap

def get_report_params(input_text: str):
    prompt = textwrap.dedent("""\
        Extract report parameters from user input.
        The parameters are:
          - actionType
          - tagNames
        Use the exact text span from input for extraction_text.
        Donot extract any extra parameters other than (actionType, tagNames)
        Each parameter must be a separate extraction.
    """)
    examples = [
        lx.data.ExampleData(
            text="make a report of all PDF files",
            extractions=[
                lx.data.Extraction(
                    extraction_class="actionType",
                    extraction_text="report",
                    attributes={"actionType": "report"},
                ),
            ]
        ),
        lx.data.ExampleData(
            text="create a report for files tagged with finance, payroll, and confidential",
            extractions=[
                lx.data.Extraction(
                    extraction_class="actionType",
                    extraction_text="report",
                    attributes={"actionType": "report"},
                ),
                lx.data.Extraction(
                    extraction_class="tagNames",
                    extraction_text="finance, payroll, and confidential",
                    attributes={"tagNames": ["finance", "payroll", 'confidential']},
                ),
            ]
        ),
        lx.data.ExampleData(
            text="I need a report for everything under the Archive and Deleted tags",
            extractions=[
                lx.data.Extraction(
                    extraction_class="actionType",
                    extraction_text="report",
                    attributes={"actionType": "report"},
                ),
                lx.data.Extraction(
                    extraction_class="tagNames",
                    extraction_text="Archive and Deleted tags",
                    attributes={"tagNames": ["Archive", "Deleted"]},
                ),
            ]
        ),
        lx.data.ExampleData(
            text="can you prepare a report for files with tag Sensitive and file type exe",
            extractions=[
                lx.data.Extraction(
                    extraction_class="actionType",
                    extraction_text="report",
                    attributes={"actionType": "report"},
                ),
                lx.data.Extraction(
                    extraction_class="tagNames",
                    extraction_text="Sensitive",
                    attributes={"tagNames": ["Sensitive"]},
                ),
            ]
        ),
        lx.data.ExampleData(
            text="create a report for files tagged with New York Office",
            extractions=[
                lx.data.Extraction(
                    extraction_class="actionType",
                    extraction_text="report",
                    attributes={"actionType": "report"},
                ),
                lx.data.Extraction(
                    extraction_class="tagNames",
                    extraction_text="New York Office",
                    attributes={"tagNames": ["New York Office"]},
                ),
            ]
        ),
        lx.data.ExampleData(
            text="make a report for Excel sheets tagged as Finance accessed after Jan 2021",
            extractions=[
                lx.data.Extraction(
                    extraction_class="actionType",
                    extraction_text="report",
                    attributes={"actionType": "report"},
                ),
                lx.data.Extraction(
                    extraction_class="tagNames",
                    extraction_text="Finance",
                    attributes={"tagNames": ["Finance"]},
                ),
            ]
        ),
        lx.data.ExampleData(
            text="get me data tagged as Finance accessed after Jan 2021",
            extractions=[
                lx.data.Extraction(
                    extraction_class="tagNames",
                    extraction_text="Finance",
                    attributes={"tagNames": ["Finance"]},
                ),
            ]
        ),
    ]

    result = lx.extract(
        text_or_documents=input_text,
        prompt_description=prompt,
        examples=examples,
        language_model_type=lx.inference.OllamaLanguageModel,
        model_id="mistral",
        model_url="http://localhost:11434",
        fence_output=False,
        use_schema_constraints=False,
    )

    extracted_dict = {}
    for e in result.extractions:
        extracted_dict.update(e.attributes)

        
    return extracted_dict