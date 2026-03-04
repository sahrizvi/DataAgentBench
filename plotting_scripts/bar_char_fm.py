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
    "FM1": [0, 0, 64, 1713, 0],
    "FM1-4": [1879, 1721, 1526, 678, 1744],
    "FM5": [1, 21, 3, 16, 178],
    "Successful runs": [820, 958, 1107, 293, 778]
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

categories = ["FM1", "FM1-4", "FM5", "Successful runs"]
colors = ["#0000a2", "#bc272d", "#e9c716", "#50ad9f"]

left = np.zeros(len(df_percent))

for category, color in zip(categories, colors):
    if category == 'FM1':
        cname = "FM1 (no_tool_call)"
    elif category == "FM1-4":
        cname = "FM1 (other), FM2, FM3, FM4"
    elif category == "Successful runs":
        cname = "Successful trials"
    else:
        cname = category
    ax.barh(
        df_percent.index,
        df_percent[category],
        left=left,
        label=cname,
        color=color,
        # edgecolor='black',
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
ax.set_title("Frequencies of All Failure Modes", pad=40, fontsize=14, loc='right')
ax.tick_params(axis='y', labelsize=13)
ax.tick_params(axis='x', labelsize=12)
# Move legend fully outside (top center)
ax.legend(
    loc="lower center",
    bbox_to_anchor=(0.28, 0.91),
    ncol=2,
    frameon=False,
    fontsize=12,
    # set interval between legend entries
    columnspacing=0.5,
)

# Remove extra whitespace
plt.tight_layout(pad=0)
plt.subplots_adjust(top=0.8)   # ensure space for legend
plt.margins(x=0, y=0.1)

# plt.tight_layout()
plt.savefig("figures/fm_freq.pdf")
