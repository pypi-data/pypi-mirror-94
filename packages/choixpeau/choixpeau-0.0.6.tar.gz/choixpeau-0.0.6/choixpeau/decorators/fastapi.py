from functools import wraps

def ab(func):
    
    @wraps(func)
    async def wrapper(*args, **kwargs):
        
        request = kwargs.get("request")
        background_tasks = kwargs.get("background_tasks")

        body = await request.json()
        user_id = body.get("user_id")
        
        choixpeau = request.app.state.choixpeau

        ab_tests = choixpeau.get(user_id)

        for key, value, _  in ab_tests:
            if key:
                background_tasks.add_task(choixpeau.store, key, value)

        setattr(
            request.state, 
            "user", 
            [
                {
                    "user_id": user_id, 
                    "ab_test_id": ab_test_id, 
                    **value
                } 
                for _, value, ab_test_id in ab_tests
            ]
        )         
        
        return await func(*args, **kwargs)

    return wrapper