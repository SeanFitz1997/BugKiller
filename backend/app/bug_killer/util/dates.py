from arrow import Arrow


def to_utc_str(dt: Arrow) -> str:
    return dt.format('YYYY-MM-DDTHH:mm:ss') + 'Z'
