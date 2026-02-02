import os

# 设置要搜索的根目录（"." 表示当前目录及以下所有内容）
root_directory = "."

print(f"🔍 正在从目录 [{os.path.abspath(root_directory)}] 开始全库扫描...")

fixed_count = 0
scanned_count = 0

# os.walk 会递归遍历每一层目录
for dirpath, dirnames, filenames in os.walk(root_directory):
    
    # 过滤掉隐藏文件夹 (如 .ipynb_checkpoints, .git)，避免修改系统文件
    dirnames[:] = [d for d in dirnames if not d.startswith('.')]
    
    for filename in filenames:
        # 只处理 .py 文件
        if filename.endswith(".py"):
            file_path = os.path.join(dirpath, filename)
            scanned_count += 1
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # 判定逻辑：
                # 1. 文件里包含 "test = {" (这是 Otter 测试文件的特征)
                # 2. 文件里还没有 "OK_FORMAT" (说明是旧文件)
                if "test = {" in content and "OK_FORMAT" not in content:
                    
                    # 在文件开头添加补丁
                    new_content = "OK_FORMAT = True\n" + content
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                        
                    print(f"✅ 已修复: {file_path}")
                    fixed_count += 1
                    
            except Exception as e:
                print(f"⚠️ 无法读取/写入文件 {file_path}: {e}")

print("\n" + "="*30)
print(f"🎉 扫描完成！")
print(f"共扫描 Python 文件: {scanned_count} 个")
print(f"共修复 Otter 测试文件: {fixed_count} 个")
print("现在你可以放心地运行任意课程作业了！")
print("="*30)