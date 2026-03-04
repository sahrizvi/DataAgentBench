import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# -------------------------
# Data
# -------------------------
data = {
    "Model": [
        "GPT-5.2",
        "GPT-5-mini",
        "Gemini-3-Pro",
        "Gemini-2.5-Flash",
        "Kimi-K2"
    ],
    "FM1": [0, 0, 0, 0, 0],
    "FM2": [85, 96, 84, 82, 119],
    "FM3": [40, 37, 32, 33, 28],
    "FM4": [116, 100, 102, 88, 109],
}

df = pd.DataFrame(data)
df.set_index("Model", inplace=True)

# -------------------------
# Convert to percentage
# -------------------------
df_percent = df.div(df.sum(axis=1), axis=0) * 100

# -------------------------
# Plot
# -------------------------
fig, ax = plt.subplots(figsize=(5, 2.3))
ax.set_aspect(6)

categories = ["FM1", "FM2", "FM3", "FM4"]
colors = ["#707070", "#a00000", "#c46666", "#d8a6a6"]
hatches = [None, '//','xx', '\\\\']

left = np.zeros(len(df_percent))

for category, color, hatch in zip(categories, colors, hatches):
    ax.barh(
        df_percent.index,
        df_percent[category],
        left=left,
        label=category if category != "FM1" else "FM1 (other)",
        color=color,
        hatch=hatch
    )
    left += df_percent[category]

# # Formatting
# ax.set_xlim(0, 100)
# ax.set_xlabel("Percentage (%)")
# ax.set_title("Frequencies of Failure Modes")
# ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=4)


# Formatting
ax.set_xlim(0, 100)
ax.set_xticks([i*10 for i in range(11)])
ax.set_xlabel("Percentage (%)", labelpad=2, fontsize=13)
# set the distance of title from the left margin
ax.set_title("Frequencies of FM1 (other), FM2, FM3, and FM4\namong sampled trajectories", pad=20, fontsize=14, loc='right')
ax.tick_params(axis='y', labelsize=13)
ax.tick_params(axis='x', labelsize=12)

# Move legend fully outside (top center)
ax.legend(
    loc="lower center",
    bbox_to_anchor=(0.36, 0.87),
    ncol=len(categories),
    frameon=False,
    fontsize=12,
    columnspacing=0.5,
)

# Remove extra whitespace
plt.tight_layout(pad=0)
plt.subplots_adjust(top=0.82)   # ensure space for legend
plt.margins(x=0, y=0.1)

# plt.tight_layout()
plt.savefig("figures/fm234_freq.pdf")
