ERROR_MESSAGES = {
    "ERR 100": "Authentication failed",
    "ERR 101": "Operation is invalid or unknown",
    "ERR 102": "One or more required fields are empty",
    "ERR 103": "Not enough credit for this operation",
    "ERR 104": "Webservice token is not available",
    "ERR 105": "Webservice token not enabled for this user",
    "ERR 106": "Webservice token not allowed from this IP address",
    "ERR 200": "Send message failed",
    "ERR 201": "Destination number or message is empty",
    "ERR 400": "No delivery status available",
    "ERR 401": "No delivery status — SMS still in queue",
    "ERR 402": "No delivery status — SMS already processed from queue",
    "ERR 501": "No data returned or result is empty",
    "ERR 600": "Admin authentication failed",
    "ERR 601": "Inject message failed",
    "ERR 602": "Sender ID or message is empty",
    "ERR 603": "Account addition failed due to missing data",
    "ERR 604": "Failed to add account",
    "ERR 605": "Account removal failed — unknown username",
    "ERR 606": "Failed to remove account",
    "ERR 607": "Set parent failed due to unknown username",
    "ERR 608": "Failed to set parent",
    "ERR 609": "Get parent failed due to unknown username",
    "ERR 610": "Failed to get parent",
    "ERR 611": "Account ban failed due to unknown username",
    "ERR 612": "Failed to ban account",
    "ERR 613": "Account unban failed due to unknown username",
    "ERR 614": "Failed to unban account",
    "ERR 615": "Editing account preferences failed due to missing data",
    "ERR 616": "Failed to edit account preferences",
    "ERR 617": "Editing account configuration failed due to missing data",
    "ERR 618": "Failed to edit account configuration",
    "ERR 619": "Viewing credit failed due to missing data",
    "ERR 620": "Failed to view credit",
    "ERR 621": "Adding credit failed due to missing data",
    "ERR 622": "Failed to add credit",
    "ERR 623": "Deducting credit failed due to missing data",
    "ERR 624": "Failed to deduct credit",
    "ERR 625": "Setting login key failed due to missing data",
    "ERR 626": "Failed to set login key",
}

class JunubSMSError(Exception):
    #Raised when the API returns an error code

    def __init__(self, code: str, message: str = ""):
        self.code = code
        self.message = message or ERROR_MESSAGES.get(code, "Unknown error")
        super().__init__(f"{self.code}: {self.message}")