from core import Core

def login(Handler):
    username = input("input username : ")
    password = input("input user password : ")
    return Handler.UserSetting(username, password)

if __name__ == "__main__":
    Handler = Core()
    if login(Handler):
        Handler.Handler()
    else:
        print("login error")
