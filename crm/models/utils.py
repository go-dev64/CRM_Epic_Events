class Utils:
    def get_type_of_user(self, user) -> str:
        """
        Return l type of user: "Manager", "Seller" or "Supporter"

        Args:
            user (_type_): Instance User class.

        Returns:
            str: "Manager", "Seller" or "Supporter"
        """
        user_type = type(user).__name__
        return user_type
