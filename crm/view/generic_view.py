class GenericView:
    def display_element_list(self, list_element):
        for i in range(len(list_element)):
            print(f"{i} - {list_element[i]}")

    def display_element(self, list_element):
        element = self.select_element_view(list_element)
        print(element)
        return element

    def select_element_view(self, list_element):
        self.display_element_list(list_element=list_element)
        element_chosen = input
        return element_chosen

    def get_address_info(self):
        pass
