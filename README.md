# Supported Operations
This SDK provides a Python interface for the JunubSMS Web Services API. The library exposes all major messaging and administration operations available through the platform.

---

## Messaging Operations

### Send Message (`op=pv`)

Send SMS messages to:

- A single mobile number
- Multiple mobile numbers
- A username (`@username`)
- A contact group (`#groupcode`)

Features:

- Custom sender ID
- Unicode messaging support
- Scheduled delivery
- Custom message footer
- Multiple recipients

```python
results = client.messages.send(
    to="0912345678",
    msg="Hello World"
)

print(results[0].ok)
```

---

### Outgoing Messages (`op=ds`)

Retrieve outgoing SMS messages and their delivery statuses.

```python
statuses = client.messages.outgoing()

for sms in statuses:
    print(sms.status)
```

---

### Incoming Messages (`op=in`)

Retrieve incoming SMS messages.

```python
messages = client.messages.incoming()

for msg in messages:
    print(msg.src, msg.msg)
```

---

### Inbox Messages (`op=ix`)

Retrieve SMS messages stored in the user's inbox.

```python
messages = client.messages.inbox()
```

---

### Sandbox Messages (`op=sx`)

Retrieve unhandled incoming SMS messages from the sandbox.

```python
messages = client.messages.sandbox()
```

---

### Credit Information (`op=cr`)

View the current account credit balance.

```python
credit = client.messages.credit()

print(credit.balance)
```

---

### Generate API Token (`op=set_token`)

Generate a new API token for the current account.

```python
new_token = client.messages.set_token()
```

---

### Search Contacts (`op=get_contact`)

Search contacts by:

- Name
- Mobile number
- Email address

```python
contacts = client.messages.get_contacts("John")

for contact in contacts:
    print(contact.p_desc)
```

---

### Search Contact Groups (`op=get_contact_group`)

Search contact groups by:

- Group name
- Group code

```python
groups = client.messages.get_contact_groups("STAFF")
```

---

### Query Account Information (`op=query`)

Retrieve account information, credit details, and SMS statistics.

```python
info = client.messages.query()
```

---

## Administrative Operations

### Inject Incoming SMS (`op=inject`)

Inject a message into the system as a valid incoming SMS.

Useful for testing SMS workflows and applications.

```python
client.admin.inject_message(
    sender="+249123456789",
    msg="TEST MESSAGE",
    receiver="1234",
    smsc="test-smsc"
)
```

---

### Create Account (`op=accountadd`)

Create a new account.

```python
client.admin.add_account(
    username="john",
    password="secret",
    name="John Doe",
    email="john@example.com"
)
```

---

### Remove Account (`op=accountremove`)

Permanently remove an account.

```python
client.admin.remove_account("john")
```

---

### Ban Account (`op=accountban`)

Ban an account from accessing the service.

```python
client.admin.ban_account("john")
```

---

### Unban Account (`op=accountunban`)

Restore access to a banned account.

```python
client.admin.unban_account("john")
```

---

### Update Account Preferences (`op=accountpref`)

Update account information such as:

- Name
- Email
- Mobile number
- Password

```python
client.admin.update_preferences(
    "john",
    email="new@example.com",
    mobile="0912345678"
)
```

---

### Update Account Configuration (`op=accountconf`)

Update account configuration settings such as:

- Sender ID
- Message footer
- Forwarding settings

```python
client.admin.update_config(
    "john",
    sender="MyBrand"
)
```

---

### Set Parent Account (`op=parentset`)

Assign a parent account to a subuser.

```python
client.admin.set_parent(
    username="agent1",
    parent="master_account"
)
```

---

### Get Parent Account (`op=parentget`)

Retrieve the parent account of a subuser.

```python
parent = client.admin.get_parent("agent1")

print(parent)
```

---

### View Credit (`op=creditview`)

Retrieve the credit balance of an account.

```python
balance = client.admin.view_credit("john")

print(balance)
```

---

### Add Credit (`op=creditadd`)

Add credit to an account.

```python
client.admin.add_credit(
    username="john",
    amount=100
)
```

---

### Deduct Credit (`op=creditdeduct`)

Deduct credit from an account.

```python
client.admin.deduct_credit(
    username="john",
    amount=50
)
```

---

### Generate Login Key (`op=loginkeyset`)

Generate a login key for an account.

```python
login_key = client.admin.set_login_key("john")

print(login_key)
```