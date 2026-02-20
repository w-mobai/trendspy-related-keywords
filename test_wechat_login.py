#!/usr/bin/env python3
"""
微信登录测试脚本
使用说明：
1. 运行脚本后会显示二维码
2. 用微信扫描二维码
3. 在手机上点击"登录"按钮（注意：必须在30秒内点击）
4. 登录成功后会显示你的微信昵称
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wechat_utils import WeChatManager
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    print("=" * 60)
    print("微信登录测试")
    print("=" * 60)
    print("\n重要提示：")
    print("1. 扫描二维码后，请在 30 秒内点击手机上的'登录'按钮")
    print("2. 如果超时，程序会自动重新生成二维码")
    print("3. 按 Ctrl+C 可以随时退出\n")
    print("=" * 60)
    
    manager = WeChatManager()
    
    # 尝试登录
    if manager.login(max_retries=5, clean_cache=True):
        print("\n" + "=" * 60)
        print("✅ 登录成功！")
        print("=" * 60)
        
        # 获取自己的信息
        import itchat
        my_info = itchat.search_friends()
        if my_info:
            print(f"\n你的微信昵称: {my_info[0]['NickName']}")
            print(f"备注名: {my_info[0].get('RemarkName', '无')}")
        
        print("\n登录状态已保存，下次运行时可以自动登录")
        print("=" * 60)
        return True
    else:
        print("\n" + "=" * 60)
        print("❌ 登录失败")
        print("=" * 60)
        print("\n可能的原因：")
        print("1. 扫码后没有及时点击'登录'按钮")
        print("2. 网络连接问题")
        print("3. 微信版本不兼容")
        print("\n建议：")
        print("1. 重新运行脚本")
        print("2. 确保网络连接正常")
        print("3. 扫码后立即点击手机上的'登录'按钮")
        print("=" * 60)
        return False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户取消登录")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
