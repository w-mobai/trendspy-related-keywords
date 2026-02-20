#!/bin/bash
# Google Trends 监控工具 - 一键运行脚本

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 激活虚拟环境
source venv/bin/activate

# 显示菜单
echo "========================================"
echo "Google Trends 监控工具"
echo "========================================"
echo ""
echo "请选择操作："
echo "1. 快速测试（3个关键词）"
echo "2. 完整测试（所有关键词）"
echo "3. 查看已保存的数据"
echo "4. 运行定时任务"
echo "0. 退出"
echo ""
read -p "请输入选项 (0-4): " choice

case $choice in
    1)
        echo ""
        echo "正在运行快速测试..."
        python quick_test.py
        ;;
    2)
        echo ""
        echo "正在运行完整测试..."
        python trends_monitor.py --test
        ;;
    3)
        echo ""
        python view_data.py
        ;;
    4)
        echo ""
        echo "启动定时任务（每天 23:05 自动运行）"
        echo "按 Ctrl+C 可以停止"
        python trends_monitor.py
        ;;
    0)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效的选项"
        exit 1
        ;;
esac

# 保持终端打开
echo ""
read -p "按回车键退出..."
