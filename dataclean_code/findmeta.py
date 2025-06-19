import json

# 文件路径
review_path = "dataset/googlelocal/light_review.json"
meta_path = "dataset/googlelocal/meta-California.json"
output_meta_path = "dataset/googlelocal/light_meta.json"

# 读取light_review中的gmap_id
gmap_ids = set()
with open(review_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            entry = json.loads(line)
            gmap_ids.add(entry["gmap_id"])
        except:
            continue

print(f"✅ 从light_review中提取了 {len(gmap_ids)} 个唯一gmap_id")

# 遍历meta文件并匹配gmap_id
matched_meta = []
with open(meta_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            entry = json.loads(line)
            if entry.get("gmap_id") in gmap_ids:
                matched_meta.append(line)
                if len(matched_meta) >= len(gmap_ids):
                    break  # 可选优化：提前退出
        except:
            continue

# 保存结果
with open(output_meta_path, "w", encoding="utf-8") as f:
    f.writelines(matched_meta)

print(f"✅ 已将匹配的 {len(matched_meta)} 条meta数据保存到 {output_meta_path}")
