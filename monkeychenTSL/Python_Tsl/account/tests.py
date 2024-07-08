from pathlib import Path

from account.models import Profile


def test_login(user, api_client):
    resp = api_client.post(
        "/api/account/profile/login/",
        {
            "username": "test_user",
            "password": "test_user_pass",
        },
        format="json",
    )
    assert resp.status_code == 200, resp.status_code


def test_api_401(api_client):
    resp = api_client.get("/api/account/profile/profile/")
    assert resp.status_code == 401, resp.status_code


def test_reset_password(user, user_api_client):
    resp = user_api_client.post(
        "/api/account/profile/reset_password/",
        {
            "new_password": "1234567",
            "confirm_password": "1234567",
        },
        format="json",
    )
    assert resp.status_code == 204, resp.status_code
    # 通过数据库方式验证新密码
    user.refresh_from_db()  # 加载新数据内容
    assert user.check_password("1234567")
    # 通过接口的方式验证新密码
    user_api_client.logout()  # 退出登录
    resp = user_api_client.post(
        "/api/account/profile/login/",
        {  # 尝试重新登录
            "username": "test_user",
            "password": "1234567",
        },
        format="json",
    )
    assert resp.status_code == 200, resp.status_code


def test_api_profile(user_api_client, user):
    resp = user_api_client.get("/api/account/profile/profile/")
    assert resp.status_code == 200, resp.status_code
    assert resp.data["user"] == user.id


def test_change_profile(user_api_client, user):
    path = Path(__file__).parent / "logo.jpg"
    file = open(path, "rb")
    resp = user_api_client.post(
        "/api/account/profile/change/",
        {
            "name": "北凡123",
            "head_img": file,
        },
    )
    assert resp.status_code == 200, resp.status_code
    # 数据库断言
    profile = Profile.objects.get(user=user)
    assert profile.name == "北凡123"
    assert "logo" in str(profile.head_img)
    assert "jpg" in str(profile.head_img)
