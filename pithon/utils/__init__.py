import io
import uuid

import matplotlib.pyplot as plt


def render_latex(latex_string):
    line_height_in = 20 / 72  # convert points to inches

    fig = plt.figure(figsize=(2.0, line_height_in + 1), dpi=300)
    plt.rcParams["text.usetex"] = True
    plt.text(0.5, 0.5, f"${latex_string}$", fontsize=20, ha="center", va="center")
    plt.axis("off")

    name = "imageCache/" + str(uuid.uuid4()) + ".png"
    plt.savefig(name, format="png", bbox_inches="tight", dpi=300, pad_inches=0.1)
    return name


# small test to see if it works
if __name__ == "__main__":
    render_latex(
        r"""\frac{\frac{9x}{\sqrt[3]{2}} \cdot \sin(\omega\epsilon)}{2}=\frac{\frac{1}{2} \cdot \frac{\sqrt{2}}{\sum_{n=0}^{399} n^2 + 19} \cdot \frac{1}{3}}{2}"""
    )
