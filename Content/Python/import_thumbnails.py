import unreal as ue
import os
import sys

def get_AssetPath(inAsset, includeTrailingBackslash=True):

	assetPath = inAsset.get_path_name()
	assetPath = assetPath.split(".")[0]

	assetPath = os.path.abspath(os.path.join(assetPath, os.pardir)).replace("C:", "")
	if includeTrailingBackslash:
		
		assetPath = assetPath + "\\"
	
	return assetPath
def get_files(file_dir):
    #for root, dirs, files in os.walk(file_dir):
        # print("root", root)  # 当前目录路径
        # print("dirs", dirs)  # 当前路径下所有子目录
        # print("files", files)  # 当前路径下所有非目录子文件
    files_local = []
    for file in os.listdir(file_dir):
        if os.path.splitext(file)[1] == '.txt':
            files_local.append(file)
if __name__ == '__main__':
    files_local = []
    log_str = "一键导出缩略图工具 || "
    print(log_str +"Start \n")
    save_path = "'C:\hiko_trunk\MainArt\Common\SpeedGame\Saved\Thumbnails\'"
    assets = ue.EditorUtilityLibrary.get_selected_assets()
    for asset in assets:
        assetPath = get_AssetPath(asset)
        assetPath += "'\Saved\'"
        asset_tools = ue.AssetToolsHelpers.get_asset_tools()
        stringtable = asset_tools.create_asset(asset_name = basename, package_path = package_path, asset_class = None, factory = unreal.StringTableFactory())