import pandas as pd

df = pd.read_excel('ev1.xlsx')

# Dump all model outputs for manual review
lines = []
for i, row in df.iterrows():
    q = str(row['Question']).replace('**User**: ', '').strip()[:60]
    ans = str(row['ModelAnswer']).strip()
    if len(ans) < 20:
        continue
    lines.append(f"=== #{i} | {q}... ===")
    lines.append(f"[Rouge-L-F={row['Rouge-L-F']:.4f}]")
    lines.append(ans)
    lines.append("")

with open('all_outputs.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f"Dumped {len(lines)//3} samples to all_outputs.txt")
