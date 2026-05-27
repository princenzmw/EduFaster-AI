import sys
from io import StringIO
from langchain_core.tools import tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

@tool
def execute_python_code(code: str) -> str:
    """Executes basic Python code and returns the printed output. Use this to verify code examples before teaching them."""
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    
    try:
        exec(code)
        sys.stdout = old_stdout
        output = redirected_output.getvalue()
        if not output:
            return "Code executed successfully, but nothing was printed."
        return output
    except Exception as e:
        sys.stdout = old_stdout
        return f"Error executing code: {str(e)}"

# Instantiate a stable Wikipedia search tool for the educational bot
api_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=1000)
search_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
