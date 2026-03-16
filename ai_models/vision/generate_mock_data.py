import os
from PIL import Image, ImageDraw

def create_mock_dataset(base_dir="dataset"):
    # Typical classes from the Plant village dataset
    classes = [
        "Apple___Apple_scab",
        "Apple___Black_rot",
        "Apple___Cedar_apple_rust",
        "Apple___healthy",
        "Corn_(maize)___Cercospora_leaf_spot_Gray_leaf_spot",
        "Corn_(maize)___Common_rust_",
        "Corn_(maize)___Northern_Leaf_Blight",
        "Corn_(maize)___healthy",
        "Potato___Early_blight",
        "Potato___Late_blight",
        "Potato___healthy",
        "Tomato___Bacterial_spot",
        "Tomato___Early_blight",
        "Tomato___Late_blight",
        "Tomato___Leaf_Mold",
        "Tomato___Septoria_leaf_spot",
        "Tomato___Spider_mites_Two-spotted_spider_mite",
        "Tomato___Target_Spot",
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "Tomato___Tomato_mosaic_virus",
        "Tomato___healthy"
    ]

    for split in ["train", "valid"]:
        for c in classes:
            dir_path = os.path.join(base_dir, split, c)
            os.makedirs(dir_path, exist_ok=True)
            
            # Generate 3 mock images per class per split to make training fast and functional
            num_images = 5 if split == "train" else 2
            for i in range(num_images):
                img = Image.new('RGB', (256, 256), color = (73, 109, 137))
                d = ImageDraw.Draw(img)
                d.text((10,10), f"{c} {i}", fill=(255,255,0))
                
                # Mock a green leaf shape
                d.ellipse((50, 50, 200, 200), fill=(34,139,34), outline=(0,0,0))
                
                # Add "disease" spots if not healthy
                if "healthy" not in c.lower():
                    d.ellipse((100, 100, 120, 120), fill=(139,69,19))
                    d.ellipse((140, 150, 155, 165), fill=(139,69,19))
                
                img.save(os.path.join(dir_path, f"mock_img_{i}.jpg"))
                
    print(f"Mock dataset created in {base_dir}")

if __name__ == "__main__":
    create_mock_dataset()
