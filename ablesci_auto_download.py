import logging
logging.basicConfig(filename='error_log.txt', level=logging.ERROR)
try:
    ###多个文献下载功能
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    import time
    import os
    import sys
    import traceback


    # 获取资源路径的函数
    def resource_path(relative_path):
        """获取资源的绝对路径，适用于开发环境和PyInstaller打包后的环境"""
        try:
            # PyInstaller创建临时文件夹并将路径存储在_MEIPASS中
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    try:
        # 创建下载文件夹
        download_folder = os.path.join(os.getcwd(), "文献下载")
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
            print(f"已创建下载文件夹: {download_folder}")
        else:
            print(f"使用现有下载文件夹: {download_folder}")

        #获取cookies地址
        with open('cookies.txt', 'r') as file:
            cookies_str = file.read()
        
        # 浏览器设置
        options = Options()
        options.add_argument("--disable-images")
        options.add_argument("--disable-gpu")
        #options.add_argument("--headless=new")
        #options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")






        # 设置下载目录为专门的下载文件夹
        prefs = {
            "download.default_directory": download_folder,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        
        def get_application_path():
            """获取应用程序的实际运行路径"""
            if getattr(sys, 'frozen', False):
                # 如果是打包后的可执行文件
                return os.path.dirname(sys.executable)
            else:
                # 如果是普通Python脚本
                return os.path.dirname(os.path.abspath(__file__))

        try:
            # 尝试使用自动管理模式
            options = Options()
            driver = webdriver.Chrome(options=options)
        except Exception as e:
            print(f"自动管理失败: {e}")
            print("尝试使用本地ChromeDriver...")
            
            # 使用本地ChromeDriver
            # 查找可能的chromedriver位置
            app_path = get_application_path()
            possible_paths = [
                os.path.join(app_path, "chromedriver.exe"),  # 应用程序目录
                os.path.join(os.getcwd(), "chromedriver.exe"),  # 当前工作目录
                "chromedriver.exe"  # 相对路径
            ]
            
            driver_found = False
            for chrome_driver_path in possible_paths:
                if os.path.exists(chrome_driver_path):
                    print(f"找到ChromeDriver: {chrome_driver_path}")
                    service = Service(executable_path=chrome_driver_path)
                    driver = webdriver.Chrome(service=service)
                    driver_found = True
                    break
            
            if not driver_found:
                paths_str = "\n".join(possible_paths)
                raise Exception(f"ChromeDriver未找到，已尝试以下路径:\n{paths_str}")

        driver.minimize_window()

        
        wait = WebDriverWait(driver, 20)
        print('请输入DOI或PMID，多个请用分号(;)分隔：')
        input_content = input()
        
        # 分割多个DOI
        doi_list = [doi.strip() for doi in input_content.split(';') if doi.strip()]
        print(f"检测到{len(doi_list)}个DOI/PMID")
        
        # 初次访问网站以设置Cookie
        driver.get("https://www.ablesci.com/")
        
        
        for cookie in cookies_str.split(';'):
            name, value = cookie.strip().split('=', 1)
            driver.add_cookie({'name': name, 'value': value, 'domain': '.ablesci.com'})
        
        # 刷新页面使Cookie生效
        driver.refresh()

        # 记录成功下载的DOI
        successful_downloads = []
        failed_downloads = []
        
        # 处理每个DOI
        for index, doi in enumerate(doi_list, 1):
            print(f"\n正在处理第 {index}/{len(doi_list)} 个DOI/PMID: {doi}")
            
            try:
                # 每次处理新DOI时，点击导航按钮回到文献查询页面
                time.sleep(2)
                nav_button = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "body > div.able-header.header-bg-assist > div > div > a")))
                print("正在跳转到查询页面...")
                nav_button.click()
                
                # 表单操作
                input_selector = "#onekey"
                submit_selector = "#assist-create-form > div.alert.alert-success > div.layui-form-item.layui-row > div:nth-child(2) > div > button"
                confirm_button = '#layui-layer2 > div.layui-layer-btn.layui-layer-btn- > a.layui-layer-btn0'
                
                wait.until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, input_selector))).clear()  # 清除之前的输入
                wait.until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, input_selector))).send_keys(doi)
                
                wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, submit_selector))).click()
                time.sleep(2)
                wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, confirm_button))).click()
                
                ##点击查看求助详情
                ask_detail = '#layui-layer5 > div.layui-layer-btn.layui-layer-btn- > a'
                wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ask_detail))).click()
                
                # 获取当前页面的 URL(暂时无用)
                current_url = driver.current_url
                match = re.search(r'id=([^&]+)', current_url)
                if match:
                    article_id = match.group(1)
                else:
                    article_id = None

                # 等待确认框出现并点击
                print(f"正在搜索文献 DOI/PMID: {doi}，这可能需要几分钟...")
                
                ###获取文献名称
                
                article_name = driver.find_element(By.CSS_SELECTOR, "#LAY_ucm > div:nth-child(1) > div.assist-detail.layui-row > div > table > tbody > tr:nth-child(1) > td.assist-title > div:nth-child(1)")
                article_name_content = article_name.text
                
                # 使用较长的等待时间
                long_wait = WebDriverWait(driver, 28800)  # 8小时
                confirm_button = long_wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#layui-layer1 > div > div:nth-child(3) > div.layui-layer-btn.layui-layer-btn- > a")))
                print("确认文献")
                confirm_button.click()
                ##查看并审核
                censor_button = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#layui-layer1 > div.layui-layer-btn.layui-layer-btn- > a")))
                censor_button.click()
                time.sleep(2)
                

                # 点击下载链接
                print("等待下载链接出现...")
                download_link = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "a[title='点击下载']")))
                download_url = download_link.get_attribute("href")
                print("下载地址:", download_url)
                print("点击下载链接...")
                download_link.click()
                time.sleep(1)
                ###自动采纳
                wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#uploaded-file-handle > button:nth-child(1)"))).click()
                wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#layui-layer2 > div.layui-layer-btn.layui-layer-btn- > a.layui-layer-btn0"))).click()
                wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#layui-layer4 > div.layui-layer-btn.layui-layer-btn- > a"))).click()
                # 等待下载完成
                print(f"文献 {article_name_content} 的下载已开始")
                time.sleep(10)  # 给下载一些时间启动
                
                successful_downloads.append(doi)
                
            except Exception as e:
                error_msg = f"处理DOI/PMID: {doi} 时发生错误: {str(e)}"
                print(error_msg)
                print(traceback.format_exc())
                failed_downloads.append(doi)
                
                # 尝试恢复到初始页面，以便继续处理下一个DOI
                try:
                    driver.get("https://www.ablesci.com/")
                    time.sleep(2)
                except:
                    print("无法恢复到初始页面，将尝试继续处理下一个DOI")
        
        # 所有DOI处理完成后，等待所有下载完成
        if successful_downloads:
            print("\n所有文献处理完成，等待下载完成...")
            wait_time = 10 + (5 * len(successful_downloads))  # 基础等待时间加上每个DOI的额外等待时间
            time.sleep(wait_time)
            
            # 列出下载文件夹中的文件
            print("\n下载文件夹中的最新文件:")
            recent_files = []
            for file in os.listdir(download_folder):
                file_path = os.path.join(download_folder, file)
                if os.path.isfile(file_path):
                    # 记录文件和其创建时间
                    recent_files.append((file, os.path.getctime(file_path)))
            
            # 按创建时间排序，最新的在前
            recent_files.sort(key=lambda x: x[1], reverse=True)
            
            # 显示最新的10个文件或者全部（如果少于10个）
            for file, create_time in recent_files[:10]:
                create_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(create_time))
                print(f"- {file} (创建时间: {create_time_str})")
        
        # 显示处理结果摘要
        print("\n处理结果摘要:")
        print(f"- 成功处理的文献: {len(successful_downloads)}/{len(doi_list)}")
        if successful_downloads:
            print(f"- 成功的文献: {', '.join(successful_downloads)}")
        if failed_downloads:
            print(f"- 失败的文献: {', '.join(failed_downloads)}")

    except Exception as e:
        error_msg = f"程序执行过程中发生错误: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())

    finally:
        # 保持浏览器窗口开启，直到用户手动关闭
        credits = driver.find_element(By.CSS_SELECTOR, "#user-point-now")
        credits_content = credits.text
        print('- 您的剩余积分：'+ credits_content)
        input("\n所有操作已完成，按回车键关闭...")
        if 'driver' in locals():
            driver.quit()

except Exception as e:
    logging.error(f"发生错误: {str(e)}")
    input("按Enter键退出...")
    driver.quit()
