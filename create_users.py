import json, urllib.request, urllib.error
API_KEY = "AIzaSyB_4aAZBxQbdAH5BsWnIk9-5-zSr0hwHc4"
users = [
    ("joao@cybhor.com", "user123"),
    ("lisboa@cybhor.com", "user456"),
    ("cristofer@cybhor.com", "user789"),
    ("lopes@cybhor.com", "Admin000"),
]

for email, password in users:
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            print(email, "OK", body.get("localId"))
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8")
        if err.code == 400 and "EMAIL_EXISTS" in body:
            print(email, "EXISTS")
        else:
            print(email, "ERROR", err.code, body)
