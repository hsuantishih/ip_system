from nckuccapi import NckuCcApi

SoapClient = NckuCcApi()

def handle_user_info(query):
    result = SoapClient.GetUserInfo(query)

    return result