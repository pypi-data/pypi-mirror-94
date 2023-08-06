def dissoc(m, *keys):
    return {k: m[k] for k in m if k not in keys}
