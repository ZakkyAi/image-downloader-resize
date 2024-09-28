from bing_image_downloader import downloader

# Download images
downloader.download(
    query="four-legged animal",  
    limit=150,
    output_dir='hewan berkaki 4',
    adult_filter_off=False,  
    force_replace=False,
    timeout=60,
    verbose=True
)
