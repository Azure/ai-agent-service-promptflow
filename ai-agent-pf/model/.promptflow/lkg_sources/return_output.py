from promptflow import tool

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need

# In Python tool you can do things like calling external services or
# pre/post processing of data, pretty much anything you want


@tool
def echo(node1_result: str, node2_result: str, node3_result: str) -> str:
    if node1_result is not None:
        return "final_result:" + node1_result
    else:
        return "final_result:" + node2_result
    
    