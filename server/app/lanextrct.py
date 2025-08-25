import langextract as lx
import textwrap

def langextrct(input_list: list):
    prompt = textwrap.dedent("""\
        Extract workflow parameters from user input. The input can contain both 'Human' and 'AI' messages,
        'AI' messages will be responses to the user input asking for more information or giving feedback,
        such messages should be used ONLY to build context about what the user is sending.
        The actual parameters should ONLY be extracted from the user's messages
        The parameters are:
          - workflowServiceClass
          - tagKey
          - displayName
          - queryName
        Use the exact text span from input for extraction_text.
        Each parameter must be a separate extraction.
    """)
    examples = [
        lx.data.ExampleData(
            text="Human: use this PureStorage-cold-data to create a workflow",
            extractions=[
                lx.data.Extraction(
                    extraction_class="queryName",
                    extraction_text="PureStorage-cold-data",
                    attributes={"queryName": "PureStorage-cold-data"},
                ),
            ]
        ),
        lx.data.ExampleData(
            text="Human: use Cold Data 10+ MB to create a workflow for PII detection",
            extractions=[
                lx.data.Extraction(
                    extraction_class="queryName",
                    extraction_text="Cold Data 10+ MB",
                    attributes={"queryName": "Cold Data 10+ MB"},
                ),
                lx.data.Extraction(
                    extraction_class="workflowServiceClass",
                    extraction_text="PII",
                    attributes={"workflowServiceClass": "PII"},
                ),
            ]
        ),
        lx.data.ExampleData(
            text="Human: create a workflow for AMAZON_REKOGNITION",
            extractions=[
                lx.data.Extraction(
                    extraction_class="workflowServiceClass",
                    extraction_text="AMAZON_REKOGNITION",
                    attributes={"workflowServiceClass": "AMAZON_REKOGNITION"},
                ),
            ]
        ),
        lx.data.ExampleData(
            text="Human: create a workflow using PII scanner. AI: It looks like the <b>tag key</b> is missing. Please provide it to move forward. Human: america1",
            extractions=[
                lx.data.Extraction(
                    extraction_class="workflowServiceClass",
                    extraction_text="PII",
                    attributes={"workflowServiceClass": "PII"},
                ),
                lx.data.Extraction(
                    extraction_class="tagKey",
                    extraction_text="america1",
                    attributes={"tagKey": "america1"},
                ),
            ]
        ),
        lx.data.ExampleData(
            text="Human: create a workflow using B-PENG engg data",
            extractions=[
                lx.data.Extraction(
                    extraction_class="queryName",
                    extraction_text=" B-PENG engg data",
                    attributes={"queryName": " B-PENG engg data"},
                ),
            ]
        ),
        lx.data.ExampleData(
            text="Human: add Department as the tag",
            extractions=[
                lx.data.Extraction(
                    extraction_class="tagKey",
                    extraction_text="Department",
                    attributes={"tagKey": "Department"},
                ),
            ]
        ),
        lx.data.ExampleData(
            text="Human: tag my PII data as mgmt",
            extractions=[
                lx.data.Extraction(
                    extraction_class="workflowServiceClass",
                    extraction_text="PII",
                    attributes={"workflowServiceClass": "PII"},
                ),
                lx.data.Extraction(
                    extraction_class="tagKey",
                    extraction_text="mgmt",
                    attributes={"tagKey": "mgmt"},
                ),
            ]
        ),
        lx.data.ExampleData(
            text="Human: name it Finance-Flow",
            extractions=[
                lx.data.Extraction(
                    extraction_class="displayName",
                    extraction_text="Finance-Flow",
                    attributes={"displayName": "Finance-Flow"},
                ),
            ]
        ),
        lx.data.ExampleData(
            text="Human: Create a workflow named HR-Cleanup using Employee-Data with PII detection and add Team as tag",
            extractions=[
                lx.data.Extraction(
                    extraction_class="displayName",
                    extraction_text="HR-Cleanup",
                    attributes={"displayName": "HR-Cleanup"},
                ),
                lx.data.Extraction(
                    extraction_class="queryName",
                    extraction_text="Employee-Data",
                    attributes={"queryName": "Employee-Data"},
                ),
                lx.data.Extraction(
                    extraction_class="workflowServiceClass",
                    extraction_text="PII",
                    attributes={"workflowServiceClass": "PII"},
                ),
                lx.data.Extraction(
                    extraction_class="tagKey",
                    extraction_text="Team",
                    attributes={"tagKey": "Team"},
                ),
            ]
        ),
    ]
    
    input_text = "\n".join(reversed(input_list))
    
    print("INPYjdkfskjdfbskbgkjsbkjgbsbgjksfgET", input_text)

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



# import langextract as lx
# import textwrap
# from langextract.data import Document


# # def prepare_conversation(history, new_input=None):
# #     """
# #     Convert history (list of dicts) + new input into a list of langextract Documents.
# #     """
# #     docs = []
# #     for turn in history:
# #         role = turn.get("role", "user")
# #         text = turn["content"]
# #         docs.append(Document(
# #             text=text,
# #             additional_context=f"Role: {role}"
# #         ))
    
# #     if new_input:
# #         docs.append(Document(
# #             text=new_input,
# #             additional_context="Role: user"
# #         ))
    
# #     return docs




# def langextrct(input):
#     prompt = textwrap.dedent("""\
#         Extract queryName from user input
#         """)

#     # 2. Provide examples (few-shot guidance)
#     examples = [
#         lx.data.ExampleData(
#             text="use this PureStorage-cold-data to create a workflow",
#             extractions=[
#                 lx.data.Extraction(extraction_class="queryName", extraction_text="PureStorage-cold-data", attributes={"queryName":"PureStorage-cold-data"}),
#             ]
#         ),
#         lx.data.ExampleData(
#             text="use Cold Data 10+ MB to create a workflow for PII detection",
#             extractions=[
#                 lx.data.Extraction(extraction_class="queryName", extraction_text="Cold Data 10+ MB", attributes={"queryName":"Cold Data 10+ MB"}),
#             ]
#         ),
#         lx.data.ExampleData(
#             text="Create a workflow for Old NetApp VM's-Move-Cleanup",
#             extractions=[
#                 lx.data.Extraction(extraction_class="queryName", extraction_text="Old NetApp VM's-Move-Cleanup", attributes={"queryName":"Old NetApp VM's-Move-Cleanup"}),
#             ]
#         ),
#     ]

#     # 3. Run extraction
#     result = lx.extract(
#         text_or_documents=input,
#         prompt_description=prompt,
#         examples=examples,
#         language_model_type=lx.inference.OllamaLanguageModel,
#         model_id="mistral",
#         model_url="http://localhost:11434",
#         fence_output=False,          # output not fenced by ```json
#         use_schema_constraints=False # can set True if you want strict schema
#     )

#     # 4. Save + visualize (optional)
#     lx.io.save_annotated_documents([result], output_name="workflow_results.jsonl", output_dir=".")
#     html_content = lx.visualize("workflow_results.jsonl")
#     with open("workflow_visualization.html", "w") as f:
#         f.write(html_content)

#     print(result.extractions)


# langextrct("generate a report for AMAZON 125 GB VMware")