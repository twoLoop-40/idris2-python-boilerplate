"""
Converted from Idris2 func.idr
Original Idris2 code:
    private helperFunction: Int -> Int
    helperFunction x = x + 1

    public apiFunction : Int -> Int
    apiFunction x = helperFunction x * 2
"""


def _helper_function(x: int) -> int:
    """
    Private helper function.
    Adds 1 to the input value.

    Args:
        x: An integer value

    Returns:
        x + 1
    """
    return x + 1


def api_function(x: int) -> int:
    """
    Public API function.
    Applies helper function and multiplies result by 2.

    Args:
        x: An integer value

    Returns:
        (x + 1) * 2
    """
    return _helper_function(x) * 2


if __name__ == "__main__":
    # Example usage
    result = api_function(5)
    print(result)
