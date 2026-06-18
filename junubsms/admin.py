from collections.abc import Set

from .base import BaseResource


class AdminResource(BaseResource):

    #Admin-level API operations.

    def inject_message(self, sender: str, msg: str, receiver: str, smsc: str) -> dict:
        """Inject a message into the system as a valid incoming SMS."""
        return self._get("inject", **{"from": sender}, msg=msg, recvnum=receiver, smsc=smsc)

    #Account management 

    def add_account(
        self,
        username: str,
        password: str,
        name: str,
        email: str,
        status: int = 3,
        mobile: str = "",
        parent: str = "",
    ) -> dict:
        
        #Create a new account.
        return self._get(
            "accountadd",
            data_username=username,
            data_password=password,
            data_name=name,
            data_email=email,
            data_status=status,
            data_mobile=mobile or None,
            data_parent=parent or None,
        )

    def remove_account(self, username: str) -> dict:
        #Permanently remove an account
        return self._get("accountremove", data_username=username)

    def ban_account(self, username: str) -> dict:
        #Ban an account from using the service
        return self._get("accountban", data_username=username)

    def unban_account(self, username: str) -> dict:
        #Remove a ban from an account
        return self._get("accountunban", data_username=username)

    def update_preferences(self, username: str, **fields) -> dict:
        
        #Update account preferences (name, email, mobile, password, etc.).
        #Example: update_preferences("john", name="John Doe", email="j@example.com")
        
        prefixed = {f"data_{k}": v for k, v in fields.items()}
        return self._get("accountpref", data_username=username, **prefixed)

    def update_config(self, username: str, **fields) -> dict:
        
        #Update account configuration (sender, footer, forwarding, etc.).
        #Example: update_config("john", sender="MyBrand", fwd_to_email=1)
        
        prefixed = {f"data_{k}": v for k, v in fields.items()}
        return self._get("accountconf", data_username=username, **prefixed)

    # Parent / subuser

    def set_parent(self, username: str, parent: str) -> dict:
        #Set the parent account for a subuser
        return self._get("parentset", data_username=username, data_parent=parent)

    def get_parent(self, username: str) -> str:
        #Return the parent username for a subuser account
        data = self._get("parentget", data_username=username)
        return data.get("data", {}).get("parent", "")

    # Credit management

    def view_credit(self, username: str) -> str:
        #Return the credit balance for the given account
        data = self._get("creditview", data_username=username)
        return data.get("data", {}).get("balance", "")

    def add_credit(self, username: str, amount: float) -> dict:
        #Add credit to an account
        return self._get("creditadd", data_username=username, data_amount=amount)

    def deduct_credit(self, username: str, amount: float) -> dict:
        #Deduct credit from an account
        return self._get("creditdeduct", data_username=username, data_amount=amount)
    
    # Login key

    def set_login_key(self, username: str) -> str:
        #Generate and return a new login key for an account
        data = self._get("loginkeyset", data_username=username)
        return data.get("data", {}).get("login_key", "")