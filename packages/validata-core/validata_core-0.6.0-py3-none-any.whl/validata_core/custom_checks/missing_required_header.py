"""Reimplementation of NonMatchingHeader check,
   taking into account missing header, extra header and wrong header order."""
from frictionless import Check, errors


class MissingRequiredHeaderError(errors.HeaderError):
    """Custom error."""

    code = "missing-required-header"
    name = "Colonne obligatoire manquante"
    tags = ["#head", "#structure"]
    template = "{note}"
    description = ""


class MissingRequiredHeader(Check):
    """Custom check."""

    possible_Errors = [MissingRequiredHeaderError]

    def prepare(self):
        """Extract custom params from descriptor.

        schema required fields are provided as task parameter
        We can't use self.table.schema to access to the whole schema as
        `sync_schema=True` remove schema fields that don't appear in table.
        """
        self.__required_field_names = self.get("required_field_names")

    def validate_header(self, header):
        for pos, field_name in enumerate(self.__required_field_names):
            if field_name not in header:
                yield MissingRequiredHeaderError(
                    note=f"La colonne obligatoire `{field_name}` est manquante.",
                    labels=header,
                    row_positions=[pos],
                )

    metadata_profile = {  # type: ignore
        "type": "object",
        "required": ["required_field_names"],
        "properties": {"required_field_names": {"type": "array"}},
    }
