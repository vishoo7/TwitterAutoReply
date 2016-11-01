from utils import gen_hashtags

class TestUtils:
    def test_gen_hashtags(self):
        single_hashtag = gen_hashtags(['test'])
        single_hashtag2 = gen_hashtags(['123'])
        multiple_hashtags = gen_hashtags(['foo', 'bar', 'baz'])
        multiple_hashtags2 = gen_hashtags(['quux', '123', 'war&peace'])

        assert single_hashtag == '#test'
        assert single_hashtag2 == '#123'
        assert multiple_hashtags == '#foo #bar #baz'
        assert multiple_hashtags2 == '#quux #123 #war&peace'