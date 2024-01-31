from pyneo4j_ogm import RelationshipModel  # type: ignore


class Default(RelationshipModel):
    class Settings:
        type = "DEFAULT"