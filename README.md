<<<<<<< HEAD
# Image Management Website



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/topics/git/add_files/#add-files-to-a-git-repository) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://git.zju.edu.cn/3230105233/image-management-website.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://git.zju.edu.cn/3230105233/image-management-website/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/user/project/merge_requests/auto_merge/)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
=======
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
