# 科研通文献批量下载工具

🔍 **工具简介**  
本工具是基于Python和Selenium开发的自动化文献下载脚本，通过输入DOI号/PMID批量从科研通学术互助平台下载文献。支持自动创建下载目录、多任务处理、下载状态追踪等功能，适用于科研工作者高效获取文献资源。
———————————————————————————————

2025-03-29更新：
加入多线程处理功能，可自动指定最高线程数，同时下载多个DOI，详见ablesci_auto_download_multithreads

---

## 🚀 主要功能

- **批量DOI/PMID处理**：支持分号分隔的多DOI/PMID同时并且混合输入
- **自动化流程**：
  - 自动/手动管理chrome浏览器driver
  - 自动创建/识别下载文件夹（`文献下载`）
  - 自动配置浏览器参数（禁用图片加载、优化下载设置）
  - 自动处理网站Cookies和页面跳转
  - 自动点击确认按钮与下载链接
- **状态监控**：
  - 实时显示处理进度（成功/失败计数）
  - 错误捕获与异常处理机制
  - 最终下载文件列表展示（显示最新10个文件）
- **长时任务支持**：单文献最长等待8小时（适用于数据库资源较少的文献）

---

## ⚙️ 使用说明

### 环境要求

- Python 3.10+（其余版本未测试）

- Chrome浏览器

- 所需依赖：  

  ```bash
  pip install -r requirements.txt
  ```

### 快速开始

1. **配置Cookies**（重要！）  
   将您登录后的有效cookies复制并保存至ablesci_auto_download.py同目录下的cookies.txt文件中（注意不要留空格）

2. **运行脚本**  

   ```bash
   python ablesci_auto_download.py
   ```

3. **输入DOI/PMID**  

   ```
   请输入DOI/PMID，多个请用分号(;)分隔：
   (示例) 10.1038/s41586-023-06900-0;28463612
   ```

4. **等待执行**  

   - 自动获取Chrome driver
   - 自动弹出Chrome浏览器窗口
   - 实时显示处理进度
   - 处理完后自动显示积分余额
   - 完成后按回车键关闭浏览器

---

## 📂 文件管理

- **下载目录**：自动创建在脚本同级的`文献下载`文件夹
- **文件列表**：完成后显示按创建时间排序的最新文件
- **日志记录**：
  - 终端显示成功/失败DOI列表
  - 错误信息包含详细堆栈追踪

---

## ⚠️ 注意事项

1. **Cookies有效性**：需定期更新cookies以确保登录状态
2. **网络环境**：需保持稳定网络连接
3. **安全警告**：  
   - 本工具仅限合法获取已授权的文献资源
   - 使用者需遵守平台服务条款和著作权法
4. **性能优化**：
   - 默认禁用图片加载以提升速度
   - 每个DOI处理间隔2秒防止高频请求
   - 下载超时时间可自行调整

---

## 📜 免责声明  

本工具仅用于技术研究目的，开发者不对滥用行为负责。使用者应确保遵守相关学术平台的规定和版权法律要求，请在法律允许范围内使用本工具。
