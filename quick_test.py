#!/usr/bin/env python3
"""
快速测试脚本 - 不需要邮件配置
直接在终端显示 Google Trends 数据
"""

import sys
from querytrends import batch_get_queries
from config import KEYWORDS, TRENDS_CONFIG
import json

def main():
    print("=" * 70)
    print("Google Trends 快速测试")
    print("=" * 70)
    
    # 使用配置文件中的前3个关键词进行测试
    test_keywords = KEYWORDS[:3] if len(KEYWORDS) >= 3 else KEYWORDS
    
    if not test_keywords:
        print("\n❌ 错误: config.py 中没有配置关键词")
        print("请编辑 config.py 文件，在 KEYWORDS 列表中添加关键词")
        return
    
    print(f"\n测试关键词: {', '.join(test_keywords)}")
    print(f"时间范围: {TRENDS_CONFIG['timeframe']}")
    print(f"地区: {TRENDS_CONFIG['geo'] or '全球'}")
    print("\n正在查询数据...\n")
    
    try:
        # 查询趋势数据
        results = batch_get_queries(
            test_keywords,
            geo=TRENDS_CONFIG['geo'],
            timeframe=TRENDS_CONFIG['timeframe'],
            delay_between_queries=5
        )
        
        if not results:
            print("❌ 没有获取到数据")
            return
        
        # 显示结果
        print("\n" + "=" * 70)
        print("查询结果")
        print("=" * 70)
        
        for keyword, data in results.items():
            print(f"\n关键词: {keyword}")
            print("-" * 70)
            
            if data is None:
                print(f"  ❌ 未能获取数据")
                continue
            
            # 显示相关查询
            # 上升趋势
            if 'rising' in data and data['rising'] is not None:
                rising = data['rising']
                print(f"\n  📈 上升趋势 (共 {len(rising)} 条):")
                for i, row in enumerate(rising.head(5).itertuples(), 1):
                    value = row.value if hasattr(row, 'value') else 'N/A'
                    print(f"    {i}. {row.query} - 增长: {value}")
            else:
                print("\n  📈 上升趋势: 无数据")
            
            # 热门趋势
            if 'top' in data and data['top'] is not None:
                top = data['top']
                print(f"\n  🔥 热门趋势 (共 {len(top)} 条):")
                for i, row in enumerate(top.head(5).itertuples(), 1):
                    value = row.value if hasattr(row, 'value') else 'N/A'
                    print(f"    {i}. {row.query} - 热度: {value}")
            else:
                print("\n  🔥 热门趋势: 无数据")
        
        print("\n" + "=" * 70)
        print("✅ 测试完成！")
        print("=" * 70)
        print("\n提示:")
        print("1. 如果看到数据，说明程序运行正常")
        print("2. 接下来可以配置邮件通知")
        print("3. 或者继续调试微信通知")
        
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
