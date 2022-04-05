from logging import info, debug, error

from core.text_embedding import SentenceEmbedding

def image_mod2vec(data:dict, embedding:SentenceEmbedding, threshold:float = 0.7):
    assert 'height' in data and 'width' in data
    area = data['height'] * data['width']
    size = '' 
    if area < (320 * 240):
        size = 'very small'
    elif area < (1024 * 240):
        size = 'small'
    elif area < (1920 * 1024):
        size = 'large'
    else: size = 'very large'

    assert "unsafe" in data and "safe" in data
    nsfw = ''
    if data["unsafe"] >= 0.9:
        nsfw = ' very likely NSFW'
    elif data["unsafe"] >= threshold:
        nsfw = ' likely NSFW'
    elif data["safe"] >= 0.9:
        nsfw = ' very likely work-safe'
    elif data["safe"] >= threshold:
        nsfw = ' likely work-safe'

    assert "drawings" in data
    assert "hentai" in data
    assert "neutral" in data
    assert "porn" in data
    assert "sexy" in data
    category = ''
    if data["porn"] >= 0.9:
        category = ' image that is very likely pornographic'
    elif data["porn"] >= threshold:
        category = ' image that is likely pornographic'
    elif data["hentai"] >= 0.9:
        category = ' image that is very likely hentai or adult cartoon'
    elif data["hentai"] >= threshold:
        category = ' image that is likely hentai or adult cartoon'
    elif data["sexy"] >= 0.9:
        category = ' image that is very likely adult or racy content'
    elif data["sexy"] >= threshold:
        category = 'image that is likely adult or racy'
    else: category = ' image'

    assert "objects" in data
    s = 'This is a {}{}{}.'.format(size, nsfw, category)
    return s, embedding.get_vector(s)