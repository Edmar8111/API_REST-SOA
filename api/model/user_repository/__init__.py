from .. import create, read, update, delete


create=create.CreateModel()
    
def ReadAll():
    return read.get_all_users()

def ReadById(id: int):
    return read.ReadModel(id).get_user_by_id()

def CreateUser(**user_data):
    username, email=(
        user_data['username'],
        user_data['email']
    )
    return create.create_user(username=username, email=email)

def UpdateUser(**update_data):
    id, username, email=(
        update_data['id'], 
        update_data['username'],
        update_data['email']
    )
    return update.UpdateUserModel(id=id,username=username,email=email)