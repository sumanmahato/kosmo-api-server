from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from app.schemas.query_schema import QueryParams

parser = PydanticOutputParser(pydantic_object=QueryParams)

EXAMPLES = """
Example 1:
User: "Find cold data from last 3 months"
Output:
{"tier": "cold", "volume": null, "date_range": "last_3_months"}

Example 2:
User: "Get hot data from volume ABC older than 5 years"
Output:
{"tier": "hot", "volume": "ABC", "date_range": "more_than_5_years_ago"}

Example 3:
User: "Retrieve archive tier data for volume X in the last month"
Output:
{"tier": "archive", "volume": "X", "date_range": "last_month"}
"""

query_prompt = PromptTemplate(
    template="""
Convert the following user request into a JSON object matching this schema:
{format_instructions}



User input:
{query}
""",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)


get_parser = lambda: parser

#  Only return a FLAT JSON object matching the schema. Do NOT wrap it inside another object like {{ "query": {{ ... }} }}.