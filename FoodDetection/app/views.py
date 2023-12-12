from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from .models import UploadedImage
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from keras.models import load_model
import numpy as np
import wikipedia
from django.http import JsonResponse


# Create your views here.
def home(request):
    return render(request, "index.html")


def predict(request):
    if request.method == "POST" and request.FILES["image"]:
        img_path = request.FILES["image"]

        img = image.load_img(img_path, target_size=(224, 224))
        img = image.img_to_array(img)

        # load efficientnet
        efficientNet = EfficientNetB0(include_top=False, weights="imagenet")
        # load task model
        classify_model = load_model("Dish_Recognition_12.h5")

        feature = np.expand_dims(img, axis=0)
        feature = preprocess_input(feature)
        feature = efficientNet.predict(feature)
        output = classify_model.predict(feature)

        LABELS = [
            "Banh chung",
            "Banh mi",
            "Banh tet",
            "Banh trang",
            "Banh xeo",
            "Bun",
            "Com tam",
            "Goi cuon",
            "Pho",
            "Bun dau mam tom",
            "Nem chua",
            "Chao long",
        ]

        percent = output.max() * 100
        label_predict = LABELS[np.argmax(output)]
        print("model's prediction:", label_predict, "- Percentage:", percent, "%")

        text_food = content_food(label_predict)

        return JsonResponse(
            {"label_predict": label_predict, "percent": percent, "text": text_food}
        )


def content_food(item):
    if item == "Banh mi":
        content = wikipedia.summary("Bánh mì")
    elif item == "Banh trang":
        content = wikipedia.summary("Bánh tráng nướng")
    elif item == "Bun":
        content = wikipedia.summary("Bún")
    elif item == "Pho":
        content = wikipedia.summary("Phở")
    elif item == "Bun dau mam tom":
        content = "Bún đậu mắm tôm là món ăn đơn giản, dân dã trong ẩm thực miền Bắc Việt Nam và có xuất xứ từ Hà Nội. Đây là món thường được dùng như bữa ăn nhẹ, ăn chơi. Thành phần chính gồm có bún tươi, đậu hũ chiên vàng, chả cốm, nem chua,dồi chó, mắm tôm pha chanh, ớt và ăn kèm với các loại rau thơm như tía tô, kinh giới, rau húng, xà lách, cà pháo...[1] Cũng như các món ăn dân gian khác, giá thành rẻ nên được nhiều người giới bình dân ăn nên thu nhập của những người buôn bán những món ăn này khá cao.[2]"
    elif item == "chao long":
        content = "Cháo lòng là món cháo được nấu theo phương thức nấu cháo thông thường, trong sự kết hợp với nước dùng ngọt làm từ xương lợn hay nước luộc lòng lợn, và nguyên liệu chính cho bát cháo không thể thiếu các món phủ tạng lợn luộc, dồi. Cháo lòng tương đối phổ thông thậm chí khá bình dân trong ẩm thực Việt Nam, được bán rộng rãi tại các cửa hàng lòng lợn trong cả nước, tạo nên một bộ ba sản phẩm được ăn theo thứ tự trong bữa ăn là tiết canh, lòng lợn, cháo lòng, và thường kết hợp với rượu đế."
    else:
        content = wikipedia.summary(item)

    return content


# http://127.0.0.1:8000/static/uploads/food_long.jpg
def upload_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        img_path = request.FILES["image"]
        img_path = str(img_path)
        img_paths = "../../static/uploads/" + img_path
        img_pathss = (
            "D:\\Machine learning\\Project\\Food-detection\\FoodDetection\\static\\uploads\\"
            + img_path
        )
        # img_paths = img_path
        # # img_path = request.FILES['image']
        # print(img_paths)
        img = image.load_img(
            img_pathss,
            target_size=(224, 224),
        )

        img = image.img_to_array(img)
        print(img)
        # load efficientnet
        efficientNet = EfficientNetB0(include_top=False, weights="imagenet")
        # load task model
        classify_model = load_model("Dish_Recognition_12.h5")

        feature = np.expand_dims(img, axis=0)
        feature = preprocess_input(feature)
        feature = efficientNet.predict(feature)
        output = classify_model.predict(feature)

        LABELS = [
            "Banh chung",
            "Banh mi",
            "Banh tet",
            "Banh trang",
            "Banh xeo",
            "Bun",
            "Com tam",
            "Goi cuon",
            "Pho",
            "Bun dau mam tom",
            "Nem chua",
            "Chao long",
        ]

        percent = output.max() * 100
        label_predict = LABELS[np.argmax(output)]
        print("model's prediction:", label_predict, "- Percentage:", percent, "%")

        text_food = content_food(label_predict)

        UploadedImage.objects.create(image=img_path)
        # print(img_path)

        return render(
            request,
            "index.html",
            {
                "label_predict": label_predict,
                "percent": percent,
                "text": text_food,
                "link_image": img_paths,
            },
        )

    return redirect("index")


def index(request):
    images = UploadedImage.objects.latest("timestamp")
    return render(request, "index.html", {"images": images})
