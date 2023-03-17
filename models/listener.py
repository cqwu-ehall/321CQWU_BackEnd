from cqwu import Client
from cqwu.errors import UsernameOrPasswordError, CookieError, NeedCaptchaError


def listener(**args_):
    """ 自动解决密码过期，密码错误问题 """
    web_vpn = args_.get("web_vpn", False)

    if "web_vpn" in args_:
        del args_["web_vpn"]

    def decorator(function):
        async def handler(*args, **kwargs):
            client: Client = args[0]
            need_login = False
            if web_vpn and not client.web_ehall_path:
                need_login = True
            for i in range(2):
                try:
                    if need_login:
                        await client.login_with_password()
                        if web_vpn:
                            await client.login_web_vpn()
                    return await function(*args, **kwargs)
                except UsernameOrPasswordError:
                    return {"code": 1, "msg": "用户名或密码错误，请尝试重新登录"}
                except NeedCaptchaError:
                    return {"code": 1, "msg": "需要验证码，请尝试重新登录"}
                except CookieError:
                    if i == 1:
                        return {"code": 1, "msg": "自动登录失败，请尝试重新登录"}
                    need_login = True

        return handler

    return decorator
