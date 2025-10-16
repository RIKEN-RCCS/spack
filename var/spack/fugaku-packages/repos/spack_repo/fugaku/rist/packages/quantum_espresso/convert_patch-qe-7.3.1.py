import re

# 入出力ファイル名
input_file = "patch-qe-7.3.1"
output_file = "patch-qe-7.3.1.spack"

# 正規表現パターン
diff_pattern = re.compile(r'^(diff -ru )a/qe-7\.3\.1/(.+?) b/qe-7\.3\.1/(.+)$')
file_pattern = re.compile(r'^(---|\+\+\+) (a|b)/qe-7\.3\.1/(.+)$')

# 変換処理
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        # diff ヘッダ行の変換
        match_diff = diff_pattern.match(line)
        if match_diff:
            new_line = f"{match_diff.group(1)}a/{match_diff.group(2)} b/{match_diff.group(3)}\n"
            outfile.write(new_line)
            continue

        # --- や +++ のファイル行の変換
        match_file = file_pattern.match(line)
        if match_file:
            new_line = f"{match_file.group(1)} {match_file.group(2)}/{match_file.group(3)}\n"
            outfile.write(new_line)
            continue

        # その他の行はそのまま
        outfile.write(line)

print(f"変換完了: {output_file}")
