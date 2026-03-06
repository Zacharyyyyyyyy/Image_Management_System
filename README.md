# Image_Management_System：图片管理网站

**Image_Management_System** 是一个全栈式、容器化的 Web 图像管理方案。本项目不仅涵盖了传统图库的 CRUD 操作，更集成了 **EXIF 元数据解析**、**AI 自动标签化**以及 **MCP (Model Context Protocol)** 接口，实现了从“文件存储”到“智能语义检索”的跨越。

---

## 🚀 核心特性

### 1. 智能处理流 (Smart Pipeline)
* **EXIF 自动解析**：上传时自动提取拍摄时间、地理位置（GPS）、设备型号及分辨率。
* **多尺度预览**：自动生成高质量缩略图，兼顾加载速度与展示效果。
* **AI 视觉标注**：集成预训练模型，自动识别风景、人物、动物等场景并自动打标。

### 2. 用户与安全 (Security)
* **严格验证**：实现正则化校验（用户名/密码 ≥ 6 字节，Email 格式校验），保证系统唯一性。
* **持久化存储**：采用数据库记录图片元信息，文件系统存储原始资源，确保数据一致性。

### 3. 卓越用户体验 (UX)
* **响应式设计**：采用媒体查询适配 PC、手机及微信内置浏览器，支持瀑布流与轮播展示。
* **在线编辑器**：内置图片裁剪、色调调节等轻量级编辑功能。
* **语义检索**：支持根据标签、地点、时间等多种复合条件进行模糊查询。

### 4. 扩展功能 (Advanced)
* **MCP 接口实现**：支持通过大语言模型（LLM）对话方式检索网站上的图片。

---

## 🛠 技术栈

* **后端**: Python 3.9 (Flask / FastAPI), SQLAlchemy
* **前端**: HTML5, CSS3 (Tailwind CSS), JavaScript
* **图像处理**: Pillow, ExifRead
* **容器化**: Docker, Docker Compose
* **数据库**: MySQL 8.0

---

## 📦 快速开始 (Docker 部署)

本项目已完全容器化，确保在任何环境下表现一致。

### 1. 克隆仓库
```bash
git clone [https://github.com/Zacharyyyyyyyy/Image_Management_System.git]
cd Image_Management_System

### 2. 配置环境变量
在项目根目录创建 `.env` 文件并配置相关路径：
```env
DB_PASSWORD=your_password
UPLOAD_FOLDER=./uploads
SECRET_KEY=your_runtime_secret
```

### 3. 一键启动
```bash
/* 构建并启动容器 */
docker-compose up -d --build
```
启动后，访问 `http://localhost:5000` 即可开始使用。

---

## 📂 项目结构

```text
.
├── app/
│   ├── models/          /* 数据库模型 (User, Image, Tag) */
│   ├── static/          /* 静态资源 (CSS, JS, Thumbnails) */
│   ├── templates/       /* 响应式 HTML 模板 */
│   ├── utils/           /* AI 处理与 EXIF 解析工具 */
│   └── routes/          /* 路由逻辑 (Auth, Image API) */
├── uploads/             /* 图片存储挂载点 (受 .dockerignore 保护) */
├── Dockerfile           /* 镜像构建文件 */
├── docker-compose.yml   /* 容器编排配置文件 */
├── requirements.txt     /* 依赖清单 */
└── README.md
```

---

## 🧪 实验亮点

* **唯一性约束**：在数据库层实现双重校验，确保 Email 与用户名全局唯一。
* **移动端适配**：针对手机浏览器进行深度优化，提供友好的触摸交互体验，支持图片轮播显示。
* **数据持久化**：利用 **Docker Volume** 实现宿主机与容器的数据映射，保证图片资源不因容器销毁而丢失。
* **AI 增强**：通过调用 AI 模型分析图像内容，解决了传统图片分类效率低下的问题。

---
>>>>>>> 7dcc4c8548e364adba6b17390db0c7dab21abe89
