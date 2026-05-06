def format_price(price: int | float | None) -> str:
    if price is None:
        return "未提供"

    return f"NT$ {int(price):,}"


def format_students(students: int | None) -> str:
    if students is None:
        return "未提供"

    return f"{int(students):,} 人"


def format_rating(rating: int | float | None) -> str:
    if rating is None:
        return "未提供"

    return f"{float(rating):.1f} ⭐"