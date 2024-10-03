from icon_loader import load_icon


def test_something():
    icon = load_icon('local_florist')
    assert icon is not None


if __name__ == '__main__':
    test_something()