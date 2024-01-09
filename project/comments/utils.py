def check_ownership(author_id: int, user_id: int):
    if author_id != user_id:
        return False
    return True