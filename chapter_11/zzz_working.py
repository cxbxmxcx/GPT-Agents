import re

def wrap_latex(text):
    # Regex patterns for inline and block LaTeX
    inline_latex_pattern = r"(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)"
    block_latex_pattern = r"(?<!\$)\$\$(?!\$)(.*?)(?<!\$)\$\$(?!\$)"
    
    # Wrapping inline LaTeX with single $
    text = re.sub(inline_latex_pattern, r'$\1$', text)
    
    # Wrapping block LaTeX with double $$
    text = re.sub(block_latex_pattern, r'$$\1$$', text)
    
    return text

# Example text with LaTeX content
example_text = """
Here is some inline LaTeX: $E = mc^2$. And here is a block LaTeX:

$$
\int_{a}^{b} f(x) \,dx = F(b) - F(a)
$$

Here is another inline LaTeX $a^2 + b^2 = c^2$ and another block:

$$
f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!} (x - a)^n
$$
"""

wrapped_text = wrap_latex(example_text)
print(wrapped_text)
