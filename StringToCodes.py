import datetime
import urllib.parse
import html
import xml.sax.saxutils
import sys
import base64
import encodings.punycode
import quopri
import argparse
import DateTime


def encode_special_chars(input_str):
    special_chars = {
        '<': '%3C',
        '>': '%3E',
        '"': '%22',
        "'": '%27',
        "&": '%26',
        "#": '%23'
    }
    encoded_str = ''
    for char in input_str:
        if char in special_chars:
            encoded_str += special_chars[char]
        else:
            encoded_str += char
    return encoded_str

def encode_special_chars2(input_str):
    special_chars = {
        '<': '%26%2360;',
        '>': '%26%2362;',
        '"': '%26%2334;',
        "'": '%26%2339;',
        "&": '%26',
        "#": '%23'
    }
    encoded_str = ''
    for char in input_str:
        if char in special_chars:
            encoded_str += special_chars[char]
        else:
            encoded_str += char
    return encoded_str

def encode_special_chars3(input_str):
    special_chars = {
        '<': '%26%23x3c;',
        '>': '%26%23x3e;',
        '"': '%26%23x22;',
        "'": '%26%23x27;',
        "&": '%26',
        "#": '%23'
    }
    encoded_str = ''
    for char in input_str:
        if char in special_chars:
            encoded_str += special_chars[char]
        else:
            encoded_str += char
    return encoded_str

def encode_html_entities(input_str):
    return html.escape(input_str)

def encode_html_codes(input_str):
    html_codes = {
        '<': '&#60;',
        '>': '&#62;',
        '"': '&#34;',
        "'": '&#39;',
        "&": '&#38;',
        "#": '&#35;'
    }
    encoded_str = ''
    for char in input_str:
        if char in html_codes:
            encoded_str += html_codes[char]
        else:
            encoded_str += char
    return encoded_str

def encode_html_codes2(input_str):
    html_codes = {
        '<': '&#x3C;',
        '>': '&#x3E;',
        '"': '&#x22;',
        "'": '&#x27;',
        "&": '&#38;',
        "#": '&#35;'
    }
    encoded_str = ''
    for char in input_str:
        if char in html_codes:
            encoded_str += html_codes[char]
        else:
            encoded_str += char
    return encoded_str

def encode_xml_entities(input_str):
    return xml.sax.saxutils.escape(input_str)

def encode_unicode_escape(input_str):
    encoded_str = input_str.encode('unicode_escape').decode('utf-8')
    return encoded_str

def encode_url_percent(input_str):
    return urllib.parse.quote_plus(input_str)

def replace_spaces_with_slash(input_str):
    input_str = input_str.replace(' ', '/')
    input_str = input_str.replace('%20', '/')
    return input_str

def decode_url_percent(encoded_str):
    return urllib.parse.unquote(encoded_str)

def encode_base64(input_str):
    encoded_bytes = base64.b64encode(input_str.encode('utf-8'))
    encoded_str = encoded_bytes.decode('utf-8')
    return encoded_str


def encode_hexadecimal(input_str):
    encoded_bytes = input_str.encode('utf-8')
    encoded_str = ''.join(f'{byte:02x}' for byte in encoded_bytes)
    return encoded_str

def encode_uppercase(input_str):
    return input_str.upper()

def encode_lowercase(input_str):
    return input_str.lower()



