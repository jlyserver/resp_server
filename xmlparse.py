#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import xml.sax

class WxResponseXmlHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.res = {}
        self.CurrentData = ''
    def startElement(self, tag, attributes):
        self.CurrentData = tag
    def endElement(self, tag):
        self.CurrentData = ''
    def _trip(self, s):
        i = s.find('[', 0)
        i = s.find('[', i)
        return s[i+1, -2]
    def characters(self, content):
        a = ['return_code','return_msg','appid','mch_id','device_info',\
            'nonce_str', 'sign','result_code','prepay_id','trade_type',\
        'code_url', 'bank_type', 'cash_fee','fee_type', 'is_subscribe',\
        'openid', 'out_trade_no', 'result_code','time_end','total_fee',\
        'trade_type', 'transaction_id']
        for e in a:
            if self.CurrentData == e:
                self.res[e] = content
                break
    def dis(self):
        for e in self.res:
            print('%s=%s' % (e, self.res[e]))

#支付结果 微信返回的xml结果 返回字典
def order_response_xml_parse(xml_str):
    h  = WxResponseXmlHandler()
    xml.sax.parseString(xml_str, h)
    return h.res

if __name__ == '__main__':
    line = '<xml><appid><![CDATA[wx0267b1a42b591564]]></appid><bank_type><![CDATA[CFT]]></bank_type><cash_fee><![CDATA[1]]></cash_fee><device_info><![CDATA[WEB]]></device_info><fee_type><![CDATA[CNY]]></fee_type><is_subscribe><![CDATA[Y]]></is_subscribe><mch_id><![CDATA[1501837141]]></mch_id><nonce_str><![CDATA[5E1AD59DC715DF861CB2]]></nonce_str><openid><![CDATA[oqNGlwbrQmKlwEn39RC5DxLW0Wbw]]></openid><out_trade_no><![CDATA[2018042212465000]]></out_trade_no><result_code><![CDATA[SUCCESS]]></result_code><return_code><![CDATA[SUCCESS]]></return_code><sign><![CDATA[A9DE6EBD0C213BCC493E2690B538AE7F]]></sign><time_end><![CDATA[20180422124742]]></time_end><total_fee>1</total_fee><trade_type><![CDATA[NATIVE]]></trade_type><transaction_id><![CDATA[4200000080201804223556267858]]></transaction_id></xml>'
    r = order_response_xml_parse(line)
    print(r)
