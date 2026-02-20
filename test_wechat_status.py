#!/usr/bin/env python3
"""
检查微信登录状态并测试发送消息
"""

import sys
from wechat_utils import WeChatManager
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    print("=" * 70)
    print("微信登录状态检查")
    print("=" * 70)
    
    manager = WeChatManager()
    
    # 检查登录状态
    print("\n正在检查登录状态...")
    if manager.check_login_status():
        print("✅ 微信已登录！")
        
        # 获取自己的信息
        import itchat
        my_info = itchat.search_friends()
        if my_info:
            print(f"\n你的微信信息:")
            print(f"  昵称: {my_info[0]['NickName']}")
            print(f"  备注名: {my_info[0].get('RemarkName', '无')}")
        
        # 测试发送消息
        print("\n" + "=" * 70)
        print("测试发送消息")
        print("=" * 70)
        
        choice = input("\n是否要测试发送消息到文件传输助手？(y/n): ").strip().lower()
        
        if choice == 'y':
            test_msg = "🤖 这是来自 Google Trends 监控工具的测试消息\n\n如果你看到这条消息，说明微信通知功能正常工作！"
            
            print("\n正在发送测试消息...")
            if manager.send_message(test_msg, 'filehelper'):
                print("✅ 消息发送成功！请检查你的文件传输助手")
            else:
                print("❌ 消息发送失败")
        
        print("\n" + "=" * 70)
        print("提示:")
        print("1. 微信登录状态已保存，下次运行时会自动登录")
        print("2. 可以在 .env 文件中配置 TRENDS_WECHAT_RECEIVER")
        print("3. 可以在 config.py 中设置通知方式为 'wechat' 或 'both'")
        print("=" * 70)
        
    else:
        print("❌ 微信未登录")
        print("\n尝试重新登录...")
        if manager.login(clean_cache=True):
            print("✅ 登录成功！")
        else:
            print("❌ 登录失败")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
