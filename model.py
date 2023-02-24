import datetime


class Todo:
    def __init__(self, namespace, deploy, version, 
                 date_added=None, date_match=None,
                 status=None, position=None):
        self.namespace= namespace
        self.deploy = deploy
        self.version = version
        self.date_added = date_added if date_added is not None else datetime.datetime.now().isoformat()
        self.date_match = date_match if date_match is not None else None
        self.status = status if status is not None else 1  # 1 = open, 2 = match
        self.position = position if position is not None else None

    def __repr__(self) -> str:
        return f"({self.namespace}, {self.deploy}, {self.version}, {self.date_added}, {self.date_match}, {self.status}, {self.position})"