# Windows 从零复现 MuJoCable 肘关节绳驱动仿真

适用对象：首次配置 MuJoCable、希望在 VS Code 中查看和修改模型的 Windows 用户。教程版本：2026-09-20。

完成后，你将拥有一个独立 Python 环境，能运行四绳肘关节模型，观看“弯曲—返回—放绳”，导出 CSV、验证报告和视频，并知道后续修改哪些文件。

**主线：安装 VS Code → 安装 Python → 解压项目 → 创建虚拟环境 → 安装 MuJoCo → 加载绳插件 → 运行肘关节 → 导出结果。** 所有命令均在 Windows 原生环境执行，无需 WSL、Linux、Conda 或 C++ 编译器。

## 0. 先选对包，确认电脑条件

### 三种软件分别做什么

| 名称 | 在本项目中的作用 | 怎样获得 |
|---|---|---|
| VS Code | 编辑 Python、MJCF，运行与调试程序 | 下载 Windows 桌面安装程序 |
| Python | 执行仿真控制脚本 | 安装 Python 3.12.10 x64 |
| MuJoCo | 物理仿真引擎 | 在项目虚拟环境中用 pip 安装 3.4.0 |
| MuJoCable | 给 MuJoCo 增加绳索力学、表面绳路和收放绳能力 | 项目内的 Windows DLL，由 Python 加载 |
| 肘关节 demo | MJCF、网格、四根绳和控制程序 | 本教程项目包 |

**VS Code 的 Python 扩展与 MuJoCable 是两回事。** 前者在 VS Code 扩展面板安装；后者是 MuJoCo 的 DLL 插件，不在 VS Code 扩展商店安装。

### 电脑要求

- Windows 10/11，Intel 或 AMD 的 x64 处理器；在“设置 → 系统 → 关于 → 系统类型”查看。这里不使用 32 位 Python，也不是 Windows ARM64 原生包。
- 图形窗口和视频导出需要可用的 OpenGL 显卡驱动；无图形计算可以先独立检查。
- 安装 VS Code、Python 和 pip 依赖时联网。依赖装好后，运行当前模型不需要联网。
- 建议使用短英文目录，例如 `C:\work\elbow_demo`，避免深层目录和中文路径造成第三方文件接口问题。**不必放在 C 盘**；D 盘或 E 盘同样可以，例如 `D:\work\elbow_demo`。目录没有写权限时，换到自己可写的位置。

### 下载资源

