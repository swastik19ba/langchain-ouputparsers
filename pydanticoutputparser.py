from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParsers


load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text-generation"
)
model = ChatHuggingFace(llm=llm)

class Person(BaseModel):
    name:str=Field(description='Name of the person')
    age:int =Field(gt=8,description='Age of the person ')
    city=str=Field(description='name of the city the person belongs to')

    parser=PydanticOutputParsers(pydantic_object=Person)

    template=PromptTemplate(
        template='Generate the name,age ,city of a fictional {place} person \n
        {format_instructions} ',
        input_varibales=['place']
        partial_variables={'format_instruction':parser.get_format_instructions()}
    )
    prompt=template.invoke({'place':'indian'})

    model=model.innvoke(prompt)
    final_result=parser.parse(result.content )

    print(final_result)