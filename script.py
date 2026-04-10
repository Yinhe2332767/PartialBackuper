import json
import os
import shutil
import zipfile
import tempfile
from datetime import datetime
# 作者：Yinhe233，主要代码由豆包生成

lang = 'EN'
prt = True

def printer(cn, en):
    if lang == 'CN':
        print(cn)
    else: 
        print(en)

# --------------------------
# region 文件名生成函数
# --------------------------
def compile_regions(x1, z1, x2, z2):
    regions = []
    min_x = min(x1, x2) // 512
    max_x = max(x1, x2) // 512
    min_z = min(z1, z2) // 512
    max_z = max(z1, z2) // 512
    for x in range(min_x, max_x + 1):
        for z in range(min_z, max_z + 1):
            regions.append(f"r.{x}.{z}.mca")
    return regions

# --------------------------
# 从 JSON 读取配置
# --------------------------
def load_config(config_path="config.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg

# --------------------------
# 把 ignores / partials 展开为路径列表
# --------------------------
def build_paths(items):
    paths = []
    for item in items:
        # 直接路径字符串
        if isinstance(item, str):
            paths.append(item.replace("\\", "/"))
            continue

        # 文件夹+文件列表
        if isinstance(item, dict):
            if item.get("files") != None: 
                folder = item["folder"]
                files = item.get("files", [])
                for f in files:
                    p = os.path.join(folder, f).replace("\\", "/")
                    paths.append(p)
                continue
            else: # region 坐标
                folder = item["folder"]
                x1 = item["x1"]
                z1 = item["z1"]
                x2 = item["x2"]
                z2 = item["z2"]
                regions = compile_regions(x1, z1, x2, z2)
                for r in regions:
                    p = os.path.join(folder, r).replace("\\", "/")
                    paths.append(p)
                continue
            
    return paths

# --------------------------
# 复制：忽略 ignores 列表
# --------------------------
def smart_copy(src, dst, ignores):
    if not os.path.exists(src):
        return
    os.makedirs(dst, exist_ok=True)
    for root, dirs, files in os.walk(src, topdown=True):
        rel_path = os.path.relpath(root, src)
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(rel_path, d), ignores)]
        for file in files:
            file_rel = os.path.join(rel_path, file) if rel_path != "." else file
            if is_ignored(file_rel, ignores):
                continue
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst, file_rel)
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(src_file, dst_file)

def is_ignored(path, ignores):
    path = path.replace("\\", "/")
    for ig in ignores:
        ig = ig.replace("\\", "/")
        if path == ig or path.startswith(ig + "/"):
            return True
    return False

# --------------------------
# 按列表复制文件
# --------------------------
def copy_list(file_list, src_root, dst_root):
    for item in file_list:
        src = os.path.join(src_root, item)
        if not os.path.exists(src):
            continue
        dst = os.path.join(dst_root, item)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

# --------------------------
# 打包 ZIP
# --------------------------
def zip_folder(folder_path, output_zip):
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full = os.path.join(root, file)
                rel = os.path.relpath(full, folder_path)
                zf.write(full, rel)

# --------------------------
# 主入口
# --------------------------
def main(config_path):
    cfg = load_config(config_path)
    save_path = cfg.get("save_path", "")
    ignores_raw = cfg.get("ignores", [])
    partials_raw = cfg.get("partials", [])

    printer("读取到存档路径：", "Save path loaded: ")
    print(save_path)

    if not save_path or not os.path.isdir(save_path):
        printer("存档路径无效或不存在", "Save path not found.")
        return
    
    printer("开始备份...", "Starting backup...")

    ignore_list = build_paths(ignores_raw)
    partial_list = build_paths(partials_raw)

    # 把 partial 所在目录加入忽略，避免重复复制
    for p in partial_list:
        d = os.path.dirname(p)
        if d and d not in ignore_list:
            ignore_list.append(d)

    if prt:
        printer("\n===== 忽略路径 =====", "\n===== ignores =====")
        for p in ignore_list:
            print(p)

    if prt:
        printer("\n===== 部分复制 =====", "\n===== partials =====")
        for p in partial_list:
            print(p)

    with tempfile.TemporaryDirectory() as temp_dir:
        if prt:
            printer("\n正在复制基础文件（排除忽略项）...","Copying all not ignored...")
        smart_copy(save_path, temp_dir, ignore_list)

        if prt:
            print("正在复制部分备份文件...", "Copying partials...")
        copy_list(partial_list, save_path, temp_dir)

        tmark = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        zip_name = f"{save_path}_{tmark}_partial.zip"
        if prt:
            printer(f"正在打包：{zip_name}",f"Zipping up: {zip_name}")
        zip_folder(temp_dir, zip_name)

    printer(f"已完成打包{zip_name}", f"Zipping {zip_name} done.")

if __name__ == "__main__":
    glbcfg = load_config("global_config.json")
    lang = glbcfg.get("language")
    if lang == '中文' or lang == '中' or lang == '文': 
        lang = 'CN'
    else: 
        lang = 'EN'
    prt = glbcfg.get("print_full_process")
    files = os.listdir('configs')
    for file in files: 
        if os.path.splitext(file)[1] != '.json' or file == 'config_template.json': 
            continue
        printer(f'开始执行{file}配置指令',f'Start running with {file}')
        main(os.path.join('configs',file).replace("\\", "/"))
    printer('备份完成！','Backup complete!')