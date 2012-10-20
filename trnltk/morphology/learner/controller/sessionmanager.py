import uuid

class SessionManager(object):
    def __init__(self, session_map):
        self.session_map = session_map

    def put_parse_result_in_session(self, parse_result):
        """
        @param parse_result: str or unicode
        @rtype str
        """
        str_uuid = str(uuid.uuid4())
        self.session_map[str_uuid] = parse_result

        return str_uuid