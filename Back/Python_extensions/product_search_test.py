import json
import os
import numpy as np
from Back.Python_extensions.utils.database.faiss_database import FaissDatabase
from Back.Python_extensions.utils.encode.encode_text import TextEncoder  # 导入真实编码器

# 加载配置文件
with open('config/config.json') as f:
    config = json.load(f)

# 数据库配置
bin_path = config["product_data"]["bin"]
npy_path = config["product_data"]["npy"]
model_path = config["model_path"]["product_model"]

# 全局商品信息存储
product_details = {}


# ----------------- 初始化编码器和数据库 -----------------
def init_system():
    """初始化系统（带异常捕获）"""
    try:
        # 清理旧测试数据
        if os.path.exists(bin_path): os.remove(bin_path)
        if os.path.exists(npy_path): os.remove(npy_path)

        # 初始化组件
        encoder = TextEncoder(model_path)
        database = FaissDatabase(
            dim=384,
            index_path=bin_path,
            id_map_path=npy_path,
            index_type="L2",
            normalize=False
        )
        return encoder, database
    except Exception as e:
        print(f"❌ 系统初始化失败: {str(e)}")
        exit(1)


encoder, database = init_system()


# ----------------- 增强版测试用例 -------------------
def test_add_product(id: int, description: str):
    """测试添加商品（带数据验证）"""
    try:
        # 数据验证
        if not isinstance(id, int):
            raise ValueError("ID必须是整数")
        if id in product_details:
            raise ValueError(f"重复ID: {id}")
        if len(description) < 5:
            raise ValueError("描述至少需要5个字符")

        # 编码和存储
        vector = encoder.encode(description)
        if vector.shape != (384,):
            raise ValueError(f"无效向量维度: {vector.shape}")

        database.add_item(vector, id)
        product_details[id] = {
            "description": description,
            "vector_norm": round(np.linalg.norm(vector), 2)
        }
        print(f"✅ 添加成功: ID={id} | 描述: {description[:30]}...")
    except Exception as e:
        print(f"❌ 添加失败 [ID:{id}]: {str(e)}")


def test_search_products(keyword: str,threshold=0.7):
    """增强版搜索测试（带详情展示）"""
    try:
        query_vec = encoder.encode(keyword)
        results = database.search(query_vec, top_k = 5,threshold=threshold)

        print(f"\n🔍 搜索: '{keyword}' | 阈值={threshold}")
        print(f"找到 {len(results)} 个匹配商品:")

        # 假设 results 是纯 ID 列表
        for i, product_id in enumerate(results, 1):
            detail = product_details.get(product_id, {})
            print(f"{i}. ID: {product_id}")
            print(f"   描述: {detail.get('description', '未知')}")

        return results
    except Exception as e:
        print(f"❌ 搜索失败: {str(e)}")
        return []


def print_all_products():
    """打印所有已存储商品"""
    print("\n📦 当前数据库商品列表:")
    for pid, detail in product_details.items():
        print(f"ID: {pid} | 描述: {detail['description'][:40]}...")
    print(f"总计 {len(product_details)} 个商品")

# 添加语义相似度验证方法
def test_similarity( text1: str, text2: str):
    v1 = encoder.encode(text1)
    v2 = encoder.encode(text2)
    return np.dot(v1, v2)


print(test_similarity("游戏键盘", "电竞设备"))  # 预期: 0.82-0.88
print(test_similarity("游戏键盘", "测试商品"))  # 预期: 0.1-0.3
print(test_similarity("苹果", "水果"))        # 预期: 0.6-0.7 (多义词场景)
print(test_similarity("苹果", "iPhone"))     # 预期: 0.75-0.85

# ----------------- 主程序 -------------------
if __name__ == "__main__":

    # 扩展测试数据
    test_cases = [
        (1001, "无线蓝牙耳机 主动降噪 30小时续航 Hi-Res音质 触控操作"),
        (1002, "防水运动耳机 IPX7等级 耳挂式设计 16小时续航 磁吸充电"),
        (1003, "智能运动防水手表 心率监测 GPS定位 50米防水 血氧检测 运动模式"),
        (1004, "4K高清摄像机 光学防抖 30倍变焦 无线直播 人脸追踪"),
        (1005, "专业单反相机 全画幅传感器 4K视频拍摄 五轴防抖 双卡槽"),
        (1006, "便携式投影仪 1080P高清 自动对焦 内置电池 手机同屏"),
        (1007, "无人机 4K相机 GPS定位 智能避障 30分钟续航 手势控制"),
        (1008, "机械键盘 RGB背光 青轴 有线游戏键盘 全键无冲 金属面板"),
        (1009, "电竞鼠标 16000DPI 6个可编程按钮 RGB灯光 人体工学设计"),
        (1010, "降噪耳机 混合主动降噪 无线充电 智能佩戴检测 LDAC编码"),
    ]

    # 阶段1：添加商品测试
    print("=== 添加测试 ===")
    for pid, desc in test_cases:
        test_add_product(pid, desc)

    # 显示所有有效商品
    print_all_products()

    # 阶段2：多维度搜索测试
    print("\n=== 搜索测试 ===")
    test_search_products("防水耳机手表", threshold=0.8)
    # test_search_products("摄影器材", threshold=0.7)
    # test_search_products("电竞外设", threshold=0.75)
    # test_search_products("不存在商品", threshold=0.9)

    # 阶段3：边界测试
    # print("\n=== 边界测试 ===")
    # test_search_products("", threshold=0)  # 空搜索
    # test_search_products("a" * 100, threshold=0.5)  # 长搜索文本
