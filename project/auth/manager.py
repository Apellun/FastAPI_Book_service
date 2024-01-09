from typing import Optional
from fastapi import Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from auth.models import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.") #TODO: try to send an email?