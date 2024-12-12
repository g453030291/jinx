import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from api.conf.config import constant


class BrevoUtil:
    def __init__(self):
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = constant.brevo_api_key
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    def send_verification_email(self, email_address, verification_code):
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{'email': email_address}],
            sender={'email': 'support@jinx-aa.xyz', 'name': 'jinx-support'},
            subject='邮件验证',
            html_content=f'<html><body>'
                         f'<p>您正在使用该邮箱验证登录: {verification_code}</p>'
                         f'<p>非本人操作请忽略</p>'
                         f'</body></html>'
        )
        try:
            api_response = self.api_instance.send_transac_email(send_smtp_email)
            return api_response
        except ApiException as e:
            print(f"Exception when sending email: {e}")
            return e

if __name__ == '__main__':
    brevo_util = BrevoUtil()
    result = brevo_util.send_verification_email('453030291@qq.com', 'ABCD')
    print(result)
