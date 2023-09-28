import pytest
from crm.view.contract_view import ContractView


class TestContractView:
    def test_get_user_info_view(self, mocker):
        # testvalid if dict returned is correct.
        mocker.patch("crm.view.generic_view.GenericView.header")
        contract_restriction = [
            {"attribute_name": "total_amount", "parametre": {"type": int, "max": None}},
            {"attribute_name": "remaining", "parametre": {"type": int, "max": None}},
            {"attribute_name": "signed_contract", "parametre": {"type": bool, "max": None}},
        ]
        mocker.patch(
            "crm.models.element_administratif.Contract.availables_attribue_list", return_value=contract_restriction
        )
        mocker.patch("crm.view.generic_view.GenericView.integer_form", return_value=500)
        mocker.patch("crm.view.generic_view.GenericView.bool_form", return_value=True)
        result = ContractView().get_info_contract(department="", current_user_name="")
        assert result.get("total_amount") == 500
        assert result.get("remaining") == 500
        assert result.get("signed_contract") == True
        assert len(result.keys()) == 3
