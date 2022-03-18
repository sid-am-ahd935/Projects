import requests


def get_todos(token):
    url = "http://127.0.0.1:8000/api/todos?count=30"       # count set to maximum page size that can be requested, set in todos.pagination
    r = requests.get(url= url, headers= {"Authorization": "Bearer " + token})
    # print(r.content.decode())

    return r.json()

def post_todos(token : str, post_count : int, title= None, desc= None, is_complete= None) -> dict:

    url = "http://127.0.0.1:8000/api/todos/"

    if not desc:
        desc = "This is a test description for token " + str(token[~5:])
    
    if not title:
        title = "Dummy Title for token " + str(token[~5:])
    
    for i in range(post_count):
        payload = {
            "title" : f"{title} ({i+1})",
            "desc" : f"{desc} ({i+1})",
            "is_complete" : is_complete,
        }
        r = requests.post(url= url, data = payload, headers= {"Authorization": "Bearer " + token})
        # print(r.content.decode())
    
    return get_todos(token)


def login():
    url = "http://127.0.0.1:8000/api/auth/login"
    payload = {
        "email" : "aman2@gmail.com",
        "password" : "password1234",
    }
    r = requests.post(url= url, data= payload)

    # print(r.content.decode())

    return (r.json().get("token"))




if __name__ == "__main__":
    token = login()
    result = post_todos(token,1).get("results")
    # result = get_todos(token).get("results")
    if result:
        for todo in result:
            print(todo)
    # print(token)
    # print(result)

