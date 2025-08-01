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
