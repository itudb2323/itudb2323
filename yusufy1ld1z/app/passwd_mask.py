import base64

string = "fill"  # enter your mySQL password here


def maskPsw():
    encode = base64.b64encode(string.encode("utf-8"))
    # print("str-byte : ", encode)

    # Decoding the string
    decode = base64.b64decode(encode).decode("utf-8")
    # print("byte-str : ", decode)

    return decode
