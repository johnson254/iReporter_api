class User:
    count = 0

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.id = User.count
        User.count += 1
