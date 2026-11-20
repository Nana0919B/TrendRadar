# coding=utf-8
"""
TrendRadar - 热点新闻聚合与分析工具

使用方式:
  python -m trendradar        # 模块执行
  trendradar                  # 安装后执行
"""

__version__ = "6.11.0"
__all__ = ["AppContext", "__version__"]


def __getattr__(name):
    # Collection/storage users should not need the optional AI runtime.
    if name == "AppContext":
        from trendradar.context import AppContext

        globals()[name] = AppContext
        return AppContext
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
