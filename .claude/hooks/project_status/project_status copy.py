from typing import Any, Annotated, NamedTuple
from flatten_dict import flatten, unflatten
from pydantic import BaseModel, StringConstraints, ValidationError


class NestedStatusQuery(BaseModel):
    query: Annotated[str, StringConstraints(pattern=r".+\..+")]


pokemon = {
    "pikachu": {"name": "Pikachu", "type": "Electric", "level": 100},
    "squirtle": {"name": "Squirtle", "type": "Water"},
}


class Project:
    def __init__(self, status_data: dict[str, Any]):
        self._status_data = status_data

    @property
    def status_data(self) -> dict[str, Any]:
        return self._status_data

    @status_data.setter
    def status_data(self, value: dict[str, Any]) -> None:
        self._status = value

    def get_status(self, query: str) -> str | None:
        return self._status_data.get(query, "")

    def set_status(self, query: str, value: Any) -> None:
        self._status_data[query] = value

    def get_nestedstatus(self, query: str) -> str | None:
        status_data = self._status_data
        flattened_data = flatten(status_data, reducer="dot")
        try:
            NestedStatusQuery(query=query)
            return flattened_data.get(query, "")
        except ValidationError:
            print(f"No dot seperator found in query: {query}")
            return None

    def set_nested_status(self, query: str, value: Any) -> None:
        flattened_data = flatten(self._status_data, reducer="dot")
        try:
            NestedStatusQuery(query=query)
            if not query in flattened_data.keys():
                raise KeyError(f"Key {query} not found in status data")
            flattened_data[query] = value
            unflattened_data = unflatten(flattened_data, splitter="dot")
            self._status_data.update(unflattened_data)
        except (ValidationError, KeyError) as e:
            if isinstance(e, KeyError):
                print(f"Key {query} not found in status data")
            else:
                print(f"Error: {e}")

    def get_roadmap(self) -> Any:
        return self.get_status("roadmap")

    def get_phases(self, query: str) -> list[dict[str, Any]]:
        try:
            NestedStatusQuery(query=query)
            return self.get_nested_status(query)
        except ValidationError:
            print(f"No dot seperator found in query: {query}")
            return None


    def set_roadmap(self, value: Any) -> None:
        self.set_status("roadmap", value)

    def set_phases(self, value: list[dict[str, Any]]) -> None:
        self.set_status("phases", value)

    def 


if __name__ == "__main__":
    project = Project(pokemon)
    project.set_status("pikachu", "Raichu")
    print(project.status_data.get("pikachu"))
