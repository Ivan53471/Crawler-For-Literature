from download import download

def main():
    # # 获取所有PDF文件的下载URL
    # download_urls = get_download_urls()
    # # 写入文件保存
    # if download_urls:
    #     with open('download_urls.txt', 'w') as f:
    #         for url in download_urls:
    #             f.write(url + '\n')
    download()

if __name__ == "__main__":
    main()