| 资源 | 下载入口 | 说明 |
|---|---|---|
| VS Code | [官方下载页](https://code.visualstudio.com/download) | Windows → User Installer → x64 |
| Python 3.12.10 | [官方版本页](https://www.python.org/downloads/release/python-31210/) · [64 位安装程序](https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe) | 选 Windows installer (64-bit) |
| **本教程项目包** | [MuJoCable_Elbow_Windows_Project.zip](https://github.com/MuJoCable/mujocable.github.io/releases/download/windows-tutorial-v1/MuJoCable_Elbow_Windows_Project.zip) | 推荐用于学习与开发；包含模型、DLL、代码、VS Code 配置，不包含 Python |
| 快速体验包 | [MuJoCable_Windows_x64.zip](https://github.com/MuJoCable/mujocable.github.io/releases/download/windows-tutorial-v1/MuJoCable_Windows_x64.zip) | 自带 Python，解压即可体验，见第 13 节 |
| 单独插件包 | [MuJoCable_plugin_Windows_x64.zip](https://github.com/MuJoCable/mujocable.github.io/releases/download/windows-tutorial-v1/MuJoCable_plugin_Windows_x64.zip) | 已有其他 MuJoCo 项目时使用，见第 12 节 |
| 插件上游源码 | [MuJoCable v0.2.0 Release](https://github.com/MuJoCable/mujoco-cable-dynamics/releases/tag/v0.2.0) | 本 DLL 的源码来源，普通使用不需要自行编译 |

上表的项目包与插件包通过本网站仓库的 GitHub Release 分发。选择一种适合自己的包即可；学习和开发推荐本教程项目包。

当前 DLL 是“官方 v0.2.0 源码 + 肘关节圆柱绳路补丁”的 Windows x64 适配构建。源码、补丁与许可证随包提供；它不是官方原样预编译附件。项目包已经包含所需插件，不必同时下载另外两个包。

## 1. 下载并安装 VS Code

1. 打开 [VS Code 下载页](https://code.visualstudio.com/download)。选择 **Windows / User Installer / x64**。下载的是 `.exe` 桌面安装程序；本教程使用本地桌面软件。
2. 双击下载的 `VSCodeUserSetup-…-x64.exe`，按安装向导继续。User Installer 面向当前用户安装。
3. 如果安装选项中出现 **Add to PATH**，保留勾选；“使用 Code 打开目录”等右键菜单选项可按需要勾选。
4. 完成后启动 VS Code。若安装前已开终端，关闭并重新打开，使 PATH 更新生效。
5. 左侧点击四个方块的“扩展”图标，或按 `Ctrl+Shift+X`。搜索 `Python`，安装发布者为 **Microsoft**、标识为 `ms-python.python` 的扩展。
6. 确认 **Python Debugger** 扩展也已安装；后面 F5 调试会用到。若没有，搜索 Microsoft 的 `ms-python.debugpy` 安装。

**完成标志：** 可以打开 VS Code，扩展面板中的 Microsoft Python 显示已安装。此时还没有安装 Python 解释器，下一节继续。

参考：[VS Code 官方 Windows 安装说明](https://code.visualstudio.com/docs/setup/windows)、[Microsoft Python 扩展说明](https://marketplace.visualstudio.com/items?itemName=ms-python.python)。

## 2. 安装 Python 3.12.10（64 位）

为与已验证环境一致，本教程固定使用 Python 3.12.10 x64。它是复现基线，并不表示它是最新 Python 版本。

1. 打开 [Python 3.12.10 版本页](https://www.python.org/downloads/release/python-31210/)，在 Files 表格选择 **Windows installer (64-bit)**，文件名应为 `python-3.12.10-amd64.exe`。
2. 运行安装程序。第一页勾选 **Add python.exe to PATH**，然后选择 **Install Now**。保留 pip 和 Python launcher 的安装选项。
3. 等待安装完成，关闭并重新打开 VS Code。
4. 在 VS Code 顶部菜单选 **Terminal → New Terminal（终端 → 新建终端）**。下面会出现终端面板，选 PowerShell。
5. 输入下列命令，每行输完按回车：

```powershell
py -3.12 --version
py -3.12 -c "import struct; print(struct.calcsize('P') * 8)"
```

期望分别输出 `Python 3.12.10` 和 `64`。已经装有其他 Python 时，`py -3.12` 用来明确选择 3.12。

**不要下载 embeddable package 来完成这一节。** 本教程需要标准安装版提供的 pip 和 venv；此前免安装包内的嵌入式 Python 用途不同。

若 `py` 未被识别，先重开终端；仍不行，可检查 Python launcher 是否安装，或使用自己的 Python 完整路径。默认按用户安装时，常见路径为：

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" --version
```

这只是默认位置示例，若安装时选择了其他路径，应使用实际路径。

## 3. 解压项目，用 VS Code 打开正确目录

1. 下载本教程的 **MuJoCable_Elbow_Windows_Project.zip**。
2. 在资源管理器中右键 ZIP → **全部解压**。
3. 找到解压后真正包含 `run_demo.py` 的文件夹，将这个文件夹放到 `C:\work` 下并命名为 `elbow_demo`。
4. 打开 VS Code，选择 **File → Open Folder（文件 → 打开文件夹）**，选 `C:\work\elbow_demo`。
5. 只在确认项目来自上方链接的 MuJoCable 仓库后接受 VS Code 的工作区信任提示。

正确目录应是：

```text
C:\work\elbow_demo\
├─ .vscode\                    VS Code 解释器和调试配置
├─ requirements-windows.txt    固定版本的 Python 依赖
├─ check_mujoco.py             只检查基础 MuJoCo
├─ check_env.py                检查绳插件和肘关节
├─ mujocable_plugin.py         Windows DLL 加载器
├─ runtime.py                  项目模型加载入口
├─ run_demo.py                 肘关节控制与数据记录
├─ verify_results.py           与参考数据比较
├─ render_video.py             生成视频、GIF 和截图
├─ open_model.py               单滑轮/自有 XML 的通用查看器
├─ plugin\cable_unilateral.dll 绳驱动插件
├─ msvcp140.dll                项目本地 C++ 运行库
├─ vcruntime140.dll
├─ vcruntime140_1.dll
├─ model\elbow.xml             肘关节 MJCF
├─ model\assets\               已导出的模型网格
├─ examples\single_pulley.xml  简单滑轮例子
├─ reference\                  原有参考数据与视频
└─ validation\                 已完成测试的证据
```

以下使用 `C:\work\elbow_demo` 举例。如果项目在 D 盘，把 `Set-Location` 后的路径换成实际目录；后续以 `.\` 开头的命令不必改。VS Code、Python 和项目可以位于不同盘。

在新终端中输入：

```powershell
Set-Location C:\work\elbow_demo
Test-Path .\run_demo.py
Test-Path .\plugin\cable_unilateral.dll
```

两项应输出 `True`。如果为 `False`，先修正打开的目录，不要继续安装。项目根目录是有 `run_demo.py` 的那一级，不是它的父文件夹。

## 4. 创建项目专用虚拟环境

虚拟环境把本项目依赖放在 `.venv` 内，避免与其他实验混用。仍在上面的项目根目录运行：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -c "import sys; print(sys.executable)"
```

最后一行应显示 `C:\work\elbow_demo\.venv\Scripts\python.exe`。如果 `py` 不可用，可用上一节查到的标准 Python 完整路径替代第一行的 `py -3.12`。

**后面的命令统一显式调用 `.\.venv\Scripts\python.exe`。** 因此无需运行 `Activate.ps1`，也不用修改 PowerShell 执行策略。不要把命令前面终端自带的 `PS C:\…>` 一起复制进去。

在 VS Code 选择同一个解释器：

1. 按 `Ctrl+Shift+P`。
2. 输入并选择 **Python: Select Interpreter**。
3. 选择项目的 `.venv`；没看到时选 **Enter interpreter path（输入解释器路径）**，找到 `C:\work\elbow_demo\.venv\Scripts\python.exe`。

选择解释器决定 VS Code 使用哪个 Python；终端中的显式路径命令则始终指向我们指定的环境。[Python venv 文档](https://docs.python.org/3.12/library/venv.html)、[VS Code 环境选择文档](https://code.visualstudio.com/docs/python/environments)。

## 5. 安装 MuJoCo 及运行依赖

在项目终端依次执行；上一行成功完成后再执行下一行：

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install --only-binary=:all: -r .\requirements-windows.txt
.\.venv\Scripts\python.exe -m pip check
```

第二行会安装 **MuJoCo 3.4.0、NumPy 2.2.6、Pillow 11.3.0、imageio-ffmpeg 0.6.0** 等固定依赖。`--only-binary=:all:` 要求使用预编译 wheel，避免在用户电脑上意外进入编译流程。若没有匹配 wheel，先检查 Python 版本、位数和网络。

第三行正常情况下显示 `No broken requirements found.`。然后验证 MuJoCo 本体：

```powershell
.\.venv\Scripts\python.exe .\check_mujoco.py
```

正常输出包括：

```text
MuJoCo: 3.4.0
PASS: base MuJoCo advanced 100 steps; no cable plugin loaded.
```

这一步只运行一个简单球体，不加载绳插件，用于区分“MuJoCo 没装好”和“插件/模型没装好”。检查脚本会先添加项目本地运行库目录。

MuJoCo 的 Python wheel 已包含引擎库，不必另外下载桌面引擎或安装旧的 `mujoco-py`。本项目要求 3.4.0，不能直接升级后继续沿用该 DLL。[MuJoCo 官方 Python 安装说明](https://mujoco.readthedocs.io/en/3.4.0/python.html#installation)。

## 6. 安装与验证我们的 MuJoCable 插件

### 6.1 本教程采用项目本地安装

第 3 节解压项目后，插件文件已经放到位了：

- `plugin/cable_unilateral.dll`：Windows x64 绳插件。
- `mujocable_plugin.py`：先配置 DLL 搜索目录，再加载插件。
- 根目录三个运行库 DLL：保留在原位置，供新电脑使用。
- `runtime.py`：为本肘关节项目提供加载接口。

**无需再执行一个 MuJoCable 的 pip 安装命令，也不用把 DLL 复制进 Windows/System32。** 普通使用不要求注册表修改、管理员权限或本地编译。

### 6.2 先检查小模型，再检查肘关节

```powershell
.\.venv\Scripts\python.exe .\open_model.py .\examples\single_pulley.xml --check
.\.venv\Scripts\python.exe .\check_env.py
```

第一行应显示 `PASS`，表示一个绳插件实例运行了 1000 步。第二行检查肘关节，期望出现：

```json
{
  "passed": true,
  "mujoco": "3.4.0",
  "cables": 4,
  "actuators": 2
}
```

实际输出还包括 Python、NumPy、绳路状态和 DLL 哈希。完整报告保存到 `results/environment_check.json`。四根绳中两根主动驱动，另外两根为被动绳。

插件按进程加载，程序每次启动都要先加载 DLL，再编译含该插件的 XML；`runtime.py` 已替你完成。直接双击 XML，或把它拖到一个没有加载插件的普通 MuJoCo 查看器，可能出现 unknown plugin。

## 7. 运行肘关节驱动 demo

执行：

```powershell
.\.venv\Scripts\python.exe .\run_demo.py
```

稍等模型加载，弹出 MuJoCo 窗口。初次显示可能需要一点时间。程序通过两条驱动绳的收放控制关节运动，碰撞约束参与求解。

| 仿真时间 | 预期动作 |
|---|---|
| 0–0.5 s | 初始状态 |
| 0.5–12.5 s | 逐步大幅弯曲 |
| 12.5–14.5 s | 在最大弯曲附近保持 |
| 14.5–26.5 s | 返回原位 |
| 26.5–27.5 s | 原位短暂保持 |
| 27.5–29 s | 放松驱动绳 |
| 29–32 s | 保持放松，低张力绳变灰 |

控制目标是 180°，已有模型在接触限制下最大约 **178.8°**；不需要强行改关节位置达到 180°。灰色表示显示所用的绳张力低于 0.02 N，不表示绳模型被删除。

- **空格**：暂停/继续。
- **R**：重置并重新运行。
- **关闭窗口**：退出程序；32 s 仿真结束后窗口会自动暂停，但不会自动关闭。
- 32 s 指仿真时间，实际等待时间受电脑速度影响。

这一步用于交互观察。**图形模式本身不生成用于验收的 CSV；下一节用 `--headless` 正式记录结果。** 通用 `open_model.py model/elbow.xml` 也不会自动附带这个专用控制器，因此请用 `run_demo.py` 复现规定动作。

可先观看随包参考视频，比对整体动作：

<video controls preload="metadata" poster="media/elbow-maximum.png" src="media/elbow.mp4" aria-label="肘关节参考动作"></video>

如果创建 `.venv` 后移动了项目目录，请在新位置重新创建虚拟环境并安装依赖；不要直接跨目录或跨电脑复用旧 `.venv`。

### 在 VS Code 中按 F5 运行

项目已带 `.vscode/launch.json`。完成 `.venv` 和依赖安装后，打开左侧“运行和调试”，从下拉框选择 **Elbow demo**，按 F5。

还可以选 **Environment check / Elbow headless / Verify results / Single pulley**。这些配置明确使用项目 `.venv`。无须安装 Code Runner；它可能使用另一套解释器。

## 8. 运行完整计算并验收结果

先关闭交互窗口，在项目终端运行：

```powershell
.\.venv\Scripts\python.exe .\run_demo.py --headless
.\.venv\Scripts\python.exe .\verify_results.py
```

**第一行正常结束后再执行第二行。** 第一行每隔约 2 s 仿真时间打印阶段和角度，跑完 32 s 后写文件；第二行读取新结果，与随包参考数据比较。

主要输出：

| 文件 | 用途 |
|---|---|
| `results/motion.csv` | 约每 0.02 s 采样一次的角度、收绳量、张力、接触等 |
| `results/summary.json` | 最大弯曲、回位角度、放松后张力、警告等摘要 |
| `results/environment.json` | 实际 Python/MuJoCo/NumPy、模型与 DLL 哈希 |
| `results/verification.json` | 各验收条件与总的 `passed` 状态 |

验收参考：

| 指标 | 参考结果/验收标准 |
|---|---|
| 最大弯曲角 | 参考约 178.8146°；与参考差小于 1° |
| 返回原位 | 参考约 −0.0165°；绝对值小于 1° |
| 放松后主动绳张力 | 参考为 0 N；最大值小于 0.02 N |
| 完整时长 | 32 s，允许数值积分的微小浮点误差 |
| 整段角度曲线 RMSE | 与参考相比小于 2° |
| 动力学警告 | 无 |
| 接触代理最大穿透 | 小于 0.05 mm |
| 绳路状态 | 小于 2；原模型允许状态 1 |

通过时 `verification.json` 中 `"passed": true`，并列出 9 项判断。不同硬件可以有微小浮点差异，不能要求 CSV 逐字相同。失败时保留数据定位原因，不要先放宽阈值。

每次再次运行无图形计算会覆盖 `results` 内同名结果。做不同实验前，应把当前 `results` 复制为独立目录，例如 `experiments/baseline/results`；同时备份该次模型、控制脚本和 `environment.json`。

## 9. 导出视频、GIF 和截图

先完成第 8 节，确保当前 `results/motion.csv` 与你想展示的实验一致。以下命令用于 PowerShell：

```powershell
$env:ELBOW_FONT = "$env:WINDIR\Fonts\times.ttf"
$env:ELBOW_FONT_BOLD = "$env:WINDIR\Fonts\timesbd.ttf"
Test-Path $env:ELBOW_FONT
Test-Path $env:ELBOW_FONT_BOLD
```

两项都为 `True` 后执行：

```powershell
.\.venv\Scripts\python.exe .\render_video.py
```

如果只有普通体存在，可以把粗体路径也设为普通体，然后运行：

```powershell
$env:ELBOW_FONT_BOLD = $env:ELBOW_FONT
```

若普通体也不存在，需要先安装合法取得的 Times New Roman，或将两个环境变量设为自己已有字体的完整文件路径。教程不附带字体文件。

正常输出：

- `results/elbow_flexion.mp4`
- `results/elbow_flexion.gif`
- `results/maximum.png`、`return.png`、`release.png`

视频左边显示模型，右边以英文 Times New Roman 显示时间、弯曲角、四条绳张力和摩擦系数。FFmpeg 随 Python 依赖获得，无需另装系统版。

导出程序读取已保存的动力学记录来呈现画面；它不产生新的动力学实验。改过模型后要重新运行第 8 节，再导出视频，避免新模型配旧数据。

## 10. 看懂数据，找到修改位置

### CSV 的常用字段

| 字段 | 含义/单位 |
|---|---|
| `time_s`, `stage` | 仿真时间（s）和动作阶段 |
| `flexion_deg` | 便于阅读的正向弯曲角（°） |
| `upper_deg`, `lower_deg` | 两个内部关节坐标（°），符号遵循模型定义 |
| `02_ctrl_mm`, `03_ctrl_mm` | 两个主动绳的控制输入，记录为 mm |
| `02_tension_N`, `03_tension_N` | 两个主动绳张力（N） |
| `fixed_right_tension_N`, `fixed_left_tension_N` | 两个被动绳张力（N） |
| `*_length_mm`, `*_free_length_mm` | 绳路实际长度与自由长度（mm） |
| `contact_count`, `contact_normal_force_N` | 选定结构接触代理的接触数量与法向力统计 |
| `max_penetration_mm` | 当前采样时刻结构接触代理的最大穿透（mm） |
| `cable_friction_mu` | 演示记录的绳摩擦系数，本基线为 0 |

注意：程序内部长度单位通常是 m，CSV 的有关字段转换成了 mm。正向弯曲角与内部角度之和符号相反，画图优先使用 `flexion_deg`，不要将 `angle_deg` 误当作正向弯曲角。

### 文件与实验的关系

| 你想做什么 | 先看哪个文件 |
|---|---|
| 理解动作时间和驱动策略 | `run_demo.py` 中 `schedule()` 与 `Controller` |
| 查看滑轮、引导点、绳路和结构碰撞 | `model/elbow.xml` |
| 理解一个简单插件 MJCF | `examples/single_pulley.xml` |
| 检查模型加载或 DLL 路径 | `runtime.py`、`mujocable_plugin.py` |
| 修改显示视角和视频布局 | `render_video.py` |
| 查看原基线验收标准 | `verify_results.py` |
| 查看圆柱绳路适配改动 | `patches` 和 `source` |

**几何修改后不能直接假定原控制表仍然适用。** 当前 `Controller` 使用 `model/mobility_route_scan.json` 中的角度—绳长表；若修改滑轮位置、半径或绳路，需重新扫描并校准该表与控制策略。本项目包没有提供一键重建该扫描表的脚本。本教程先完成原样复现，不把几何修改后的失败自动归因于插件。

此外，当前记录代码将 `cable_friction_mu` 写为 0；若后续实际修改了摩擦，必须同步修改参数记录，不能只改图中文字或只改模型一处。

## 11. 常见问题：按这一顺序排查

| 现象 | 检查与处理 |
|---|---|
| `py` 不是可识别命令 | 重开终端，确认标准 Python 与 launcher 已安装；或用 Python 实际完整路径 |
| `.venv\Scripts\python.exe` 不存在 | 确认终端在项目根目录，重新检查第 4 节是否成功 |
| PowerShell 报 Activate.ps1 无法运行 | 跳过激活，直接使用教程中的 `.\.venv\Scripts\python.exe`；无需放宽执行策略 |
| `No module named mujoco` | 用同一 `.venv` 解释器执行 pip 安装；检查 VS Code 解释器选择 |
| pip 下载失败 | 检查网络、代理和当前软件源；先重试。不要关闭 TLS 校验；国内镜像可能暂未同步这些固定版本 |
| `No matching distribution` | 确认 Python 3.12、64 位和包版本；核对镜像是否有对应 wheel，不要随意删除版本约束 |
| MuJoCo 导入报 DLL load failed / WinError 126 | 确认项目根目录三个运行库 DLL 和插件文件完整；使用项目检查脚本。必要时通过[微软官方页面](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170)安装/修复 x64 VC++ 运行库，避免从不明站点补 DLL |
| `unknown plugin` / 找不到 `mujoco.cable.unilateral` | 必须先调用加载器，再编译 XML；用 `run_demo.py` 或 `open_model.py`，不要用未加载插件的普通查看器 |
| WinError 193 | 常见于位数或平台不匹配；核对 x64 Python、x64 Windows DLL，不能用 macOS `.dylib` 或 Linux `.so` |
| 找不到 mesh 文件 | 完整保留 `model/assets`；不要只复制 `elbow.xml` |
| 无图形计算正常，窗口打不开 | 更新显卡厂商驱动，检查本地桌面 OpenGL；远程桌面/虚拟机图形支持可能不同 |
| 视频导出说没有字体 | 按第 9 节设置字体变量并用 `Test-Path` 确认 |
| 视频内容还是上次实验 | `render_video.py` 读取已有 CSV；先重新计算并确认文件修改时间 |
| 模型只打开但不按规定弯曲 | 用 `run_demo.py`，通用查看器不包含肘关节控制策略 |
| 最大角度不是恰好 180° | 原基线约 178.8°，这是接触限制下的结果 |
| F5 报解释器不存在 | 确认打开了正确项目根目录，并已创建 `.venv` |

排错时先依次运行 `check_mujoco.py`、`open_model.py examples/single_pulley.xml --check`、`check_env.py`，可以分清问题出在引擎、插件还是肘模型。

反馈问题时附上报错终端原文与 `results/environment_check.json`；若计算完成但验收失败，再附 `summary.json`、`verification.json` 和 `motion.csv`。

## 12. 已有其他 MuJoCo 项目时，单独安装插件

这一节供已有环境的人使用；按前面主线操作的用户无需重复。

1. 下载并全部解压 [独立 DLL 插件包](https://github.com/MuJoCable/mujocable.github.io/releases/download/windows-tutorial-v1/MuJoCable_plugin_Windows_x64.zip)。
2. 用该项目自己的 64 位 Python 安装插件包的 `requirements.txt`，确保 MuJoCo 为 3.4.0。
3. 在插件包目录运行 `example.py`，先验证单滑轮。
4. 接入其他项目时保留插件包完整结构，并使 `mujocable_plugin.py` 所在目录进入 Python 模块搜索路径。下面示例假定此模块可以被 import：

```python
from mujocable_plugin import load_plugin
load_plugin()  # 必须先于含插件 XML 的编译
import mujoco

m = mujoco.MjModel.from_xml_path("your_model.xml")
d = mujoco.MjData(m)
```

自己的 MJCF 还需定义 `mujoco.cable.unilateral` 插件实例、端点/引导点、包络几何及驱动器，不能仅凭安装 DLL 就自动生成绳子。控制输入单位由模型配置决定；`examples/single_pulley.xml` 使用 target_contraction，正值为收绳量，单位 m。

## 13. 只想先看效果：免安装包路线

下载 [MuJoCable_Windows_x64.zip](https://github.com/MuJoCable/mujocable.github.io/releases/download/windows-tutorial-v1/MuJoCable_Windows_x64.zip)，全部解压，然后：

1. 双击 `CHECK_ENV.cmd`，检查 `passed: true`。
2. 双击 `START_ELBOW.cmd`，观看运动。
3. 双击 `RUN_HEADLESS.cmd`，输出和核验结果。
4. 双击 `EXPORT_VIDEO.cmd`，导出视频。

这一路线无需安装 VS Code 或 Python。包中的 `.cmd` 固定使用内置 `python/python.exe`；本教程主线使用项目 `.venv`。两者不要混用来判断自己新建的环境是否安装成功。

可以用 VS Code 阅读免安装包的代码，但其嵌入式 Python 不适合作为本教程创建 venv、安装开发依赖的起点。需要持续改模型、做实验时，使用前面的项目包主线。

## 14. 复现检查清单

- `check_mujoco.py` 显示 MuJoCo 3.4.0，基础动力学检查通过。
- `check_env.py` 显示 4 个绳插件、2 个驱动器及 `passed: true`。
- 观看并确认“弯曲—返回—放松变灰”完整动作。
- 保存 `motion.csv`、`summary.json`、`environment.json`、`verification.json`；原样复现验收通过。
- 导出 MP4 和最大角度截图，保留实验版本与日期。
- 记录是否改动模型或脚本；原样基线先单独保留，再开始参数实验。

## 15. 已验证内容与模型边界

此前 Windows x64 DLL、官方 Windows Python/MuJoCo 运行时已在 macOS 的 Wine 11.0 兼容层中通过 32 s 动力学、单滑轮、图形窗口和视频导出测试；最大弯曲约 178.8146°。详细记录在 `validation`。当前教程开发项目也已通过基础 MuJoCo、单滑轮、肘关节自检与完整 32 s 结果比较，详见 `validation/project_guide_checks.json` 和 `project_rollout_verification.json`。测试使用独立 Windows Python，并检查了项目本地运行库加载；未实际执行标准 Python 安装程序、venv 创建和 VS Code 图形操作。

**尚未完成原生 Windows 10/11 真机的安装和 GUI 验收。** VS Code 和标准 Python 安装步骤依据官方文档整理；兼容层测试不能替代所有 Windows 显卡、驱动及系统策略下的确认。Wine 视频测试曾有 OpenGL 0x506 上下文警告，但输出完成并检查了截图。

当前演示重力为零、绳路摩擦系数为零，绳路状态 1 按原模型阈值接受。它用于复现运动与控制流程；放绳后低张力不能独立证明真实负载下的机械自锁，也不是“最大负载—角度曲线”的测量实验。后续负载研究需要另外定义重力、外载荷、驱动上限和验收条件。

文档依据已在对应步骤链接：VS Code Windows 安装与 Python 环境文档、Python 3.12.10 安装资源与 venv 文档、MuJoCo 3.4.0 Python 文档；本项目版本、二进制哈希和补丁来源见 `BUILD_MANIFEST.json`。
