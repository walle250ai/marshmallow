import pytest
from marshmallow import Schema, fields


class UserSchema(Schema):
    name = fields.Str()
    email = fields.Str()
    password = fields.Str()

    class Meta:
        field_groups = {
            "public": ["name", "email"],
            "sensitive": ["password"],
        }


def test_dump_with_single_group():
    schema = UserSchema()
    user = {"name": "John", "email": "john@example.com", "password": "secret"}
    result = schema.dump(user, groups=["public"])
    assert "name" in result
    assert "email" in result
    assert "password" not in result
    assert result["name"] == "John"
    assert result["email"] == "john@example.com"


def test_load_with_single_group():
    schema = UserSchema()
    data = {"password": "secret"}
    result = schema.load(data, groups=["sensitive"])
    assert "password" in result
    assert "name" not in result
    assert "email" not in result
    assert result["password"] == "secret"


def test_dump_with_multiple_groups():
    schema = UserSchema()
    user = {"name": "John", "email": "john@example.com", "password": "secret"}
    result = schema.dump(user, groups=["public", "sensitive"])
    assert "name" in result
    assert "email" in result
    assert "password" in result
    assert result["name"] == "John"
    assert result["email"] == "john@example.com"
    assert result["password"] == "secret"


def test_load_with_multiple_groups():
    schema = UserSchema()
    data = {"name": "John", "email": "john@example.com", "password": "secret"}
    result = schema.load(data, groups=["public", "sensitive"])
    assert "name" in result
    assert "email" in result
    assert "password" in result


def test_dump_with_unknown_group():
    schema = UserSchema()
    user = {"name": "John", "email": "john@example.com", "password": "secret"}
    with pytest.raises(ValueError, match="Unknown field group"):
        schema.dump(user, groups=["unknown_group"])


def test_load_with_unknown_group():
    schema = UserSchema()
    data = {"name": "John"}
    with pytest.raises(ValueError, match="Unknown field group"):
        schema.load(data, groups=["unknown_group"])


def test_field_groups_with_nonexistent_field():
    with pytest.raises(ValueError, match="do not exist in schema"):

        class InvalidSchema(Schema):
            name = fields.Str()

            class Meta:
                field_groups = {
                    "invalid": ["nonexistent_field"],
                }


def test_groups_with_only():
    schema = UserSchema()
    user = {"name": "John", "email": "john@example.com", "password": "secret"}
    result = schema.dump(user, groups=["public"], only=["name"])
    assert "name" in result
    assert "email" not in result
    assert "password" not in result


def test_groups_with_exclude():
    schema = UserSchema()
    user = {"name": "John", "email": "john@example.com", "password": "secret"}
    result = schema.dump(user, groups=["public"], exclude=["email"])
    assert "name" in result
    assert "email" not in result
    assert "password" not in result


def test_dump_many_with_groups():
    schema = UserSchema(many=True)
    users = [
        {"name": "John", "email": "john@example.com", "password": "secret1"},
        {"name": "Jane", "email": "jane@example.com", "password": "secret2"},
    ]
    result = schema.dump(users, groups=["public"])
    assert len(result) == 2
    for item in result:
        assert "name" in item
        assert "email" in item
        assert "password" not in item


def test_load_many_with_groups():
    schema = UserSchema()
    data = [
        {"password": "secret1"},
        {"password": "secret2"},
    ]
    result = schema.load(data, many=True, groups=["sensitive"])
    assert len(result) == 2
    for item in result:
        assert "password" in item
        assert "name" not in item
        assert "email" not in item


def test_init_schema_with_groups():
    schema = UserSchema(groups=["public"])
    user = {"name": "John", "email": "john@example.com", "password": "secret"}
    result = schema.dump(user)
    assert "name" in result
    assert "email" in result
    assert "password" not in result


def test_init_schema_with_unknown_group():
    with pytest.raises(ValueError, match="Unknown field group"):
        UserSchema(groups=["unknown_group"])