# from app.db.mongodb import users

# # users.insert_one({
# #     "name": "Kumar Shanu",
# #     "email": "kumar@examhai.com"
# # })
# from app.db.user_repo import user_repo

# # data=user_repo.get_user_by_user_id("KUMA-1DC235")
# # print("User data:- ",data)

# resp=user_repo.get_user_by_email("kumarshanu1881@gmail.com")
# print("User resp:- ",resp)
# print("Connected successfully!")

from pathlib import Path
import cv2

img = Path(
r"C:\Users\bnsah\OneDrive\文档\PROJECTS(FINAL)\SecureFace AI\test\evaluation\dataset\celeba_subset\000023.jpg"
)

print(img.exists())

image = cv2.imread(str(img))

print(image)

if image is not None:
    print(image.shape)