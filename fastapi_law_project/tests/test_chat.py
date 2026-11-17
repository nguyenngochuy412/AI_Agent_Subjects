def auth(key: str) -> dict[str, str]:
    return {"X-API-Key": key}


async def test_chat_requires_api_key(client):
    r = await client.post("/chat", json={"message": "hello"})
    assert r.status_code == 401


async def test_chat_rejects_invalid_key(client):
    r = await client.post("/chat", json={"message": "hello"}, headers=auth("sk_sai"))
    assert r.status_code == 401


async def test_chat_returns_reply(client, make_api_key):
    key = await make_api_key("an")
    r = await client.post("/chat", json={"message": "hello"}, headers=auth(key))
    assert r.status_code == 200
    assert r.json() == {"reply": "Chào bạn"}


async def test_chat_rejects_empty_message(client, make_api_key):
    key = await make_api_key("an")
    r = await client.post("/chat", json={"message": ""}, headers=auth(key))
    assert r.status_code == 422


async def test_history_is_saved_in_order(client, make_api_key):
    key = await make_api_key("an")
    await client.post("/chat", json={"message": "hello"}, headers=auth(key))
    r = await client.get("/history", headers=auth(key))
    assert r.status_code == 200
    body = r.json()
    assert body["user_id"] == "an"
    assert [m["role"] for m in body["messages"]] == ["user", "assistant"]
    assert body["messages"][0]["content"] == "hello"


async def test_history_is_isolated_between_users(client, make_api_key):
    key_an = await make_api_key("an")
    key_binh = await make_api_key("binh")
    await client.post("/chat", json={"message": "hello"}, headers=auth(key_an))

    r = await client.get("/history", headers=auth(key_binh))
    assert r.json()["messages"] == []