def read_file_to_string(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
        return file_content
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def save_to_file(encoded_data, filename):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(encoded_data+"\n\n\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="파일 경로를 입력받아 내용을 출력하는 프로그램")
        parser.add_argument('file_path', type=str, help='읽을 파일의 경로')

        args = parser.parse_args()

        file_content = read_file_to_string(args.file_path)
        if file_content is not None:
            print(file_content)
        input_str = file_content
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        save_to_file(timestamp + "  Polyglot : "+ input_str + "\n\n\n", 'EncodedPolyglot' + timestamp + '.txt')
        encoded_str = encode_special_chars(input_str)
        print("Special URL Encoded:", encoded_str)
        save_to_file("Special URL Encoded: "+encoded_str, 'EncodedPolyglot' + timestamp + '.txt')

        encoded_str2 = encode_special_chars2(input_str)
        print("Special URL Encoded2:", encoded_str2)
        save_to_file("Special URL Encoded2: "+encoded_str2, 'EncodedPolyglot' + timestamp + '.txt')

        encoded_str3 = encode_special_chars3(input_str)
        print("Special URL Encoded3 (16):", encoded_str3)
        save_to_file("Special URL Encoded3: "+encoded_str3, 'EncodedPolyglot' + timestamp + '.txt')

        html_encoded_str = encode_html_entities(input_str)
        print("HTML Entities Encoded:", html_encoded_str)
        save_to_file("HTML Entities Encoded: "+html_encoded_str, 'EncodedPolyglot' + timestamp + '.txt')

        html_codes_encoded_str = encode_html_codes(input_str)
        print("HTML Codes Encoded:", html_codes_encoded_str)
        save_to_file("HTML Codes Encoded: "+html_codes_encoded_str, 'EncodedPolyglot' + timestamp + '.txt')

        html_codes_encoded_str2 = encode_html_codes2(input_str)
        print("HTML Codes Encoded (16):", html_codes_encoded_str2)
        save_to_file("HTML Codes Encoded (16): "+html_codes_encoded_str2, 'EncodedPolyglot' + timestamp + '.txt')

        xml_encoded_str = encode_xml_entities(input_str)
        print("XML Entities Encoded:", xml_encoded_str)
        save_to_file("XML Entities Encoded: "+xml_encoded_str, 'EncodedPolyglot' + timestamp + '.txt')

        unicode_escape_encoded_str = encode_unicode_escape(input_str)
        print("Unicode Escape Encoded:", unicode_escape_encoded_str)
        save_to_file("Unicode Escape Encoded: "+unicode_escape_encoded_str, 'EncodedPolyglot' + timestamp + '.txt')

        url_percent_encoded_str = encode_url_percent(input_str)
        print("URL Percent Encoded:", url_percent_encoded_str)
        save_to_file("URL Percent Encoded: "+url_percent_encoded_str, 'EncodedPolyglot' + timestamp + '.txt')

        replaced_spaces_str = replace_spaces_with_slash(input_str)
        print("Spaces and %20 replaced with slash:", replaced_spaces_str)
        save_to_file("Spaces and %20 replaced with slash: " + replaced_spaces_str,
                     'EncodedPolyglot' + timestamp + '.txt')


        decoded_url_str = decode_url_percent(replaced_spaces_str)
        print("URL Percent Decoded:", decoded_url_str)
        save_to_file("URL Percent Decoded: " + decoded_url_str, 'EncodedPolyglot' + timestamp + '.txt')

        base64_encoded_str = encode_base64(input_str)
        print("Base64 Encoded:", base64_encoded_str)
        save_to_file("Base64 Encoded: "+base64_encoded_str, 'EncodedPolyglot' + timestamp + '.txt')


        hexadecimal_encoded_str = encode_hexadecimal(input_str)
        print("Hexadecimal Encoded:", hexadecimal_encoded_str)
        save_to_file("Hexadecimal Encoded: "+hexadecimal_encoded_str, 'EncodedPolyglot' + timestamp + '.txt')
        uppercase_encoded_str = encode_uppercase(input_str)
        print("Uppercase Encoded:", uppercase_encoded_str)
        save_to_file("Uppercase Encoded: "+uppercase_encoded_str, 'EncodedPolyglot' + timestamp + '.txt')

        lowercase_encoded_str = encode_lowercase(input_str)
        print("Lowercase Encoded:", lowercase_encoded_str)
        save_to_file("Lowercase Encoded: "+lowercase_encoded_str, 'EncodedPolyglot' + timestamp + '.txt')

        html_encoded_STR = encode_uppercase(html_encoded_str)
        print("Uppercase Html_encoded:", html_encoded_STR)
        save_to_file("Uppercase Html_encoded: "+html_encoded_STR, 'EncodedPolyglot' + timestamp + '.txt')

        html_encoded_lower_str = encode_lowercase(html_encoded_str)
        print("Lowercase Html_encoded:", html_encoded_lower_str)
        save_to_file("Lowercase Html_encoded: "+html_encoded_lower_str, 'EncodedPolyglot' + timestamp + '.txt')


    else:
        print('Usage: python StringToCodes.py "filename.txt"')