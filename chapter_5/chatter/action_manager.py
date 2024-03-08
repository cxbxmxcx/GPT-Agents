import ast
import functools
import importlib.util
import inspect
import os


def agent_action(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    # Inspect the function's signature
    sig = inspect.signature(func)
    params = sig.parameters.values()

    # Construct properties and required fields
    properties = {}
    required = []
    for param in params:
        # Determine if the parameter has a default value
        if param.default is inspect.Parameter.empty:
            required.append(param.name)
            properties[param.name] = {
                "type": "string",  # Default type for demonstration; could be enhanced to infer actual type
                "description": param.name,  # Placeholder description; could be enhanced with actual docstrings
            }
        else:
            # Enum handling for specific cases (like 'unit' in your example)
            if param.name == "unit":
                properties[param.name] = {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                }
            else:
                properties[param.name] = {
                    "type": "string",  # As above, simplified type handling
                    "description": param.name,  # Placeholder description
                }

    # Construct the OpenAI function specification
    func_spec = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        },
    }

    # If the function is a semantic function, add the prompt template from the docstring
    if "{{" in func.__doc__ and "}}" in func.__doc__:
        prompt_template = func.__doc__
        wrapper._prompt_template = prompt_template

    wrapper._agent_action = func_spec
    return wrapper


# class ActionManager:
#     def __init__(self):
#         self.actions_folder = os.path.join(os.path.dirname(__file__), "actions")
#         self.actions = self.collect_actions_from_folder(self.actions_folder)

#     def add_action(self, action):
#         """Manually add a function specification."""
#         self.actions.append(action)

#     def get_actions(self):
#         """Retrieve all stored function specifications."""
#         return self.actions

#     def collect_actions_from_folder(self, folder_path):
#         """Search and collect function specifications from Python files in the given folder."""
#         for root, dirs, files in os.walk(folder_path):
#             for file in files:
#                 if file.endswith(".py"):
#                     full_path = os.path.join(root, file)
#                     with open(full_path, "r", encoding="utf-8") as f:
#                         file_contents = f.read()
#                     self.actions.extend(
#                         self.inspect_file_for_decorated_actions(file_contents)
#                     )

#     def inspect_file_for_decorated_actions(self, file_contents):
#         """Inspect file contents for functions decorated with `agent_action`."""
#         tree = ast.parse(file_contents)
#         decorated_actions = []

#         for node in ast.walk(tree):
#             if isinstance(node, ast.FunctionDef):
#                 for decorator in node.decorator_list:
#                     if ((isinstance(decorator, ast.Name) and decorator.id == "agent_action") or
#                         (isinstance(decorator, ast.Attribute) and decorator.attr == "agent_action")):
#                         decorated_actions.append({"name": node.name, "pointer": None})  # Placeholder for function pointer
#         return decorated_actions

#     def load_function(self, module_path, function_name):
#         """Dynamically load a function from a given module path."""
#         spec = importlib.util.spec_from_file_location("module.name", module_path)
#         module = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(module)
#         return getattr(module, function_name)

#     def update_function_pointers(self):
#         """Update the function pointers for all detected decorated actions."""
#         for root, dirs, files in os.walk(self.actions_folder):
#             for file in files:
#                 if file.endswith('.py'):
#                     full_path = os.path.join(root, file)
#                     with open(full_path, 'r', encoding='utf-8') as f:
#                         file_contents = f.read()
#                     decorated_actions = self.inspect_file_for_decorated_actions(file_contents)
#                     for action in decorated_actions:
#                         action["pointer"] = self.load_function(full_path, action["name"])


class ActionManager:
    def __init__(self):
        self.actions = []  # Initialize an empty list to store actions
        self.actions_folder = os.path.join(os.path.dirname(__file__), "actions")
        self.collect_and_update_actions()

    def add_action(self, action):
        """Manually add a function specification."""
        self.actions.append(action)

    def get_actions(self):
        """Retrieve all stored function specifications."""
        return self.actions

    def collect_and_update_actions(self):
        """Collect and update actions with function pointers from Python files in the specified folder."""
        self.actions = []  # Reset actions list to ensure it's fresh on each call
        for root, dirs, files in os.walk(self.actions_folder):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    with open(full_path, "r", encoding="utf-8") as f:
                        file_contents = f.read()
                    self.actions.extend(
                        self.inspect_file_for_decorated_actions(
                            file_contents, full_path
                        )
                    )

    def inspect_file_for_decorated_actions(self, file_contents, full_path):
        """Inspect file contents for functions decorated with `agent_action` and load them."""
        tree = ast.parse(file_contents)
        decorated_actions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for decorator in node.decorator_list:
                    if (
                        isinstance(decorator, ast.Name)
                        and decorator.id == "agent_action"
                    ) or (
                        isinstance(decorator, ast.Attribute)
                        and decorator.attr == "agent_action"
                    ):
                        # Dynamically load the function and update the action with its pointer
                        function_pointer = self.load_function(full_path, node.name)
                        decorated_actions.append(
                            {
                                "name": node.name,
                                "pointer": function_pointer,
                                "agent_action": getattr(
                                    function_pointer, "_agent_action", None
                                ),
                                "prompt_template": getattr(
                                    function_pointer, "_prompt_template", None
                                ),
                            }
                        )
        return decorated_actions

    def load_function(self, module_path, function_name):
        """Dynamically load a function from a given module path."""
        spec = importlib.util.spec_from_file_location("module.name", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, function_name)
