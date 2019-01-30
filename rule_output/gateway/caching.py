from typing import Union

from rule_output.model import Reconciliation
from rule_output.gateway.development import RuleOutputGateway as PhysicalRuleOutputGateway


class RuleOutputGateway:

    def __init__(self, inner: PhysicalRuleOutputGateway):
        self.inner: PhysicalRuleOutputGateway = inner

    def get_last_active_invoice(self, reconciliation: Reconciliation) -> Union[Reconciliation, bool]:
        return self.inner.get_last_active_invoice(reconciliation)
