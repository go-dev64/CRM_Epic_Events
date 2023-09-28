from crm.models.element_administratif import Contract
from crm.view.generic_view import GenericView


class ManagerView:
    def __init__(self) -> None:
        self.generic_view = GenericView()

    def get_info_contract_view(
        self, department: str, current_user_name: str, section: str = "Create New Contract/Get Information"
    ) -> dict:
        """
        Function used to get information contract.
        The customer of contract will be get in other function.

        Args:
            department (str): Department of user connected to display in header.
            current_user_name (str): User connected name to display in header.
            section (str, optional): Section information to display in header.Defaults to:
            "Create New Contract/Get Information".

        Returns:
            dict: Dictionnary with contract information : {
                "total_amount": int, "remaning": int, "contract_singed":bool
                }
        """
        contract_info = {}
        restrictions = [
            x for x in Contract().availables_attribue_list() if x.get("attribute_name") not in ["customer"]
        ]
        self.generic_view.header(department=department, current_user=current_user_name, section=section)
        for restriction in restrictions:
            attribute_name = restriction["attribute_name"]
            if restriction["parametre"]["type"] == str:
                contract_info[attribute_name] = self.generic_view.string_form(restriction=restriction)
            elif restriction["parametre"]["type"] == int:
                contract_info[attribute_name] = self.generic_view.integer_form(restriction=restriction)
            elif restriction["parametre"]["type"] == bool:
                contract_info[attribute_name] = self.generic_view.bool_form(restriction=restriction)
        return contract_info

    def get_new_value_of_collaborator_attribute(self, restriction):
        pass

    def get_new_value_of_contract_attribute(self, restriction):
        pass
