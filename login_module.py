def login(username, password):
    # Open the file in read mode
    with open("user_credentials.txt", "r") as file:
        for line in file:
            # Split each line into username, password, and other details
            stored_username, stored_password, *_ = line.strip().split(",")

            # Check if the entered username and password match
            if username == stored_username and password == stored_password:
                return True

    return False
