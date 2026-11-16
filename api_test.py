import requests, os

def make_request(method, url, **kwargs):

     timeout = kwargs.pop("timeout", 5)

     try:
          response = requests.request(
               method,
               url,
               timeout=timeout,
               **kwargs
          )
          response.raise_for_status()

          if not response.content:
               return True, None
          try:
               return True, response.json()
          except requests.exceptions.JSONDecodeError:
               print("JSON decoding failure.")
               return False, None
          
     except requests.exceptions.RequestException as error:
          if isinstance(error, requests.exceptions.HTTPError):
               print(f"HTTP error: {error.response.status_code}")
          else:
               print(f"Request failed: {error}")

          return False, None

def get_user(user_id):
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"

    return make_request(
         "GET",
         url
    )


def create_user(name, username, email):
    headers = {
             "Accept" : "application/json"
        }
    
    url = "https://jsonplaceholder.typicode.com/users"
    new_user = {
         "name": name,
         "username": username,
         "email": email
    }

    return make_request(
         "POST",
         url,
         headers=headers,
         json=new_user
     )


def update_user(user_id, email):
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    update_data = {
         "email": email
    }

    return make_request(
         "PATCH",
         url,
         json=update_data
    )


def delete_user(user_id):
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    
    success, data = make_request(
         "DELETE",
         url
    )
    
    return success


def search_users(username):
    headers = {
         "Accept" : "application/json"
    }
    params = {
         "username" : username
         }
    url = "https://jsonplaceholder.typicode.com/users"

    return make_request(
         "GET",
         url,
         headers=headers,
         params=params
         )


def authenticated_request():
     api_key = os.getenv("MY_API_KEY")
     url = "https://jsonplaceholder.typicode.com/users"

     if not api_key:
          raise ValueError("API connection failed: Missing API Key.")
     
     headers = {
          "Accept": "application/json",
          "X-API-Key": api_key
          }
     
     print("API key loaded successfully.")

     return make_request(
          "GET",
          url,
          headers=headers
     )


def bearer_request():
     token = os.getenv("MY_API_TOKEN")
     url = "https://jsonplaceholder.typicode.com/users"

     if not token:
          raise ValueError("API connection failed: Missing Token.")
     
     headers = {
          "Accept": "application/json",
          "Authorization": f"Bearer {token}"
          }
     
     print("Token loaded successfully.")

     return make_request(
          "GET",
          url,
          headers=headers
     )
     
if __name__ == "__main__":

     get_success, get_data = get_user(4)
     if get_success:
          if get_data is not None:
               print(get_data["name"])
               print(get_data["email"])
               print(get_data["address"]["city"])
               print(get_data["address"]["geo"]["lat"])

     create_success, create_data = create_user("Douglas", "dougie", "doug@example.com")
     print(create_data)

     update_success, update_data = update_user(11, "dougie@example.com")
     print(update_data)

     delete_success = delete_user(999)

     if delete_success:
          print("User deleted successfully.")
     else:
          print("Delete request failed.")

     search_success, search_data = search_users("Bret")

     if search_success:
          for user in search_data:
               print(user["name"])
               print(user["email"])
     else:
          print("Could not retrieve users.")

     auth_success, auth_data = authenticated_request()

     token_success, token_data = bearer_request()

     request_success, request_data = make_request(
          "GET",
          "https://jsonplaceholder.typicode.com/users"
     )

     print(request_data[0]["name"])