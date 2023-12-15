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
import matplotlib.pyplot as plt


# Create your views here.
def home(request):
    return render(request, "index.html")


def content_food(item):
    if item == "Bánh chưng":
        content = "Bánh chưng là một loại bánh truyền thống của dân tộc Việt nhằm thể hiện lòng biết ơn của con cháu đối với cha ông với đất trời. Nguyên liệu làm bánh chưng gồm gạo nếp, đậu xanh, thịt lợn, lá dong. Bánh thường được làm vào các dịp Tết của dân tộc Việt, cũng như ngày giỗ tổ Hùng Vương.Bánh chưng có màu xanh, được gói theo hình vuông lớn, tượng trưng cho đất. Sự kết hợp của bánh chưng xanh và bánh dày tượng trưng cho sự kết hợp và gắn kết của đất trời. Hơn hết, người Việt Nam gắn liền với văn hóa lúa nước, phụ thuộc rất nhiều vào điều kiện thiên nhiên, trong đó đất trời là yếu tố quyết định. Chính vì lẽ đó, người ta chọn dâng bánh chưng và bánh dày vào ngày Tết để thể hiện lòng biết ơn trời đất tạo điều kiện mưa thuận gió hòa, mùa màng bội thu, nhà nhà ấm no hạnh phúc."
    elif item == "Bánh tráng":
        content = "Bánh tráng là một dạng bánh sử dụng nguyên liệu chính là tinh bột tráng mỏng phơi khô, khi ăn có thể nướng giòn,hoặc nhúng qua nước để làm nem cuốn miền nam gọi là gỏi cuốn. Nó còn là nguyên liệu để làm một món ăn khác là nem."
    elif item == "Bún":
        content = "Bún là loại thực phẩm dạng sợi tròn, trắng mềm,được làm từ tinh bột gạo ,tạo sợi qua khuôn và được luộc chín trong nước sôi. Là một nguyên liệu,thành phần chủ yếu để chế biến nhiều món ăn mà tên món ăn thường có chữ bún ở đầu (như bún cá, bún mọc, bún chả, bún thang,"
    elif item == "Phở":
        content = "Phở là một món ăn truyền thống của Việt Nam có xuất xứ từ Vân Cù, Nam Định. Phở được xem là một trong những món ăn tiêu biểu cho nền ẩm thực Việt Nam.Thành phần chính của phở là bánh phở và nước dùng cùng với thịt bò hoặc thịt gà cắt lát mỏng. Thịt bò thích hợp nhất để nấu phở là thịt, xương từ các giống bò ta (bò nội, bò vàng). Ngoài ra còn kèm theo các gia vị như: tương, tiêu, chanh, nước mắm, ớt, vân vân. Những gia vị này được thêm vào tùy theo khẩu vị của người dùng. Phở thông thường được dùng để làm món điểm tâm buổi sáng hoặc lót dạ buổi đêm; nhưng ở các thành phố lớn, món ăn này có thể được thưởng thức cả ngày. Tại các tỉnh phía Nam Việt Nam và một số vùng miền khác, phở được bày kèm với đĩa rau thơm như hành, giá và những lá cây rau mùi, rau húng, trong đó ngò gai là loại lá đặc trưng của phở; tuy nhiên tại Hà Nội thông thường sẽ không có đĩa rau sống này.."
    elif item == "Bún đậu mắm tôm":
        content = "Bún đậu mắm tôm là món ăn đơn giản, dân dã trong ẩm thực miền Bắc Việt Nam và có xuất xứ từ Hà Nội. Đây là món thường được dùng như bữa ăn nhẹ, ăn chơi. Thành phần chính gồm có bún tươi, đậu hũ chiên vàng, chả cốm, nem chua,dồi chó, mắm tôm pha chanh, ớt và ăn kèm với các loại rau thơm như tía tô, kinh giới, rau húng, xà lách, cà pháo... Cũng như các món ăn dân gian khác, giá thành rẻ nên được nhiều người giới bình dân ăn nên thu nhập của những người buôn bán những món ăn này khá cao."
    elif item == "Cháo lòng":
        content = "Cháo lòng là món cháo được nấu theo phương thức nấu cháo thông thường, trong sự kết hợp với nước dùng ngọt làm từ xương lợn hay nước luộc lòng lợn, và nguyên liệu chính cho bát cháo không thể thiếu các món phủ tạng lợn luộc, dồi. Cháo lòng tương đối phổ thông thậm chí khá bình dân trong ẩm thực Việt Nam, được bán rộng rãi tại các cửa hàng lòng lợn trong cả nước, tạo nên một bộ ba sản phẩm được ăn theo thứ tự trong bữa ăn là tiết canh, lòng lợn, cháo lòng, và thường kết hợp với rượu đế."
    elif item == "Bánh mì":
        content = "Bánh mì là một thực phẩm chế biến từ bột mì từ ngũ cốc được nghiền ra trộn với nước, thường là bằng cách nướng.Bánh mì là một món ăn Việt Nam, với lớp vỏ ngoài là một ổ bánh mì nướng có da giòn, ruột mềm, còn bên trong là phần nhân. Tùy theo văn hóa vùng miền hoặc sở thích cá nhân, người ta có thể chọn nhiều nhân bánh mì khác nhau. Tuy nhiên, loại nhân bánh truyền thống thường chứa chả lụa, thịt, cá, thực phẩm chay hoặc mứt trái cây, kèm theo một số nguyên liệu phụ khác như patê, bơ, rau, ớt, Thịt nguội với trứng và đồ chua. Bánh mì được xem như một loại thức ăn nhanh bình dân và thường được tiêu thụ trong bữa sáng hoặc bất kỳ bữa phụ nào trong ngày. Do có giá thành phù hợp nên bánh mì trở thành món ăn được rất nhiều người ưa chuộng."
    elif item == "Bánh tét":
        content = "Bánh tét, có nơi gọi là bánh đòn, là một loại bánh trong ẩm thực của cả người Việt và một số dân tộc ít người ở miền Nam và miền Trung Việt Nam, là nét tương đồng của bánh chưng ở miền Bắc về nguyên liệu, cách nấu, chỉ khác về hình dáng và sử dụng lá chuối để gói thay vì lá dong, vì vậy nó cũng được sử dụng nhiều nhất trong dịp Tết Nguyên đán cổ truyền của dân tộc Việt Nam với vai trò không khác bánh chưng. Nhưng cũng có nhiều bánh tét nhân chuối hay đậu đen được làm hay là bán quanh năm."
    elif item == "Gỏi cuốn":
        content = "Gỏi cuốn hay còn được gọi là nem cuốn (phương ngữ Bắc bộ), là một món ăn khá phổ biến ở Việt Nam. Gỏi cuốn có xuất xứ từ Miền nam Việt Nam với tên gọi là gỏi cuốn - bằng các nguyên liệu gồm rau xà lách, húng quế, tía tô, tôm khô, rau thơm, thịt luộc, tôm tươi.. tất cả được cuộn trong vỏ bánh tráng. Gia vị dùng kèm là tương hột trộn với lạc rang giã nhỏ phi bằng dầu ăn với hành khô.... tất cả thái nhỏ và cuộn trong vỏ làm từ bột mì. Gia vị dùng kèm là tương ớt trộn với lạc rang giã nhỏ phi bằng dầu ăn với hành khô."
    elif item == "Nem chua":
        content = "Nem chua (phương ngữ Bắc Bộ) hay nem (phương ngữ Trung Bộ và phương ngữ Nam Bộ) là một món ăn sử dụng thịt lợn, lợi dụng men của lá chuối (hoặc lá ổi, lá vông, lá sung v.v.) và thính gạo để ủ chín, có vị chua ngậy. Nổi tiếng ở Việt Nam như một sản vật phổ biến tại nhiều địa phương, tuy không rõ nem chua được người dân vùng nào làm ra đầu tiên. Cách chế biến nem có thể chia thành hai kiểu: Nem Miền Bắc có thể chế biến ăn sống cùng các loại lá đặc biệt; còn Nem Miền Trung (đặc biệt Thanh Hoá và Huế) được đóng gói và lên men trong một số loại lá, trong đó có lá chuối, lá ổi."
    elif item == "Cơm tấm":
        content = "Cơm tấm là một món ăn phổ biến của những người nông dân, công nhân tại vùng đồng bằng sông Cửu Long.Vào các năm mùa màng đói kém, nhiều người thường không có đủ gạo ngon để bán, vì vậy họ đã dùng gạo tấm (gạo bể) để nấu ăn vì nó luôn có sẵn trong nhà của nhiều hộ gia đình cũng như có tác dụng làm no lâu."
    else:
        content = ""
    return content


# http://127.0.0.1:8000/static/uploads/food_long.jpg
def upload_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        img_path = request.FILES["image"]
        UploadedImage.objects.create(image=img_path)
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
            "Bánh chưng",
            "Bánh mì",
            "Bánh tét",
            "Bánh tráng",
            "Bánh xèo",
            "Bún",
            "Cơm tấm",
            "Gỏi cuốn",
            "Phở",
            "Bún đậu mắm tôm",
            "Nem chua",
            "Cháo lòng",
        ]

        # percent = output.max() * 10
        percent = output
        percent = [round(num * 100, 2) for num in percent[0]]
        percent_max = max(percent)

        label_predict = LABELS[np.argmax(output)]
        print("model's prediction:", label_predict, "- Percentage:", percent, "%")

        text_food = content_food(label_predict)

        UploadedImage.objects.create(image=img_path)
        # print(img_path)
        print(percent)
        return render(
            request,
            "index.html",
            {
                "label_predict": label_predict,
                "percent": percent,
                "text": text_food,
                "link_image": img_paths,
                "percent_max": percent_max,
            },
        )

    return redirect("index")


def index(request):
    images = UploadedImage.objects.latest("timestamp")
    return render(request, "index.html", {"images": images})
