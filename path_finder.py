from collections import deque


class V:
    def __init__(self, data):
        self.data = data
        self.neighbs = list()
        self.depth = -1

    def __str__(self):
        return '%s %d' % (self.data, self.depth)


class PathFinder:
    def __init__(self, words):
        self.words = words

    def find_path(self, word_a, word_b):
        assert isinstance(word_a, str) and isinstance(word_b, str)
        if len(word_a) != len(word_b):
            return -1
        if len(word_a) == 0:
            return 0
        if word_a == word_b:
            return 0
        word_a_v = self._get_word_graph(word_a)
        assert isinstance(word_a_v, V)
        q = deque(word_a_v.neighbs)
        while not len(q) == 0:
            v = q.pop()
            if v.data == word_b:
                return v.depth
            if self._close_enough(v.data, word_b):
                return v.depth + 1
            for neighb in v.neighbs:
                assert isinstance(neighb, V)
                if neighb.depth < v.depth:
                    continue
                q.append(neighb)
        return -1

    def _get_word_graph(self, word, depth=0, visited=None):
        if visited is None:
            visited = dict()
        if word in visited:
            return visited[word]
        v = V(word)
        v.depth = depth
        visited[word] = v
        for w in self.words:
            if w == word:
                continue
            if self._close_enough(w, word):
                v.neighbs.append(self._get_word_graph(w, depth+1, visited))

        return v

    @staticmethod
    def _close_enough(word_a, word_b):
        assert isinstance(word_a, str) and isinstance(word_b, str)
        distance = 0
        for i in range(len(word_a)):
            if word_a[i] != word_b[i]:
                distance += 1
            if distance >= 2:
                return False
        return True


def test(word_a, word_b, expected_res, path_finder):
    steps = path_finder.find_path(word_a, word_b)
    print("%s-->%s reachable within %d steps" % (word_a, word_b, steps))
    assert steps == expected_res


def main():
    words = ['hot', 'pot', 'hit', 'har', 'hog', 'fog']
    path_finder = PathFinder(words)

    # word b not in words
    test('hot', 'dog', 2, path_finder)
    # word b not in words longer
    test('hot', 'for', 3, path_finder)
    # both in words short path
    test('hot', 'hit', 1, path_finder)
    # word a not in words
    test('hir', 'hit', 1, path_finder)
    # no path
    test('hot', 'har', -1, path_finder)
    # same word
    test('hot', 'hot', 0, path_finder)


if __name__ == "__main__":
    main()
