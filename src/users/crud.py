from users.schemas import CreateUser

async def create_user(user_in: CreateUser):
    user = user_in.model_dump()
    return {
        'success': True,
        'user': user
    }