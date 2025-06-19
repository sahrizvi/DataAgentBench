input_path = "dataset/restaurant/image_review_all.json"
output_path = "dataset/restaurant/light_review.json"

num_lines = 2000  # 需要提取的行数

with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
    for i, line in enumerate(infile):
        if i >= num_lines:
            break
        outfile.write(line)

print(f"已保存前 {num_lines} 行到 {output_path}")
