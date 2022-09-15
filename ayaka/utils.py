import re
import importlib
from pathlib import Path
import uvicorn
from .adapter import logger


# 启动服务
def run(host="127.0.0.1", port=19900, reload=True):
    uvicorn.run(
        app=f"{__name__}:server_app",
        host=host,
        port=port,
        reload=reload,
    )


# 导入模块
def import_plugin(module_name: str):
    try:
        importlib.import_module(module_name)
        logger.success(f"<y>{module_name}</y> 导入成功")
    except:
        logger.exception(f"<y>{module_name}</y> 导入失败")


def import_plugins(path):
    path = Path(path)
    for p in path.iterdir():
        name = p.name
        if name.startswith("_") or name.startswith("."):
            continue

        if not p.is_dir():
            if p.suffix == ".py":
                p = p.with_suffix("")
            else:
                continue

        module_name = re.sub(r"\\|/", ".", str(p))
        import_plugin(module_name)
