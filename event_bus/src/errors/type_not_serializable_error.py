class TypeNotSerializableError(TypeError):
    def __init__(self, obj: str):
        super().__init__(f"Object {obj} is not JSON serializable.")
