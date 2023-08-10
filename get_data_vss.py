import urllib.request, json

def read_data(web_url):
    with urllib.request.urlopen(web_url) as url:
        data = json.loads(url.read().decode())
        print(data)
        return data

def get_data(url):
    data = read_data(url)
    commitments = []
    # index,share_value,commitments_list_values, g_val, p_share, p_commitment
    for commit in data["commitments"]:
        commitments.append(int(commit["data"]["value"],16))
    index = data["share"]["index"]
    share_value = int(data["share"]["value"]["value"],16)
    g_val = int(data["group"]["generator"]["data"]["value"],16)
    p_share = int(data["share"]["value"]["prime"],16)
    p_commitment = int(data["group"]["generator"]["data"]["prime"],16)
    return {
        "share_index": index,
        "share_value": share_value,
        "commitments": commitments,
        "g_val": g_val,
        "p_share": p_share,
        "p_commitment": p_commitment
    }