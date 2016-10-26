def gen_hashtags(hashtags=None):
    if hashtags:
        return ' '.join(map(lambda x: '#%s' % x, hashtags))
    else:
        return None
