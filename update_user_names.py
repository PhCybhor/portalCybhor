import json, urllib.request, urllib.parse

API_KEY = "AIzaSyB_4aAZBxQbdAH5BsWnIk9-5-zSr0hwHc4"
ADMIN_EMAIL = "lopes@cybhor.com"
ADMIN_PASSWORD = "Admin000"
TARGETS = {
    "joao@cybhor.com": "João",
    "lisboa@cybhor.com": "Lisboa",
    "cristofer@cybhor.com": "Cristofer",
}
PASSWORDS = {
    "joao@cybhor.com": "user123",
    "lisboa@cybhor.com": "user456",
    "cristofer@cybhor.com": "user789",
}


def auth_request(path, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"https://identitytoolkit.googleapis.com/v1{path}?key={API_KEY}",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        raise RuntimeError(err.read().decode("utf-8"))


admin_auth = auth_request("/accounts:signInWithPassword", {
    "email": ADMIN_EMAIL,
    "password": ADMIN_PASSWORD,
    "returnSecureToken": True,
})
admin_token = admin_auth["idToken"]

for email, desired_name in TARGETS.items():
    user_auth = auth_request("/accounts:signInWithPassword", {
        "email": email,
        "password": PASSWORDS[email],
        "returnSecureToken": True,
    })
    local_id = user_auth["localId"]
    token_param = urllib.parse.quote(admin_token)
    user_ref = f"https://cybhor-b650a-default-rtdb.firebaseio.com/users/{local_id}.json?auth={token_param}"

    current_req = urllib.request.Request(user_ref, method="GET")
    with urllib.request.urlopen(current_req, timeout=30) as resp:
        current_profile = json.loads(resp.read().decode("utf-8")) or {}

    current_profile["name"] = desired_name
    put_data = json.dumps(current_profile).encode("utf-8")
    put_req = urllib.request.Request(user_ref, data=put_data, method="PUT", headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(put_req, timeout=30) as resp:
        resp.read()

    print(email, "updated", local_id, current_profile)
