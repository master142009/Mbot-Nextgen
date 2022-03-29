import os
from easy_pil import Editor, Canvas, Font, load_image


def get_card(data):
    profile_image = load_image(data["profile_image"])
    profile = Editor(profile_image).resize((150, 150)).circle_image()

    if data["bg_image"].startswith("http"):
        bg_image = load_image(data["bg_image"])
    else:
        bg_image = os.path.join(os.path.dirname(__file__), "assets", "bg.png")

        background = Editor(bg_image).resize((900, 300), crop=True)
        profile = load_image(data["profile_image"])

        profile = Editor(profile).resize((150, 150)).circle_image()
        
        square = Canvas((500, 500), "#06FFBF")
        square = Editor(square)
        square.rotate(30, expand=True)

        background.paste(square.image, (600, -250))
        background.paste(profile.image, (30, 30))

        background.rectangle((30, 220), width=650, height=40, fill="white", radius=20)
        background.bar(
            (30, 220),
            max_width=650,
            height=40,
            percentage=data["percentage"],
            fill="#FF56B2",
            radius=20,
        )
        background.text((200, 40), data["name"], font=Font.poppins(size=40), color="white")

        background.rectangle((200, 100), width=350, height=2, fill="#17F3F6")
        background.text(
            (200, 130),
            f"Level : {data['level']}"
            + f" XP : {data['xp']} / {data['level'] + 1) * 100}",
            font=Font.poppins(size=30),
            color="white",
        )

    return background.image_bytes
