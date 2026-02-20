#!/usr/bin/env python3
"""
查看保存的 Google Trends 数据
"""

import os
import json
import pandas as pd
from datetime import datetime
from tabulate import tabulate

def list_data_directories():
    """列出所有数据目录"""
    dirs = [d for d in os.listdir('.') if d.startswith('data_') and os.path.isdir(d)]
    return sorted(dirs, reverse=True)

def view_csv_report(directory):
    """查看 CSV 报告"""
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    
    if not csv_files:
        print("没有找到 CSV 报告文件")
        return
    
    csv_file = os.path.join(directory, csv_files[0])
    df = pd.read_csv(csv_file)
    
    print(f"\n{'='*80}")
    print(f"CSV 报告: {csv_files[0]}")
    print(f"{'='*80}\n")
    
    # 按关键词分组显示
    for keyword in df['keyword'].unique():
        keyword_data = df[df['keyword'] == keyword]
        
        print(f"\n关键词: {keyword}")
        print("-" * 80)
        
        # 上升趋势
        rising = keyword_data[keyword_data['type'] == 'rising']
        if not rising.empty:
            print(f"\n📈 上升趋势 (共 {len(rising)} 条):")
            print(tabulate(
                rising[['related_keywords', 'value']].head(10).values,
                headers=['查询词', '增长值'],
                tablefmt='simple'
            ))
        
        # 热门趋势
        top = keyword_data[keyword_data['type'] == 'top']
        if not top.empty:
            print(f"\n🔥 热门趋势 (共 {len(top)} 条):")
            print(tabulate(
                top[['related_keywords', 'value']].head(10).values,
                headers=['查询词', '热度值'],
                tablefmt='simple'
            ))
        
        print()

def view_json_data(directory):
    """查看 JSON 数据"""
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    
    if not json_files:
        print("没有找到 JSON 数据文件")
        return
    
    print(f"\n{'='*80}")
    print(f"JSON 数据文件 (共 {len(json_files)} 个)")
    print(f"{'='*80}\n")
    
    for json_file in sorted(json_files):
        filepath = os.path.join(directory, json_file)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"\n文件: {json_file}")
        print(f"关键词: {data['keyword']}")
        print(f"时间: {data['timestamp']}")
        
        # 统计信息
        rising_count = len(data['related_queries']['rising']) if data['related_queries']['rising'] else 0
        top_count = len(data['related_queries']['top']) if data['related_queries']['top'] else 0
        
        print(f"上升趋势: {rising_count} 条")
        print(f"热门趋势: {top_count} 条")

def main():
    print("=" * 80)
    print("Google Trends 数据查看器")
    print("=" * 80)
    
    # 列出所有数据目录
    dirs = list_data_directories()
    
    if not dirs:
        print("\n没有找到数据目录")
        print("请先运行: python trends_monitor.py --test")
        return
    
    print(f"\n找到 {len(dirs)} 个数据目录:\n")
    for i, d in enumerate(dirs, 1):
        date_str = d.replace('data_', '')
        print(f"{i}. {d} ({date_str[:4]}-{date_str[4:6]}-{date_str[6:8]})")
    
    # 选择目录
    if len(dirs) == 1:
        selected_dir = dirs[0]
        print(f"\n自动选择: {selected_dir}")
    else:
        try:
            choice = input(f"\n请选择目录 (1-{len(dirs)}, 默认为最新): ").strip()
            if not choice:
                selected_dir = dirs[0]
            else:
                selected_dir = dirs[int(choice) - 1]
        except (ValueError, IndexError):
            print("无效的选择，使用最新目录")
            selected_dir = dirs[0]
    
    # 显示数据
    print(f"\n正在查看: {selected_dir}")
    
    while True:
        print("\n" + "=" * 80)
        print("选择查看方式:")
        print("1. 查看 CSV 报告（推荐）")
        print("2. 查看 JSON 数据文件信息")
        print("3. 切换到其他目录")
        print("0. 退出")
        print("=" * 80)
        
        choice = input("\n请选择 (0-3): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            view_csv_report(selected_dir)
        elif choice == '2':
            view_json_data(selected_dir)
        elif choice == '3':
            main()
            return
        else:
            print("无效的选择")
    
    print("\n感谢使用！")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户取消")
    except Exception as e:
        print(f"\n发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
