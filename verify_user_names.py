import json, urllib.request, urllib.parse

API_KEY = "AIzaSyB_4aAZBxQbdAH5BsWnIk9-5-zSr0hwHc4"
ADMIN_EMAIL = "lopes@cybhor.com"
ADMIN_PASSWORD = "Admin000"
UIDS = [
    "riOCijbMh2fjgq2RpvD0eBo5qx43",
    "l0GGEIETAZg4luOZHsIk5clp5II2",
    "n14tf95xtfUkzbmvLktxQLmVpXp1",
]


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

for uid in UIDS:
    url = f"https://cybhor-b650a-default-rtdb.firebaseio.com/users/{uid}.json?auth={urllib.parse.quote(admin_token)}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        body = resp.read().decode("utf-8")
    print(uid, body)
