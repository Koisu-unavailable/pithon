from enum import Enum
import matplotlib.pyplot as plt
import io


def render_latex(latex_string):
    line_height_in = 20 / 72  # convert points to inches

    plt.figure(figsize=(2.0, line_height_in + 1), dpi=300)
    plt.rcParams["text.usetex"] = True
    plt.text(0.5, 0.5, f"${latex_string}$", fontsize=20, ha="center", va="center")
    plt.axis("off")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=300, pad_inches=0.1)
    buf.seek(0)
    return buf

class OPERATION_PRIORITIES(Enum):
    Exponent = 1
    """This can apply the any 'inplace' operation such as roots (technically exponenets) and factorials"""
    Multiplication = 2
    """Also applies to division"""
    Addition = 3
    """Also applies to subtraction"""

# small test to see if it works
if __name__ == "__main__":
    f = open("test.png", "wb")
    buf = render_latex(
        r"""\frac{\frac{9x}{\sqrt[3]{2}} \cdot \sin(\omega\epsilon)}{2}=\frac{\frac{1}{2} \cdot \frac{\sqrt{2}}{\sum_{n=0}^{399} n^2 + 19} \cdot \frac{1}{3}}{2}"""
    )
    f.write(buf.read())