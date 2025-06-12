// 模拟产品数据
export const products = [
  {
    id: 1,
    title: "计算机网络教材",
    description: "九成新，只翻阅过几次，无笔记",
    price: 25,
    category: "书籍",
    images: ["https://images.pexels.com/photos/159711/books-bookstore-book-reading-159711.jpeg"],
    seller: {
      id: 101,
      username: "zhang_san",
      avatar: "https://images.pexels.com/photos/614810/pexels-photo-614810.jpeg"
    },
    createdAt: "2023-05-10T08:30:00Z"
  },
  {
    id: 2,
    title: "二手iPad 2020",
    description: "iPad 2020款，128G，无划痕，配充电器和保护套",
    price: 1800,
    category: "电子",
    images: ["https://images.pexels.com/photos/1334597/pexels-photo-1334597.jpeg"],
    seller: {
      id: 102,
      username: "li_si",
      avatar: "https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg"
    },
    createdAt: "2023-05-12T14:20:00Z"
  },
  {
    id: 3,
    title: "耐克运动鞋",
    description: "Nike Air系列，43码，穿过几次，状态良好",
    price: 280,
    category: "服装",
    images: ["https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg"],
    seller: {
      id: 103,
      username: "wang_wu",
      avatar: "https://images.pexels.com/photos/1681010/pexels-photo-1681010.jpeg"
    },
    createdAt: "2023-05-15T10:45:00Z"
  },
  {
    id: 4,
    title: "宿舍小台灯",
    description: "可充电台灯，三档亮度调节，使用3个月",
    price: 35,
    category: "生活",
    images: ["https://images.pexels.com/photos/1112598/pexels-photo-1112598.jpeg"],
    seller: {
      id: 101,
      username: "zhang_san",
      avatar: "https://images.pexels.com/photos/614810/pexels-photo-614810.jpeg"
    },
    createdAt: "2023-05-18T16:30:00Z"
  },
  {
    id: 5,
    title: "高等数学教材",
    description: "大一高数教材，含习题解析，有少量笔记",
    price: 20,
    category: "书籍",
    images: ["https://images.pexels.com/photos/4439901/pexels-photo-4439901.jpeg"],
    seller: {
      id: 104,
      username: "zhao_liu",
      avatar: "https://images.pexels.com/photos/1516680/pexels-photo-1516680.jpeg"
    },
    createdAt: "2023-05-20T09:15:00Z"
  },
  {
    id: 6,
    title: "小米蓝牙音箱",
    description: "小米方盒子蓝牙音箱，音质好，电池续航长",
    price: 65,
    category: "电子",
    images: ["https://images.pexels.com/photos/1279107/pexels-photo-1279107.jpeg"],
    seller: {
      id: 105,
      username: "chen_qi",
      avatar: "https://images.pexels.com/photos/1043471/pexels-photo-1043471.jpeg"
    },
    createdAt: "2023-05-22T11:50:00Z"
  },
  {
    id: 7,
    title: "自行车",
    description: "捷安特自行车，用了一年，车况良好，有锁",
    price: 350,
    category: "生活",
    images: ["https://images.pexels.com/photos/276517/pexels-photo-276517.jpeg"],
    seller: {
      id: 102,
      username: "li_si",
      avatar: "https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg"
    },
    createdAt: "2023-05-23T13:40:00Z"
  },
  {
    id: 8,
    title: "英语四级真题集",
    description: "2022年英语四级真题解析，含听力MP3",
    price: 15,
    category: "书籍",
    images: ["https://images.pexels.com/photos/256417/pexels-photo-256417.jpeg"],
    seller: {
      id: 103,
      username: "wang_wu",
      avatar: "https://images.pexels.com/photos/1681010/pexels-photo-1681010.jpeg"
    },
    createdAt: "2023-05-25T15:20:00Z"
  }
];

// 模拟用户数据
export const users = [
  {
    id: 101,
    username: "zhang_san",
    email: "zhang_san@example.com",
    avatar: "https://images.pexels.com/photos/614810/pexels-photo-614810.jpeg"
  },
  {
    id: 102,
    username: "li_si",
    email: "li_si@example.com",
    avatar: "https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg"
  },
  {
    id: 103,
    username: "wang_wu",
    email: "wang_wu@example.com",
    avatar: "https://images.pexels.com/photos/1681010/pexels-photo-1681010.jpeg"
  }
];

// 模拟订单数据
export const orders = [
  {
    id: 1001,
    productId: 3,
    buyerId: 101,
    sellerId: 103,
    status: "completed",
    price: 280,
    createdAt: "2023-06-01T09:30:00Z",
    updatedAt: "2023-06-01T14:20:00Z"
  },
  {
    id: 1002,
    productId: 5,
    buyerId: 102,
    sellerId: 104,
    status: "pending",
    price: 20,
    createdAt: "2023-06-02T11:45:00Z",
    updatedAt: "2023-06-02T11:45:00Z"
  }
];