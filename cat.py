import os
import random 

from caption import generate_caption

def get_cat_url():
    import flickr_api
    
    flickr_api.set_keys(api_key=os.getenv("FLICKR_KEY"), api_secret=os.getenv("FLICKR_SECRET"))

    w = flickr_api.Walker(
        flickr_api.Photo.search, 
        text="cat", 
        license='2,3,4,5,6,9', 
        media="photos",
        orientation="square",
        sort='interestingness-desc',
        safe_search=3
    )
    photo = next(w)
    link_to_photo = photo.getPhotoFile()
    return link_to_photo

def neural_style_photo(cat_url):
    import Algorithmia
    cat_pic_service_path = "data://okhlopkov/neuralcat/styled_cat.jpg"

    neural_style = random.choice([
        "alien_goggles", "aqua", "blue_brush", "blue_granite", "bright_sand", 
        "cinnamon_rolls", "clean_view", "colorful_blocks", "colorful_dream", 
        "crafty_painting", "creativity", "crunch_paper", "dark_rain", "dark_soul", 
        "deep_connections", "dry_skin", "far_away", "green_zuma",
        "hot_spicy", "neo_instinct", "oily_mcoilface", "plentiful", "post_modern", 
        "purp_paper", "purple_pond", "purple_storm", "rainbow_festival", "really_hot", 
        "space_pizza", "gan_vogh", "really_hot", "sand_paper", "smooth_ride",
        "spagetti_accident", "sunday", "yellow_collage", "yellow_paper",
    ])

    client = Algorithmia.client(os.getenv("ALGORITHMIA_TOKEN"))
    algo = client.algo('deeplearning/DeepFilter/0.6.0')
    algo.set_options(timeout=300) # optional
    print(algo.pipe({
        'images': [cat_url],
        'savePaths': [cat_pic_service_path],
        'filterName': neural_style
    },).result)

    file = client.file(cat_pic_service_path)
    res = file.getFile()
    return res.name


def upload_photo(photo_path, text):
    from instabot import Bot
    bot = Bot()
    bot.login(
        username=os.environ['INSTAGRAM_USERNAME'], 
        password=os.environ['INSTAGRAM_PASSWORD']
    )
    return bot.upload_photo(photo_path, text)




if __name__ == '__main__':
    caption = generate_caption()
    cat_url = get_cat_url()

    styled_local_img_path = neural_style_photo(cat_url)

    upload_photo(styled_local_img_path, caption)
