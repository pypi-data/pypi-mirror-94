# coding: utf-8

RESOURCE_MAPPING = {
    'auto_authorize': {
        'resource': '/products/!AutoAuthorize',
        'docs': 'https://secure.sectigo.com/api/pdf/reseller/AutoAuthorize%20and%20AutoReject%20v1.01.pdf',
        'methods': ['POST']
    },
    'auto_reject': {
        'resource': '/products/!AutoReject',
        'docs': 'https://secure.sectigo.com/api/pdf/reseller/AutoAuthorize%20and%20AutoReject%20v1.01.pdf',
        'methods': ['POST']
    },
    'add_server_licence': {
        'resource': '/products/!AutoAddServerLicence',
        'docs': 'https://secure.sectigo.com/api/pdf/latest/AutoAddServerLicence.pdf',
        'methods': ['POST']
    },
    'auto_apply_ssl': {
        'resource': '/products/!AutoApplyOrder',
        'docs': 'https://sectigo.com/uploads/resources/Sectigo-AutoApplyOrder-API-v2.2.pdf',
        'methods': ['POST']
    },
    'auto_replace_ssl': {
        'resource': '/products/!AutoReplaceSSL',
        'docs': 'https://secure.sectigo.com/api/pdf/latest/AutoReplaceSSL.pdf',
        'methods': ['POST']
    },
    'auto_revoke_ssl': {
        'resource': '/products/!AutoRevokeSSL',
        'docs': 'https://secure.sectigo.com/api/pdf/latest/AutoRevokeSSL.pdf',
        'methods': ['POST']
    },
    'collect_ssl': {
        'resource': '/products/download/CollectSSL',
        'docs': 'https://secure.sectigo.com/api/pdf/webhostreseller/sslcertificates/CollectSSL%20v1.17.pdf',
        'methods': ['POST']
    },
    'csr_decoder': {
        'resource': '/products/!DecodeCSR',
        'docs': 'https://secure.sectigo.com/api/pdf/latest/DecodeCSR.pdf',
        'methods': ['POST']
    },
    'dcv_email_address_list': {
        'resource': '/products/!GetDCVEmailAddressList',
        'docs': 'https://secure.sectigo.com/api/pdf/latest/GetDCVEmailAddressList.pdf',
        'methods': ['POST']
    },
    'resend_dcv_email': {
        'resource': '/products/!ResendDCVEmail',
        'docs': 'https://secure.sectigo.com/api/pdf/latest/ResendDCVEmail.pdf',
        'methods': ['POST']
    },
    'remove_mdc_domain': {
        'resource': '/products/!AutoRemoveMDCDomain',
        'docs': 'https://secure.sectigo.com/api/pdf/latest/AutoRemoveMDCDomain.pdf',
        'methods': ['POST']
    },
    'ov_callback': {
        'resource': '/products/!UpdateUserOvCallback',
        'docs': 'https://secure.sectigo.com/api/pdf/latest/UpdateUserOvCallback.pdf',
        'methods': ['POST']
    },
    'ev_click_through': {
        'resource': '/products/!UpdateUserEvClickThrough',
        'docs': 'https://secure.sectigo.com/api/pdf/latest/UpdateUserEvClickThrough.pdf',
        'methods': ['POST']
    },
    'mdc_detail_order_status': {
        'resource': '/products/!GetMDCDomainDetails',
        'docs': 'https://secure.sectigo.com/api/pdf/latest/GetMDCDomainDetails.pdf',
        'methods': ['POST']
    },
    'provide_ev_details': {
        'resource': '/products/!ProvideEVDetails',
        'docs': 'https://secure.sectigo.com/api/pdf/latest/ProvideEVDetails.pdf',
        'methods': ['POST']
    },
    'single_domain_detail_order_status': {
        'resource': '/products/!GetDetailedOrderStatus',
        'docs': 'https://secure.sectigo.com/api/pdf/latest/GetDetailedOrderStatus.pdf',
        'methods': ['POST']
    },
    'ssl_checker': {
        'resource': '/sslchecker',
        'docs': 'https://secure.sectigo.com/api/pdf/latest/SSLChecker.pdf',
        'methods': ['GET', 'POST']
    },
    'update_dcv': {
        'resource': '/products/!AutoUpdateDCV',
        'docs': 'https://secure.sectigo.com/api/pdf/latest/AutoUpdateDCV.pdf',
        'methods': ['POST']
    },
}
