from aiogram.utils.keyboard import ReplyKeyboardBuilder


# def keyboard():
menu = ReplyKeyboardBuilder().button(text="Location 1").button(text="Location 2") \
.button(text="Location 3").button(text="Location 4").button(text="Location 5").as_markup()

    # builder.button(text="Location 1")
    # builder.button(text="Location 2")
    # builder.button(text="Location 3")
    # builder.button(text="Location 4")
    # builder.button(text="Location 5")

    # return builder.as_markup()

# menu = keyboard()