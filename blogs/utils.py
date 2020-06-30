def extractDigest(text, count):
    # 先頭からcountの数だけ抽出
    result = text[0:count] + "..."
    return result