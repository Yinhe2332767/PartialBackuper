=== save_path : 存档的路径，相对于script.py或绝对。
	例：自带的举例世界1，相对路径："./examples/instance1/world"
	例：mojang官方启动器默认存档路径下的"新的世界"存档："C:/users/name/AppData/Roaming/.minecraft/saves/新的世界"（*将name替换为你的电脑用户名）
	注：路径内不可有\，如有请手动替换为/

=== ignores : 忽略（不备份）的文件夹/文件。需填写存档往下的完整路径

        例：要忽视DH的保存文件，2.3.2-b-1.20.1版本默认位于 "存档/data/DistantHorizons.sqlite"，则在ignores中增加
		"data/DistantHorizons.sqlite"

        例：要忽略整个末地文件夹，默认位于 存档/DIM1，则同样增加
		"DIM1"

	例：要忽略备份玩家C*（uuid ooiiai）的数据，可使用ignores：（也可用partials实现）
		{
			"folder": "playerdata",
			"files": [
				"ooiiai.dat",
				"ooiiai.dat_old"
			]
		}

	例：要忽略包含主世界xz范围[-1024,-1024]到[1023,1023]区域的备份，填入（*若同一区域文件同时被ignores和partials包括，则优先遵循partials进行备份）
		{
			"folder": "region",
			"x1": -1024,
      			"z1": -1024,
      			"x2": 1023,
      			"z2": 1023
		}
        
=== partials : 部分备份文件夹。对于位于该目录下的文件夹将只备份标明的部分。同一文件夹可以填写多个备份范围。
        对于region即地形保存有特殊处理，输入坐标范围即可自动计算需要备份的region文件

        例：想要备份主世界xz坐标范围[-114,-514]到[415,411]和[1024,1024]到[2047, 2047]，则填写:（1.21之前）
		{
      			"folder": "regions",
      			"x1": -114,
      			"z1": -514,
      			"x2": 415,
      			"z2": 411
    		},
    		{
     			"folder": "region",
      			"x1": 1024,
      			"z1": 1024,
      			"x2": 2047,
      			"z2": 2047
    		}
        脚本将自动计算出需要备份的范围为r.-1.-2.mca到r.1.1.mca和r.2.2.mca到r.3.3.mca并复制备份。任何不在范围内的将不被复制。

        例：想要仅备份玩家A（uuid 114514）和玩家B（uuid 1919810）但不备份玩家C（uuid ooiiai）的数据，可使用partials：（也可用ignore实现） 
            	{
			"folder": "playerdata",
			"files": [
				"114514.dat",
				"114514.dat_old",
				"1919810.dat",
				"1919810.dat_old"
			]
		}

	同样可以使用"folder/file.ext"、"folder"格式

 * 以上仅为举例，请勿过度解读。


=== save_path : world folder path, relative to script.py or absolute. 
	Example: Example world 1 came with this package, relative to script.py: "./examples/instance1/world"
	Example: "New World" under the default save path of mojang official launcher: "C:/users/name/AppData/Roaming/.minecraft/saves/New World" (* Replace 'name' with your system username)
	Note: The path may not contain "\". If there are "\"s in your path, please replace with "/"

=== ignores: file and folders to be ignored in backup. Needs path relative to the world folder. 
	Example: To ignore Distant Horizons file (at world/data/DistantHorizons.sqlite as of version 2.3.2-b-1.20.1), add to ignores:
		"data/DistantHorizons.sqlite"

	Example: To ignore the entire end world (world/DIM1 before 1.21), add:
		"DIM1"

	Example: To ignore player C (uuid ooiiai) when backing up playerdata, add: 
		{
			"folder": "player_data",
			"files": [
				"ooiiai.dat",
				"ooiiai.dat_old"
			]
		}

	Example: To ignore overworld regions containing xz range [-1024,-1024] to [1023,1023], add: (* If the same region file is contained in both ignores and partials selection, will follow partials and do copy it)
		{
			"folder": "region",
			"x1": -1024,
      			"z1": -1024,
      			"x2": 1023,
      			"z2": 1023
		}

=== partials: files to be partially backed-up, ignoring rest in the folder. One folder can appear multiple times. 
	Has special settings about regions, which you can fill xz ranges and let the script auto compute which regions to backup

	Example: To backup overworld xz range [-114,-514] to [415,411] and [1024,1024] to [2047, 2047], fill in partials: (before 1.21)
		{
      			"folder": "region",
      			"x1": -114,
      			"z1": -514,
      			"x2": 415,
      			"z2": 411
    		},
    		{
     			"folder": "region",
      			"x1": 1024,
      			"z1": 1024,
      			"x2": 2047,
      			"z2": 2047
    		}
	And you should see region files r.-1.-2.mca ~ r.1.1.mca and r.2.2.mca ~ r.3.3.mca being copied, leaving the rest untouched. 
	
	Example: To backup only player A (uuid 114514) and player B (uuid 1919810) while not backingup player C (uuid ooiiai), you can fill in partials: (you can do this with ignored, too) 
		{
			"folder": "playerdata",
			"files": [
				"114514.dat",
				"114514.dat_old",
				"1919810.dat",
				"1919810.dat_old"
			]
		}

 * All above are for example only. Please do not interpret more than needed. 
