# choixpeau

## Install

```
pip install choixpeau
```

## Usage

```python
from choixpeau import choixpeau

redis_config = {
    "host": "localhost
}

choixpeau = choixpeau.Choixpeau(
    redis_config=redis_config, 
    ab_test_ids=["poudlard"],
    buckets=["gryffondor", "poufsouffle", "serdaigle", "serpentard"] # ["A", "B"] by default
)
```

### get

```python
choixpeau.get("harrypotter")

# if the key already exists
> [(None, { "ab_test_group": "gryffondor", "created_at": "2021-01-29" }, "poudlard")] 

# if it does not
> [("ab:poudlard:harrypotter", { "ab_test_group": "gryffondor", "created_at": "2021-01-29" }, "poudlard")]
```

### store

```python
choixpeau.store(
    "ab:poudlard:harrypotter", 
    { "ab_test_group": "gryffondor", "created_at": "2021-01-29" }
)
```

## FastAPI

```python
from fastapi import FastAPI, Request, BackgroundTasks
from choixpeau import choixpeau
from choixpeau.decorators.fastapi import ab

app = fastapi.FastAPI()

redis_config = {
    "host": "localhost
}

@app.on_event("startup")
async def startup():
    # Initialize choixpeau at the app level
    app.state.choixpeau = choixpeau.Choixpeau(
        redis_config=redis_config, 
        ab_test_ids=["poudlard"],
        buckets=["gryffondor", "poufsouffle", "serdaigle", "serpentard"]
    )

@app.post("/")
@ab # requires the request body to have a user_id field
async def read_house(request: Request, background_tasks: BackgroundTasks):
    wizard = request.state.user # the user attribute is automatically added to the request
    
    if wizard["ab_test_group"] == "gryffondor":
        return { "message": "Welcome to Gryffondor!" }
    else:
        return { "message": "Welcome!" }
```

