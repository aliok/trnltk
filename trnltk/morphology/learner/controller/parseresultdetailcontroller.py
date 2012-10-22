class ParseResultDetailController(object):
    def __init__(self, sessionmanager):
        """
        @type sessionmanager: SessionManager
        """
        self.sessionmanager = sessionmanager

    def get_calculation_context(self, param_parse_result_uuid):
        calculation_context = self.sessionmanager.get_calculation_context(param_parse_result_uuid)
        if not calculation_context:
            raise Exception("No calculation context found for parse result with UUID : {}".format(param_parse_result_uuid))

        return calculation_context

