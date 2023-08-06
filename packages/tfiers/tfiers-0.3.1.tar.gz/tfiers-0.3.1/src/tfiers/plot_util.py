def figsize(
    aspect: float = 1.6,
    width: int = 500,
    rel_text_size: float = 1.33,
):
    """
    :param aspect:  Fig width / fig height.
    :param width:  Pixel width of figure.
    :param rel_text_size:  Determines how large text is relative to other plot elements,
                such as lines and ticks. (It is scaled so that it is "1" at the default
                dpi of 72).

    :return: A dictionary with keys "figsize" and "dpi" that can be passed as **kwargs
             to matplotlib figure creation methods.
    """
    dpi = 72 * rel_text_size  # = pixels per inch
    height = round(width / aspect)
    return dict(figsize=(width / dpi, height / dpi), dpi=dpi)
