from icon_loader import load_icon


def test_something():
    icon = load_icon('local_florist')
    assert icon is not None
