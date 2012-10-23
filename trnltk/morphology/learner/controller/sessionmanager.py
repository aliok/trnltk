import uuid

class SessionManager(object):
    def __init__(self, session_map):
        self.session_map = session_map

    def put_parse_result_in_session(self, parse_result, calculation_context):
        """
        @type parse_result: MorphemeContainer
        @type calculation_context : dict
        @rtype str
        """
        str_uuid = str(uuid.uuid4())

        self._create_submaps()

        self.session_map['parse_results'][str_uuid] = parse_result
        self.session_map['calculation_contexts'][str_uuid] = calculation_context

        return str_uuid

    def get_parse_result(self, parse_result_uuid):
        return self.session_map['parse_results'][parse_result_uuid]

    def get_calculation_context(self, parse_result_uuid):
        return self.session_map['calculation_contexts'][parse_result_uuid]

    def delete_parse_results(self):
        self.session_map['parse_results'] = {}
        self.session_map['calculation_contexts'] = {}

    def _create_submaps(self):
        if not self.session_map.has_key('parse_results'):
            self.session_map['parse_results'] = {}
        if not self.session_map.has_key('calculation_contexts'):
            self.session_map['calculation_contexts'] = {}
