import humps

from pydantic import BaseModel, ConfigDict


def to_dnd_case(string: str) -> str:
    """
    A slightly more elegant method than just handling each value on its own.
    Not quite pascal case, not quite camel, sort of in between; Mostly just
    special handling for the attributes keys and a few accronym based vals
    like "MaxHP", which isn't really any case

    :param string:
    :return: string
    """
    if string == "max_hp":
        return "MaxHP"
    if 2 <= len(string) <= 3:
        # Attribute (STR, DEX, etc), will be all caps (or AC)
        return string.upper()

    return humps.pascalize(string)


class DNDModel(BaseModel):
    """
    Mainly just a config set up to handle the keys parsed from a dnd beyond
    character sheet, which don't conform to any one standard casing
    """

    model_config = ConfigDict(
        alias_generator=to_dnd_case,
        populate_by_name=True,
    )
