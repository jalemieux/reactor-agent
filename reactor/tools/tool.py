import datetime
import platform



class Tool:
    def __init__(self, names, description):
        self._names = names
        self._description = description

    def run(self, **kwargs):
        pass

    def tool_names_and_description(self) -> str:
        return "\n".join([f"{name}: {self._description}" for name in self._names])

    def names(self) -> list[str]:
        return self._names

    def description(self) -> str:
        return self._description

    def definition(self) -> list[dict]:
        pass

    def run(self, action_name, **action_args):
        pass


class FinalAnswer(Tool):
    def __init__(self):
        super().__init__(
            names=["final_answer"],
            description="Provide a concise answer to the user's question",
        )

    def final_answer(self, **kwargs):
        return kwargs

    def run(self, action_name, **action_args):
        if action_name == "final_answer":
            return self.final_answer(**action_args)
        else:
            raise ValueError(f"Invalid action name: {action_name}")

    def definition(self) -> list[dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "final_answer",
                    "description": "Provide a concise answer to the user's question",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "answer": {
                                "type": "string",
                                "description": "The final concise answer to the user's question",
                            },
                        },
                        "required": ["answer"],
                    },
                },
            }
        ]


class CurrentDate(Tool):
    def __init__(self):
        super().__init__(
            names=["current_date"],
            description="Get the current date and time in ISO format (YYYY-MM-DDTHH:MM:SS)",
        )

    def current_date(self, **kwargs):
        return {"datetime": datetime.datetime.now().isoformat()}

    def run(self, action_name, **action_args):
        if action_name == "current_date":
            return self.current_date(**action_args)
        else:
            raise ValueError(f"Invalid action name: {action_name}")

    def definition(self) -> list[dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "current_date",
                    "description": "Get the current date and time in ISO format (YYYY-MM-DDTHH:MM:SS)",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            }
        ]

class CodeInterpreter(Tool):
    def __init__(self):
        super().__init__(
            names=["code_interpreter", "execute_code", "run_code"],
            description="Execute Python code and return the results",
        )
        self._execution_globals = {}
        self._execution_locals = {}

    def execute_code(self, code: str, timeout: int = 30) -> dict:
        """
        Execute Python code safely and return the results.
        
        Args:
            code: Python code to execute
            timeout: Maximum execution time in seconds
            
        Returns:
            Dictionary containing execution results, output, and any errors
        """
        import io
        import sys
        import traceback
        from contextlib import redirect_stdout, redirect_stderr
        import ast
        
        result = {
            "success": False,
            "output": "",
            "error": "",
            "return_value": None,
            "execution_time": 0
        }
        
        # Capture stdout and stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        try:
            # Set up timeout handler (only on Unix-like systems)
            if platform.system() != "Windows":
                import signal
                
                def timeout_handler(signum, frame):
                    raise TimeoutError("Code execution timed out")
                
                # Set timeout
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(timeout)
            
            # Execute code with captured output
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                # Check if the code is a single expression
                try:
                    # Try to parse as an expression
                    tree = ast.parse(code, mode='eval')
                    # If successful, it's a single expression - use eval
                    exec_result = eval(code, self._execution_globals, self._execution_locals)
                    result["return_value"] = str(exec_result)
                except SyntaxError:
                    # It's not a single expression, use exec and try to capture last expression
                    # Split the code into lines and execute
                    lines = code.strip().split('\n')
                    last_line = lines[-1].strip()
                    
                    # Execute all lines except the last
                    if len(lines) > 1:
                        exec('\n'.join(lines[:-1]), self._execution_globals, self._execution_locals)
                    
                    # Try to evaluate the last line as an expression
                    try:
                        last_tree = ast.parse(last_line, mode='eval')
                        last_result = eval(last_line, self._execution_globals, self._execution_locals)
                        result["return_value"] = str(last_result)
                    except (SyntaxError, ValueError):
                        # Last line is not an expression, just execute it
                        exec(last_line, self._execution_globals, self._execution_locals)
                    except Exception:
                        # If eval fails, just execute the last line
                        exec(last_line, self._execution_globals, self._execution_locals)
            
            # Get captured output
            result["output"] = stdout_capture.getvalue()
            result["error"] = stderr_capture.getvalue()
            result["success"] = True
            
        except TimeoutError:
            result["error"] = f"Code execution timed out after {timeout} seconds"
        except Exception as e:
            result["error"] = f"Error executing code: {str(e)}\n{traceback.format_exc()}"
        finally:
            # Cancel timeout (only on Unix-like systems)
            if platform.system() != "Windows":
                signal.alarm(0)
        
        return result

    def run(self, action_name, **action_args):
        if action_name in ["code_interpreter", "execute_code", "run_code"]:
            return self.execute_code(**action_args)
        else:
            raise ValueError(f"Invalid action name: {action_name}")

    def definition(self) -> list[dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "execute_code",
                    "description": "Execute Python code and return the results",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "Python code to execute",
                            },
                            "timeout": {
                                "type": "integer",
                                "description": "Maximum execution time in seconds (default: 30)",
                                "default": 30,
                            },
                        },
                        "required": ["code"],
                    },
                },
            }
        ] 
    
    