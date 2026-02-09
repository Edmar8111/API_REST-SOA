from .. import read, create

create, read=(
    create.CreateModel(),
    read.ReadModel()
)
def ReadAll():
    return read.get_all_users()

def ReadById(user_id: int):
    return read.get_user_by_id(user_id)

def CreateUser(**user_data):
    return create.create_user(**user_data)