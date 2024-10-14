from bing_image_downloader import downloader

# Download images
downloader.download(
    query="yuru camp",  
    limit=10,
    output_dir='yuru casdadsmp',
    adult_filter_off=False,  
    force_replace=False,
    timeout=60,
    verbose=True
)
